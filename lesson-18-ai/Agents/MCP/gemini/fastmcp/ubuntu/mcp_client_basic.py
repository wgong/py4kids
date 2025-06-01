import asyncio
import json
import logging
import re
from typing import Dict, List, Any, Optional
from fastmcp import Client

# Configure logging with DEBUG level to see what's happening
# other levels include (INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Simple Query Parser ---
class QueryParser:
    """Parse natural language queries into tool calls"""
    
    @staticmethod
    def parse_calculator_query(query: str) -> Optional[Dict[str, Any]]:
        """Parse math queries"""
        query = query.lower().strip()
        
        # Operation patterns
        patterns = [
            ("add", ["plus", "add", "+", "sum"]),
            ("subtract", ["minus", "subtract", "-", "difference"]),
            ("multiply", ["times", "multiply", "*", "×", "product"]),
            ("divide", ["divide", "divided by", "/", "÷"]),
        ]
        
        for operation, keywords in patterns:
            for keyword in keywords:
                if keyword in query:
                    # Extract numbers
                    numbers = re.findall(r'-?\d+(?:\.\d+)?', query)
                    if len(numbers) >= 2:
                        try:
                            return {
                                "tool": "calculator",
                                "params": {
                                    "operation": operation,
                                    "num1": float(numbers[0]),
                                    "num2": float(numbers[1])
                                }
                            }
                        except ValueError:
                            pass
        return None
    
    @staticmethod
    def parse_stock_query(query: str) -> Optional[Dict[str, Any]]:
        """Parse stock price queries"""
        query_lower = query.lower().strip()
        
        stock_keywords = ["stock", "price", "quote", "ticker", "share"]
        if any(keyword in query_lower for keyword in stock_keywords):
            # Extract ticker symbols (2-5 uppercase letters)
            tickers = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
            if tickers:
                # Filter out common words that aren't tickers
                excluded_words = {"GET", "THE", "FOR", "AND", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "HAD", "HAS", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WHO", "BOY", "DID", "CAR", "EAT", "FAR", "FUN", "GOT", "HIM", "LET", "MAN", "PUT", "SAY", "SHE", "TOO", "USE"}
                valid_tickers = [t for t in tickers if t not in excluded_words]
                if valid_tickers:
                    return {
                        "tool": "stock_quote", 
                        "params": {
                            "ticker": valid_tickers[0]
                        }
                    }
        
        # Also check for common ticker patterns without explicit stock keywords
        common_tickers = ["AAPL", "GOOGL", "GOOG", "MSFT", "TSLA", "AMZN", "META", "NVDA", "AMD", "INTC"]
        for ticker in common_tickers:
            if ticker in query.upper():
                return {
                    "tool": "stock_quote",
                    "params": {
                        "ticker": ticker
                    }
                }
        
        return None
    
    @staticmethod 
    def parse_query(query: str) -> Optional[Dict[str, Any]]:
        """Main query parser"""
        # Health check
        if any(word in query.lower() for word in ["health", "status", "ping"]):
            return {"tool": "health", "params": {}}
        
        # Echo test
        if query.lower().startswith("echo "):
            message = query[5:].strip()
            return {
                "tool": "echo",
                "params": {"message": message}
            }
        
        # Try calculator
        calc_result = QueryParser.parse_calculator_query(query)
        if calc_result:
            return calc_result
        
        # Try stock query
        stock_result = QueryParser.parse_stock_query(query)
        if stock_result:
            return stock_result
        
        return None

def extract_result_data(result):
    """Extract actual data from FastMCP result object"""
    try:
        # Debug: Print what we're actually getting
        logging.debug(f" Raw result type: {type(result)}")
        logging.debug(f" Raw result: {result}")
        
        # FastMCP returns a list of TextContent objects directly
        if isinstance(result, list) and len(result) > 0:
            logging.debug(f" Result is a list with {len(result)} items")
            content_item = result[0]
            logging.debug(f" Content item type: {type(content_item)}")
            logging.debug(f" Content item: {content_item}")
            
            if hasattr(content_item, 'text'):
                logging.debug(f" Content text: {content_item.text}")
                # Try to parse as JSON
                try:
                    parsed_data = json.loads(content_item.text)
                    logging.debug(f" Parsed JSON data: {parsed_data}")
                    return parsed_data
                except json.JSONDecodeError as e:
                    logging.debug(f" JSON decode failed: {e}")
                    return {"text": content_item.text}
            else:
                logging.debug(f" Content item has no text attribute")
                return {"content": str(content_item)}
        
        # Fallback: Check if it has content attribute (old path)
        elif hasattr(result, 'content') and result.content:
            logging.debug(f" Found content attribute with {len(result.content)} items")
            content_item = result.content[0]
            if hasattr(content_item, 'text'):
                try:
                    parsed_data = json.loads(content_item.text)
                    return parsed_data
                except json.JSONDecodeError:
                    return {"text": content_item.text}
            else:
                return {"content": str(content_item)}
        
        else:
            logging.debug(f" No recognizable structure found")
            # Maybe it's already the data we need?
            if isinstance(result, dict):
                logging.debug(f" Result is already a dict")
                return result
            else:
                logging.debug(f" Converting result to string: {str(result)}")
                return {"result": str(result)}
                
    except Exception as e:
        logging.debug(f" Exception in extract_result_data: {e}")
        logging.error(f"Error extracting result data: {e}", exc_info=True)
        return {"error": f"Could not parse result: {e}"}
def format_result(tool_name: str, result: Dict) -> str:
    """Format tool results for display"""
    if isinstance(result, dict) and "error" in result:
        return f"❌ Error: {result['error']}"
    
    if tool_name == "calculator":
        if "result" in result:
            return f"""🧮 {result.get('expression', f'{result["num1"]} {result["operation"]} {result["num2"]} = {result["result"]}')}"""
        elif "error" in result:
            return f"❌ Calculator Error: {result['error']}"
    
    elif tool_name == "stock_quote":
        if "current_price" in result:
            name = result.get('company_name', result['ticker'])
            price = result['current_price']
            currency = result.get('currency', 'USD')
            extra_info = []
            if result.get('volume'):
                extra_info.append(f"Vol: {result['volume']:,}")
            if result.get('day_high') and result.get('day_low'):
                extra_info.append(f"Range: {result['day_low']}-{result['day_high']}")
            extra = f" ({', '.join(extra_info)})" if extra_info else ""
            return f"📈 {name} ({result['ticker']}): {currency} {price}{extra}"
        elif "error" in result:
            return f"❌ Stock Error: {result['error']}"
    
    elif tool_name == "health":
        return f"✅ {result.get('message', 'Server is healthy')}"
    
    elif tool_name == "echo":
        return f"🔊 {result.get('echo', result.get('message', str(result)))}"
    
    return f"✅ Result: {json.dumps(result, indent=2)}"

# --- Main Demo ---
async def run_demo():
    logging.info("🚀 MCP Client Demo Starting...")
    
    # Connect to the FastMCP server directly
    server_path = "mcp_server.py"  # Path to your server file
    
    try:
        logging.info(f"📡 Connecting to MCP server: {server_path}")
        
        async with Client(server_path) as client:
            logging.info("✅ Connected to MCP server!")
            
            # Test with health check
            logging.info("\n🩺 Testing with health check...")
            try:
                health_result = await client.call_tool("health", {})
                result_data = extract_result_data(health_result)
                logging.info(format_result("health", result_data))
            except Exception as e:
                logging.error(f"⚠️  Health check failed: {e}")
                logging.error(f"Health check error: {e}", exc_info=True)
            
            # Discover tools
            logging.info("\n🔍 Discovering available tools...")
            try:
                tools = await client.list_tools()
                if tools.tools:
                    logging.info(f"✅ Found {len(tools.tools)} tools:")
                    for tool in tools.tools:
                        logging.info(f"   • {tool.name}: {tool.description}")
                else:
                    logging.error("⚠️  No tools discovered")
            except Exception as e:
                logging.error(f"⚠️  Tool discovery failed: {e}")
                tools = None
            
            # Discover resources
            logging.info("\n📚 Discovering available resources...")
            try:
                resources = await client.list_resources()
                if resources.resources:
                    logging.info(f"✅ Found {len(resources.resources)} resources:")
                    for resource in resources.resources:
                        logging.info(f"   • {resource.uri}: {resource.description}")
                else:
                    logging.error("⚠️  No resources discovered")
            except Exception as e:
                logging.error(f"⚠️  Resource discovery failed: {e}")
            
            print(f"\n{'='*60}")
            print("🎯 Interactive Demo Started!")
            print("\n📝 Try these example queries:")
            print("   • 'What is 15 plus 27?'")
            print("   • 'Calculate 100 divided by 4'")
            print("   • 'Get AAPL stock price'")
            print("   • 'TSLA quote'")
            print("   • 'echo Hello World'")
            print("   • 'health check'")
            print("\n💡 Commands:")
            print("   • 'tools' - List available tools")
            print("   • 'resources' - List available resources")
            print("   • 'exit' - Quit the demo")
            print(f"{'='*60}")
            
            parser = QueryParser()
            
            while True:
                try:
                    user_input = input("\n💬 Your query: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() == 'exit':
                        logging.info("👋 Goodbye!")
                        break
                    
                    if user_input.lower() == 'tools':
                        if tools and tools.tools:
                            logging.info("\n🔧 Available tools:")
                            for tool in tools.tools:
                                logging.info(f"   • {tool.name}: {tool.description}")
                        else:
                            logging.info("\n🔧 Known tools: calculator, stock_quote, health, echo")
                        continue
                    
                    if user_input.lower() == 'resources':
                        try:
                            resources = await client.list_resources()
                            if resources.resources:
                                logging.info("\n📚 Available resources:")
                                for resource in resources.resources:
                                    logging.info(f"   • {resource.uri}: {resource.description}")
                            else:
                                logging.info("\n📚 No resources available")
                        except Exception as e:
                            logging.error(f"\n❌ Could not list resources: {e}")
                        continue
                    
                    # Parse the query
                    parsed_query = parser.parse_query(user_input)
                    
                    if not parsed_query:
                        logging.warning("❓ I couldn't understand your query. Try rephrasing or check the examples above.")
                        continue
                    
                    # Execute the tool call
                    tool_name = parsed_query["tool"]
                    parameters = parsed_query["params"]
                    
                    logging.info(f"🔧 Calling tool: {tool_name}")
                    if parameters:
                        logging.info(f"📝 Parameters: {json.dumps(parameters, indent=2)}")
                    
                    try:
                        result = await client.call_tool(tool_name, parameters)
                        result_data = extract_result_data(result)
                        logging.info(format_result(tool_name, result_data))
                            
                    except Exception as e:
                        logging.error(f"❌ Error calling tool: {e}")
                        logging.error(f"Tool call error: {e}", exc_info=True)
                
                except KeyboardInterrupt:
                    logging.info("\n\n👋 Goodbye!")
                    break
                except Exception as e:
                    logging.error(f"Unexpected error: {e}", exc_info=True)
                    logging.error(f"❌ Unexpected error: {e}")
                    
    except Exception as e:
        logging.error(f"❌ Failed to connect to server: {e}")
        logging.error("\nMake sure the server file exists and FastMCP is installed:")
        logging.error("  pip install fastmcp yfinance")
        logging.error(f"  Ensure {server_path} exists in the current directory")

def main():
    """Run the async demo"""
    asyncio.run(run_demo())

if __name__ == '__main__':
    main()