import uvicorn
from fastmcp import FastMCP

from pydantic import BaseModel, Field
import logging
import yfinance as yf # New import for Yahoo Finance

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize the MCPServer ---

mcp = FastMCP("Demo 🚀")

# --- Pydantic Models for Calculator Tool ---
class CalculatorInput(BaseModel):
    operation: str = Field(..., description="The arithmetic operation to perform.", examples=["add", "subtract"])
    num1: float = Field(..., description="The first number.")
    num2: float = Field(..., description="The second number.")

class CalculatorOutput(BaseModel):
    value: float = Field(..., description="The result of the arithmetic operation.")

# --- Define the Calculator Tool ---
@mcp.tool()
async def calculator_tool(input: CalculatorInput) -> CalculatorOutput:
    """
    Performs the specified arithmetic operation on two numbers.
    Currently supports 'add' and 'subtract'.
    """
    logging.info(f"Received calculator_tool call: {input.model_dump()}")
    if input.operation == "add":
        result = input.num1 + input.num2
    elif input.operation == "subtract":
        result = input.num1 - input.num2
    else:
        raise ValueError(f"Unsupported operation: {input.operation}. Only 'add' and 'subtract' are supported.")
    return CalculatorOutput(value=result)

# --- Pydantic Models for Yahoo Finance Tool ---
class YahooFinanceInput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol (e.g., GOOG, AAPL, TSLA).")

class YahooFinanceOutput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    current_price: float | None = Field(None, description="The current trading price of the stock.")
    currency: str | None = Field(None, description="The currency of the stock price.")
    long_name: str | None = Field(None, description="The full company name.")
    # You can add more fields from yfinance.Ticker.info as needed (e.g., 'marketCap', 'volume', 'fiftyTwoWeekHigh')

# --- Define the Yahoo Finance Tool ---
@mcp.tool()
async def yahoo_finance_tool(input: YahooFinanceInput) -> YahooFinanceOutput:
    """
    Retrieves live stock data for a given ticker symbol using yfinance.
    """
    logging.info(f"Received yahoo_finance_tool call for ticker: {input.ticker}")
    try:
        ticker_data = yf.Ticker(input.ticker)
        # Fetch info with a timeout to prevent hanging
        info = ticker_data.info
        # Note: yfinance's .info can sometimes return incomplete data or raise errors
        # if the ticker is invalid or there's a network issue.
        # Robust error handling for specific yfinance responses might be needed in production.

        current_price = info.get('currentPrice')
        currency = info.get('currency')
        long_name = info.get('longName')

        if current_price is None:
            logging.warning(f"Could not retrieve current price for {input.ticker}. "
                           f"Info keys available: {list(info.keys()) if info else 'None'}")
            # Return partial data if price isn't available, or raise a more specific error
            # depending on your application's requirements.
            return YahooFinanceOutput(
                ticker=input.ticker,
                current_price=None,
                currency=currency,
                long_name=long_name
            )

        return YahooFinanceOutput(
            ticker=input.ticker,
            current_price=current_price,
            currency=currency,
            long_name=long_name
        )
    except Exception as e:
        logging.error(f"Error fetching data for {input.ticker} from Yahoo Finance: {e}", exc_info=True)
        # Re-raise a ValueError that the client can catch and report
        raise ValueError(f"Failed to get stock quote for '{input.ticker}': {e}")

# --- Main execution block ---
if __name__ == "__main__":
    logging.info("Starting MCP Server with fastmcp and Uvicorn...")
    # The server will be accessible at http://127.0.0.1:5000/mcp
    uvicorn.run(mcp, host="127.0.0.1", port=5000)
