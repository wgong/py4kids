from fastmcp import FastMCP
import logging
import yfinance as yf
import math

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize the MCP Server ---
mcp = FastMCP("Demo 🚀")

# --- Define the Calculator Tool ---
@mcp.tool()
def calculator(operation: str, num1: float, num2: float) -> dict:
    """
    Performs arithmetic operations on two numbers.
    Supports: add, subtract, multiply, divide, power
    """
    logging.info(f"Calculator called: {operation} {num1} {num2}")
    
    try:
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return {"error": "Cannot divide by zero"}
            result = num1 / num2
        elif operation == "power":
            if num1 == 0:
                return {"error": "Base cannot be 0"}
            result = pow(num1, num2)
        elif operation == "sine":
            result = math.sin(math.radians(num1))
        else:
            return {"error": f"Unsupported operation: {operation}. Use: add, subtract, multiply, divide, power"}
        
        return {
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result,
            "expression": f"{num1} {operation} {num2} = {result}"
        }
    except Exception as e:
        logging.error(f"Calculator error: {e}")
        return {"error": str(e)}

@mcp.tool()
def trig(operation: str, theta: float) -> dict:
    """
    Performs trigonometric operation on an angle in degree.
    Supports: sine, cosine, tangent
    """
    logging.info(f"Trig called: {operation} {theta}")

    try:
        if operation == "sine":
            result = math.sin(math.radians(theta))
        elif operation == "cosine":
            result = math.cos(math.radians(theta))
        elif operation == "tangent":
            result = math.tan(math.radians(theta))
        else:
            return {"error": f"Unsupported operation: {operation}. Use: sine, cosine, tangent"}
        
        return {
            "operation": operation,
            "theta": theta,
            "result": result,
            "expression": f"{operation} ( {theta} ) = {result}"
        }
    except Exception as e:
        logging.error(f"Trig error: {e}")
        return {"error": str(e)}


# --- Define the Yahoo Finance Tool ---
@mcp.tool()
def stock_quote(ticker: str) -> dict:
    """
    Retrieves live stock data for a given ticker symbol.
    Example: AAPL, GOOGL, MSFT, TSLA
    """
    logging.info(f"Stock quote requested for: {ticker}")
    
    try:
        ticker_data = yf.Ticker(ticker.upper())
        info = ticker_data.info
        
        # Get current price - try multiple fields
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        
        # Fallback to recent historical data
        if current_price is None:
            try:
                hist = ticker_data.history(period="1d")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
            except Exception:
                pass
        
        if current_price is None:
            return {
                "ticker": ticker.upper(),
                "error": f"Could not retrieve price data for {ticker}. Ticker may be invalid."
            }
        
        return {
            "ticker": ticker.upper(),
            "current_price": round(float(current_price), 2),
            "currency": info.get('currency', 'USD'),
            "company_name": info.get('longName', info.get('shortName', 'Unknown')),
            "market_cap": info.get('marketCap'),
            "previous_close": info.get('previousClose'),
            "volume": info.get('volume'),
            "day_high": info.get('dayHigh'),
            "day_low": info.get('dayLow')
        }
        
    except Exception as e:
        logging.error(f"Yahoo Finance error for {ticker}: {e}")
        return {
            "ticker": ticker.upper(),
            "error": f"Failed to get stock data: {str(e)}"
        }

# --- Define a Health Check Tool ---
@mcp.tool()
def health() -> dict:
    """
    Simple health check to verify server is running.
    """
    return {
        "status": "healthy",
        "message": "MCP Server is running properly",
        "available_tools": ["calculator", "stock_quote", "health", "echo", ],
        "server_name": "Demo 🚀"
    }

# --- Add a simple echo tool for testing ---
@mcp.tool()
def echo(message: str) -> dict:
    """
    Echo back the provided message. Useful for testing.
    """
    return {
        "original_message": message,
        "echo": f"Echo: {message}",
        "length": len(message),
        "timestamp": "2025-05-28"
    }

# --- Add a resource for server info ---
@mcp.resource("info://server")
def server_info() -> str:
    """
    Provides basic information about this MCP server.
    """
    return "This is a demo MCP server built with FastMCP. It provides calculator and stock quote tools."

# --- Add a dynamic resource for stock info ---
@mcp.resource("stock://{ticker}")
def stock_info(ticker: str) -> str:
    """
    Provides basic stock information as a resource.
    """
    try:
        ticker_data = yf.Ticker(ticker.upper())
        info = ticker_data.info
        company_name = info.get('longName', ticker.upper())
        return f"{company_name} ({ticker.upper()}) - A publicly traded company"
    except:
        return f"Stock ticker: {ticker.upper()}"

# --- Main execution block ---
if __name__ == "__main__":
    logging.info("Starting MCP Server with FastMCP...")
    print("🚀 MCP Server Starting...")
    print("📊 Available tools:")
    print("   • calculator - Perform arithmetic operations") 
    print("   • trig - Perform Trigonometric operations") 
    print("   • stock_quote - Get stock price data")
    print("   • health - Server health check")
    print("   • echo - Echo messages for testing")
    print("📚 Available resources:")
    print("   • info://server - Server information")
    print("   • stock://{ticker} - Stock information")
    print("✅ Server ready! Starting on default port...")
    
    # Run the server using FastMCP's built-in method
    mcp.run()