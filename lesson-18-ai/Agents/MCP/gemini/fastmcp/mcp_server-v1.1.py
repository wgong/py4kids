import uvicorn
from fastmcp import FastMCP

from pydantic import BaseModel, Field
import logging
import yfinance as yf

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize the MCPServer ---
mcp = FastMCP("Demo 🚀")

# --- Pydantic Models for Calculator Tool ---
class CalculatorInput(BaseModel):
    operation: str = Field(..., description="The arithmetic operation to perform.", examples=["add", "subtract", "multiply", "divide"])
    num1: float = Field(..., description="The first number.")
    num2: float = Field(..., description="The second number.")

class CalculatorOutput(BaseModel):
    value: float = Field(..., description="The result of the arithmetic operation.")

# --- Define the Calculator Tool ---
@mcp.tool()
async def calculator_tool(input: CalculatorInput) -> CalculatorOutput:
    """
    Performs the specified arithmetic operation on two numbers.
    Supports 'add', 'subtract', 'multiply', and 'divide'.
    """
    logging.info(f"Received calculator_tool call: {input.model_dump()}")
    
    if input.operation == "add":
        result = input.num1 + input.num2
    elif input.operation == "subtract":
        result = input.num1 - input.num2
    elif input.operation == "multiply":
        result = input.num1 * input.num2
    elif input.operation == "divide":
        if input.num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = input.num1 / input.num2
    else:
        raise ValueError(f"Unsupported operation: {input.operation}. Supported operations: add, subtract, multiply, divide")
    
    return CalculatorOutput(value=result)

# --- Pydantic Models for Yahoo Finance Tool ---
class YahooFinanceInput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol (e.g., GOOG, AAPL, TSLA).")

class YahooFinanceOutput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    current_price: float | None = Field(None, description="The current trading price of the stock.")
    currency: str | None = Field(None, description="The currency of the stock price.")
    long_name: str | None = Field(None, description="The full company name.")
    market_cap: int | None = Field(None, description="Market capitalization.")
    error: str | None = Field(None, description="Error message if data retrieval failed.")

# --- Define the Yahoo Finance Tool ---
@mcp.tool()
async def yahoo_finance_tool(input: YahooFinanceInput) -> YahooFinanceOutput:
    """
    Retrieves live stock data for a given ticker symbol using yfinance.
    """
    logging.info(f"Received yahoo_finance_tool call for ticker: {input.ticker}")
    
    try:
        ticker_data = yf.Ticker(input.ticker)
        info = ticker_data.info
        
        # Get current price - try multiple fields as yfinance can be inconsistent
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        
        # Try to get recent data if info doesn't have current price
        if current_price is None:
            try:
                hist = ticker_data.history(period="1d")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
            except Exception as e:
                logging.warning(f"Could not get historical data for {input.ticker}: {e}")
        
        currency = info.get('currency', 'USD')
        long_name = info.get('longName', info.get('shortName', 'Unknown'))
        market_cap = info.get('marketCap')
        
        if current_price is None:
            error_msg = f"Could not retrieve current price for {input.ticker}. Ticker may be invalid."
            logging.warning(error_msg)
            return YahooFinanceOutput(
                ticker=input.ticker,
                current_price=None,
                currency=currency,
                long_name=long_name,
                market_cap=market_cap,
                error=error_msg
            )

        return YahooFinanceOutput(
            ticker=input.ticker,
            current_price=float(current_price),
            currency=currency,
            long_name=long_name,
            market_cap=market_cap,
            error=None
        )
        
    except Exception as e:
        error_msg = f"Failed to get stock data for '{input.ticker}': {str(e)}"
        logging.error(error_msg, exc_info=True)
        return YahooFinanceOutput(
            ticker=input.ticker,
            current_price=None,
            currency=None,
            long_name=None,
            market_cap=None,
            error=error_msg
        )

# --- Health Check Endpoint ---
@mcp.tool()
async def health_check() -> dict:
    """
    Simple health check tool to verify server is running.
    """
    return {"status": "healthy", "message": "MCP Server is running"}

# --- Main execution block ---
if __name__ == "__main__":
    logging.info("Starting MCP Server with fastmcp and Uvicorn...")
    print("🚀 MCP Server starting...")
    print("📡 Server will be accessible at http://127.0.0.1:5000")
    print("🔧 MCP endpoint: http://127.0.0.1:5000/mcp")
    print("📊 Available tools: calculator_tool, yahoo_finance_tool, health_check")
    
    # The server will be accessible at http://127.0.0.1:5000/mcp
    uvicorn.run(mcp, host="127.0.0.1", port=5000)