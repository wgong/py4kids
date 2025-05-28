import requests
import json
import logging
import os
import time
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
MCP_SERVER_URL = "http://127.0.0.1:5000/mcp"

# Optional: Google Gemini integration (comment out if not using)
USE_GEMINI = True # False  # Set to True if you want to use Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if USE_GEMINI and GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
    except ImportError:
        logging.warning("google-generativeai not installed. Install with: pip install google-generativeai")
        USE_GEMINI = False
elif USE_GEMINI:
    logging.warning("GEMINI_API_KEY not set. Disabling Gemini integration.")
    USE_GEMINI = False

# --- MCP Client Class ---
class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()
        self.request_id = 1
    
    def _get_request_id(self) -> int:
        """Generate unique request IDs"""
        current_id = self.request_id
        self.request_id += 1
        return current_id
    
    def _send_rpc_request(self, method: str, params: dict) -> dict:
        """Send JSON-RPC 2.0 request to MCP server"""
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._get_request_id()
        }
        
        logging.info(f"Sending RPC request: Method='{method}'")
        logging.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(
                self.server_url, 
                headers=headers, 
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logging.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return {"error": {"code": -32000, "message": f"Network Error: {e}"}}
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return {"error": {"code": -32700, "message": f"Parse Error: {e}"}}

    def test_connection(self) -> bool:
        """Test if the MCP server is accessible"""
        try:
            response = self.session.get(self.server_url.replace('/mcp', ''), timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools from the MCP server"""
        response = self._send_rpc_request("tools/list", {})
        
        if "error" in response:
            logging.error(f"Error listing tools: {response['error']}")
            return []
        
        tools = response.get("result", {}).get("tools", [])
        return tools

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a specific tool on the MCP server"""
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        
        response = self._send_rpc_request("tools/call", params)
        
        if "error" in response:
            logging.error(f"Error calling tool '{tool_name}': {response['error']}")
            return {"error": response["error"]}
        
        return response.get("result", {})

# --- Simple Query Parser (Alternative to Gemini) ---
class SimpleQueryParser:
    """Simple rule-based query parser for demo purposes"""
    
    @staticmethod
    def parse_calculator_query(query: str) -> Optional[Dict[str, Any]]:
        """Parse basic math queries"""
        query = query.lower().strip()
        
        # Simple patterns for math operations
        patterns = [
            ("add", ["plus", "add", "+"]),
            ("subtract", ["minus", "subtract", "-"]),
            ("multiply", ["times", "multiply", "*", "×"]),
            ("divide", ["divide", "divided by", "/"]),
        ]
        
        for operation, keywords in patterns:
            for keyword in keywords:
                if keyword in query:
                    # Extract numbers (very basic extraction)
                    import re
                    numbers = re.findall(r'-?\d+(?:\.\d+)?', query)
                    if len(numbers) >= 2:
                        try:
                            return {
                                "tool": "calculator_tool",
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
        query = query.lower().strip()
        
        stock_keywords = ["stock", "price", "quote", "ticker"]
        if any(keyword in query for keyword in stock_keywords):
            # Extract potential ticker symbols (3-4 uppercase letters)
            import re
            tickers = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
            if tickers:
                return {
                    "tool": "yahoo_finance_tool",
                    "params": {
                        "ticker": tickers[0]
                    }
                }
        return None
    
    @staticmethod
    def parse_query(query: str) -> Optional[Dict[str, Any]]:
        """Parse user query and return tool call if applicable"""
        # Try calculator first
        calc_result = SimpleQueryParser.parse_calculator_query(query)
        if calc_result:
            return calc_result
        
        # Try stock query
        stock_result = SimpleQueryParser.parse_stock_query(query)
        if stock_result:
            return stock_result
        
        return None

# --- Gemini Integration (Optional) ---
def parse_query_with_gemini(query: str, available_tools: List[Dict]) -> Optional[Dict[str, Any]]:
    """Use Gemini to parse queries and suggest tool calls"""
    if not USE_GEMINI:
        return None
    
    try:
        # Convert MCP tool format to Gemini format
        gemini_tools = []
        for tool in available_tools:
            gemini_tool = {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get("inputSchema", {})
            }
            gemini_tools.append(gemini_tool)
        
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            tools=gemini_tools,
            tool_config={"function_calling_config": "AUTO"}
        )
        
        chat = model.start_chat()
        response = chat.send_message(query)
        
        # Check for function calls
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    tool_call = part.function_call
                    return {
                        "tool": tool_call.name,
                        "params": dict(tool_call.args)
                    }
        
        return None
        
    except Exception as e:
        logging.error(f"Gemini parsing error: {e}")
        return None

# --- Main Demo Function ---
def run_demo():
    """Run the interactive MCP demo"""
    client = MCPClient(MCP_SERVER_URL)
    
    print("🚀 MCP Client Demo Starting...")
    
    # Test connection
    print("📡 Testing connection to MCP server...")
    if not client.test_connection():
        print("❌ Cannot connect to MCP server.")
        print(f"   Make sure the server is running at {MCP_SERVER_URL}")
        print("   Start the server with: python mcp_server.py")
        return
    
    print("✅ Connected to MCP server!")
    
    # Discover available tools
    print("\n🔍 Discovering available tools...")
    available_tools = client.list_tools()
    
    if not available_tools:
        print("❌ No tools found. Check server implementation.")
        return
    
    print(f"✅ Found {len(available_tools)} tools:")
    for tool in available_tools:
        print(f"   • {tool['name']}: {tool.get('description', 'No description')}")
    
    # Test health check if available
    health_tools = [t for t in available_tools if 'health' in t['name'].lower()]
    if health_tools:
        print(f"\n🩺 Testing health check...")
        result = client.call_tool(health_tools[0]['name'], {})
        if "error" not in result:
            print(f"✅ Health check passed: {result}")
    
    print(f"\n{'='*50}")
    print("🎯 Interactive Demo Started!")
    print("Try these example queries:")
    print("  • 'What is 15 plus 27?'")
    print("  • 'Calculate 100 minus 25'") 
    print("  • 'Get stock quote for AAPL'")
    print("  • 'GOOGL stock price'")
    print("  • Type 'tools' to list available tools")
    print("  • Type 'exit' to quit")
    print(f"{'='*50}")
    
    parser = SimpleQueryParser()
    
    while True:
        try:
            user_input = input("\n💬 Your query: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'tools':
                print("\n🔧 Available tools:")
                for tool in available_tools:
                    print(f"   • {tool['name']}: {tool.get('description', 'No description')}")
                continue
            
            # Try to parse the query
            parsed_query = None
            
            # Try Gemini first if available
            if USE_GEMINI:
                print("🤖 Parsing query with Gemini...")
                parsed_query = parse_query_with_gemini(user_input, available_tools)
            
            # Fall back to simple parser
            if not parsed_query:
                print("🔍 Parsing query with simple parser...")
                parsed_query = parser.parse_query(user_input)
            
            if not parsed_query:
                print("❓ I couldn't understand your query. Try rephrasing or check the examples above.")
                continue
            
            # Execute the tool call
            tool_name = parsed_query["tool"]
            parameters = parsed_query["params"]
            
            print(f"🔧 Calling tool: {tool_name}")
            print(f"📝 Parameters: {json.dumps(parameters, indent=2)}")
            
            result = client.call_tool(tool_name, parameters)
            
            if "error" in result:
                print(f"❌ Error: {result['error']['message']}")
            else:
                print(f"✅ Result: {json.dumps(result, indent=2)}")
                
                # Pretty print common results
                if tool_name == "calculator_tool" and "content" in result:
                    for content_item in result["content"]:
                        if content_item["type"] == "text":
                            try:
                                calc_result = json.loads(content_item["text"])
                                if "value" in calc_result:
                                    print(f"🧮 Answer: {calc_result['value']}")
                            except:
                                pass
                
                elif tool_name == "yahoo_finance_tool" and "content" in result:
                    for content_item in result["content"]:
                        if content_item["type"] == "text":
                            try:
                                stock_result = json.loads(content_item["text"])
                                if stock_result.get("current_price"):
                                    print(f"📈 {stock_result.get('long_name', stock_result['ticker'])}: ${stock_result['current_price']:.2f} {stock_result.get('currency', '')}")
                                elif stock_result.get("error"):
                                    print(f"❌ Stock Error: {stock_result['error']}")
                            except:
                                pass
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
            print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    run_demo()