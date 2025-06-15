import asyncio
import json
import logging
import os
from typing import Dict, List, Any, Optional
from fastmcp import Client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# LLM Integration Options - Choose one:
# Option 1: OpenAI API
# Option 2: Anthropic Claude API  
# Option 3: Local LLM via Ollama
# Option 4: Google Gemini API
# Option 5: AWS Bedrock Claude 3.5

LLM_MODELS = ["openai", "anthropic", "ollama", "gemini",  "bedrock"]
LLM_PROVIDER = "gemini"

# --- LLM Query Parser ---
class LLMQueryParser:
    """Use LLM to parse natural language queries into tool calls"""
    
    def __init__(self, provider: str = "ollama"):
        self.provider = provider
        self.setup_llm_client()
    
    def setup_llm_client(self):
        """Setup the appropriate LLM client based on provider"""
        if self.provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                logging.info("✅ OpenAI client initialized")
            except ImportError:
                logging.error("❌ OpenAI library not installed. Run: pip install openai")
                self.client = None
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                logging.info("✅ Anthropic client initialized")
            except ImportError:
                logging.error("❌ Anthropic library not installed. Run: pip install anthropic")
                self.client = None
        
        elif self.provider == "ollama":
            try:
                import requests
                # Test if Ollama is running
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code == 200:
                    logging.info("✅ Ollama server detected")
                    self.client = "ollama"  # Use string indicator
                else:
                    logging.error("❌ Ollama server not responding")
                    self.client = None
            except Exception as e:
                logging.error(f"❌ Ollama connection failed: {e}")
                logging.error("Make sure Ollama is installed and running: https://ollama.ai")
                self.client = None
        
        elif self.provider == "gemini":
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key:
                    genai.configure(api_key=api_key)
                    # https://ai.google.dev/gemini-api/docs/models
                    gemini_models = [
                            "gemini-2.5-flash-preview-05-20",
                            "gemini-2.5-pro-preview-05-06",
                            "gemini-2.0-flash",
                            "gemini-1.5-flash",
                            "gemini-1.5-pro",
                        ]
                    model_name = gemini_models[3]
                    self.client = genai.GenerativeModel(model_name)
                    logging.info("✅ Gemini client initialized")
                else:
                    logging.error("❌ GEMINI_API_KEY not set")
                    self.client = None
            except ImportError:
                logging.error("❌ Gemini library not installed. Run: pip install google-generativeai")
                self.client = None
        
        elif self.provider == "bedrock":
            try:
                import boto3
                from botocore.exceptions import NoCredentialsError, PartialCredentialsError
                
                # Initialize Bedrock client
                # AWS credentials should be configured via:
                # 1. AWS CLI: aws configure
                # 2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
                # 3. IAM roles (if running on EC2)
                # 4. AWS SSO
                
                region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
                
                try:
                    self.client = boto3.client(
                        service_name='bedrock-runtime',
                        region_name=region
                    )
                    
                    # Test connection with a simple call
                    # Note: We'll test this during the first actual query to avoid unnecessary calls
                    self.bedrock_model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"  # Claude 3.5 Sonnet
                    logging.info(f"✅ AWS Bedrock client initialized (region: {region})")
                    logging.info(f"📋 Using model: {self.bedrock_model_id}")
                    
                except (NoCredentialsError, PartialCredentialsError) as e:
                    logging.error(f"❌ AWS credentials not configured: {e}")
                    logging.error("Configure AWS credentials using one of these methods:")
                    logging.error("  1. AWS CLI: aws configure")
                    logging.error("  2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
                    logging.error("  3. IAM roles (if running on AWS)")
                    self.client = None
                    
            except ImportError:
                logging.error("❌ Boto3 library not installed. Run: pip install boto3")
                self.client = None
    
    def get_system_prompt(self, available_tools: List[Dict]) -> str:
        """Create system prompt with available tools"""
        tools_desc = "\n".join([
            f"- {tool['name']}: {tool.get('description', 'No description')}"
            for tool in available_tools
        ])
        
        return f"""You are a tool selection assistant. Given a user query, you must decide which tool to use and extract the necessary parameters.

Available tools:
{tools_desc}

For each user query, respond with ONLY a JSON object in this exact format:
{{
    "tool": "tool_name",
    "params": {{
        "param1": "value1",
        "param2": "value2"
    }},
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this tool was chosen"
}}

Tool-specific parameter requirements:
- calculator: operation (add/subtract/multiply/divide), num1 (number), num2 (number)
- trig: operation (sine/cosine/tangent), theta (float)
- stock_quote: ticker (stock symbol like AAPL, MSFT)
- health: no parameters needed
- echo: message (text to echo back)

If you cannot determine which tool to use or extract parameters, respond with:
{{
    "tool": null,
    "params": {{}},
    "confidence": 0.0,
    "reasoning": "Could not parse the query"
}}

Examples:
User: "What is 15 plus 27?"
Response: {{"tool": "calculator", "params": {{"operation": "add", "num1": 15, "num2": 27}}, "confidence": 0.98, "reasoning": "Clear arithmetic addition request"}}

User: "What is sine 30 degrees?"
Response: {{"tool": "trig", "params": {{"operation": "sine", "theta": 30}}, "confidence": 0.98, "reasoning": "Clear trigonometic sine function request"}}

User: "Get Apple stock price"
Response: {{"tool": "stock_quote", "params": {{"ticker": "AAPL"}}, "confidence": 0.95, "reasoning": "Request for Apple (AAPL) stock information"}}

User: "echo hello world"
Response: {{"tool": "echo", "params": {{"message": "hello world"}}, "confidence": 0.99, "reasoning": "Direct echo command"}}

User: "server status"
Response: {{"tool": "health", "params": {{}}, "confidence": 0.90, "reasoning": "Request for server health information"}}

Remember: Respond with ONLY the JSON object, no additional text."""

    async def parse_query_with_llm(self, query: str, available_tools: List[Dict]) -> Optional[Dict[str, Any]]:
        """Use LLM to parse the query"""
        if not self.client:
            logging.error("❌ LLM client not available, falling back to rule-based parsing")
            return None
        
        system_prompt = self.get_system_prompt(available_tools)
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                llm_response = response.choices[0].message.content.strip()
            
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=200,
                    temperature=0.1,
                    system=system_prompt,
                    messages=[{"role": "user", "content": query}]
                )
                llm_response = response.content[0].text.strip()
            
            elif self.provider == "ollama":
                import requests
                payload = {
                    "model": "llama3.2",  # or "mistral", "codellama", etc.
                    "prompt": f"{system_prompt}\n\nUser: {query}\nResponse:",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 200
                    }
                }
                response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
                if response.status_code == 200:
                    llm_response = response.json()["response"].strip()
                else:
                    logging.error(f"Ollama API error: {response.status_code}")
                    return None
            
            elif self.provider == "gemini":
                response = self.client.generate_content(
                    f"{system_prompt}\n\nUser: {query}",
                    generation_config={
                        "temperature": 0.1,
                        "max_output_tokens": 200
                    }
                )
                llm_response = response.text.strip()
            
            elif self.provider == "bedrock":
                import json as json_lib
                
                # Construct the request for Claude 3.5 Sonnet
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 200,
                    "temperature": 0.1,
                    "system": system_prompt,
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                }
                
                # Make the request to Bedrock
                response = self.client.invoke_model(
                    modelId=self.bedrock_model_id,
                    body=json_lib.dumps(request_body),
                    contentType="application/json",
                    accept="application/json"
                )
                
                # Parse the response
                response_body = json_lib.loads(response['body'].read())
                llm_response = response_body['content'][0]['text'].strip()
                
                logging.debug(f"Bedrock response usage: {response_body.get('usage', {})}")
            
            # Parse the JSON response
            logging.debug(f"LLM Response: {llm_response}")
            
            # Clean up the response - sometimes LLMs add extra text
            if llm_response.startswith("```json"):
                llm_response = llm_response.replace("```json", "").replace("```", "").strip()
            
            parsed_response = json.loads(llm_response)
            
            # Validate the response structure
            if not isinstance(parsed_response, dict):
                logging.error("LLM response is not a dictionary")
                return None
            
            if parsed_response.get("tool") is None:
                logging.warning(f"LLM could not parse query: {parsed_response.get('reasoning', 'Unknown reason')}")
                return None
            
            confidence = parsed_response.get("confidence", 0.0)
            if confidence < 0.5:
                logging.warning(f"Low confidence ({confidence}) in LLM parsing: {parsed_response.get('reasoning')}")
                return None
            
            logging.info(f"🤖 LLM parsed query: {parsed_response.get('reasoning')} (confidence: {confidence})")
            
            return {
                "tool": parsed_response["tool"],
                "params": parsed_response.get("params", {}),
                "confidence": confidence,
                "reasoning": parsed_response.get("reasoning", "")
            }
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse LLM JSON response: {e}")
            logging.error(f"Raw LLM response: {llm_response}")
            return None
        except Exception as e:
            logging.error(f"LLM query parsing error: {e}")
            return None

# --- Fallback Rule-Based Parser (same as before) ---
class RuleBasedQueryParser:
    """Fallback rule-based query parser"""
    
    @staticmethod
    def parse_calculator_query(query: str) -> Optional[Dict[str, Any]]:
        import re
        query = query.lower().strip()
        patterns = [
            ("add", ["plus", "add", "+", "sum"]),
            ("subtract", ["minus", "subtract", "-", "difference"]),
            ("multiply", ["times", "multiply", "*", "×", "product"]),
            ("divide", ["divide", "divided by", "/", "÷"]),
        ]
        
        for operation, keywords in patterns:
            for keyword in keywords:
                if keyword in query:
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
        import re
        query_lower = query.lower().strip()
        stock_keywords = ["stock", "price", "quote", "ticker", "share"]
        
        if any(keyword in query_lower for keyword in stock_keywords):
            tickers = re.findall(r'\b[A-Z]{2,5}\b', query.upper())
            if tickers:
                excluded_words = {"GET", "THE", "FOR", "AND", "BUT", "NOT", "YOU", "ALL", "CAN"}
                valid_tickers = [t for t in tickers if t not in excluded_words]
                if valid_tickers:
                    return {
                        "tool": "stock_quote", 
                        "params": {"ticker": valid_tickers[0]}
                    }
        
        common_tickers = ["AAPL", "GOOGL", "GOOG", "MSFT", "TSLA", "AMZN", "META", "NVDA"]
        for ticker in common_tickers:
            if ticker in query.upper():
                return {
                    "tool": "stock_quote",
                    "params": {"ticker": ticker}
                }
        return None
    
    @staticmethod
    def parse_query(query: str) -> Optional[Dict[str, Any]]:
        if any(word in query.lower() for word in ["health", "status", "ping"]):
            return {"tool": "health", "params": {}}
        
        if query.lower().startswith("echo "):
            message = query[5:].strip()
            return {"tool": "echo", "params": {"message": message}}
        
        calc_result = RuleBasedQueryParser.parse_calculator_query(query)
        if calc_result:
            return calc_result
        
        stock_result = RuleBasedQueryParser.parse_stock_query(query)
        if stock_result:
            return stock_result
        
        return None

# --- Same extraction and formatting functions as before ---
def extract_result_data(result):
    """Extract actual data from FastMCP result object"""
    try:
        if isinstance(result, list) and len(result) > 0:
            content_item = result[0]
            if hasattr(content_item, 'text'):
                try:
                    return json.loads(content_item.text)
                except json.JSONDecodeError:
                    return {"text": content_item.text}
            else:
                return {"content": str(content_item)}
        elif hasattr(result, 'content') and result.content:
            content_item = result.content[0]
            if hasattr(content_item, 'text'):
                try:
                    return json.loads(content_item.text)
                except json.JSONDecodeError:
                    return {"text": content_item.text}
            else:
                return {"content": str(content_item)}
        else:
            if isinstance(result, dict):
                return result
            else:
                return {"result": str(result)}
    except Exception as e:
        logging.error(f"Error extracting result data: {e}")
        return {"error": f"Could not parse result: {e}"}

def format_result(tool_name: str, result: Dict) -> str:
    """Format tool results for display"""
    if isinstance(result, dict) and "error" in result:
        return f"❌ Error: {result['error']}"
    
    if tool_name == "calculator":
        if "result" in result:
            expression = result.get('expression')
            if expression:
                return f"🧮 {expression}"
            else:
                num1 = result.get('num1', '?')
                num2 = result.get('num2', '?')
                operation = result.get('operation', '?')
                calc_result = result.get('result', '?')
                return f"🧮 {num1} {operation} {num2} = {calc_result}"
        elif "error" in result:
            return f"❌ Calculator Error: {result['error']}"
    
    elif tool_name == "stock_quote":
        if "current_price" in result:
            ticker = result.get('ticker', 'Unknown')
            name = result.get('company_name', ticker)
            price = result.get('current_price', 0)
            currency = result.get('currency', 'USD')
            extra_info = []
            if result.get('volume'):
                extra_info.append(f"Vol: {result['volume']:,}")
            if result.get('day_high') and result.get('day_low'):
                extra_info.append(f"Range: {result['day_low']}-{result['day_high']}")
            extra = f" ({', '.join(extra_info)})" if extra_info else ""
            return f"📈 {name} ({ticker}): {currency} {price}{extra}"
        elif "error" in result:
            return f"❌ Stock Error: {result['error']}"
    
    elif tool_name == "health":
        if isinstance(result, dict):
            return f"✅ {result.get('message', 'Server is healthy')}"
    
    elif tool_name == "echo":
        if isinstance(result, dict):
            return f"🔊 {result.get('echo', result.get('message', str(result)))}"
    
    try:
        return f"✅ Result: {json.dumps(result, indent=2)}"
    except (TypeError, ValueError):
        return f"✅ Result: {str(result)}"

# --- Main Demo with LLM Integration ---
async def run_llm_demo():
    print("🚀 LLM-powered MCP client demo starting...")
    print(f"🤖 Using LLM Provider: {LLM_PROVIDER}")
    
    # Initialize parsers
    llm_parser = LLMQueryParser(LLM_PROVIDER)
    fallback_parser = RuleBasedQueryParser()
    
    server_path = "mcp_server.py"
    
    try:
        print(f"📡 Connecting to MCP server: {server_path}")
        
        async with Client(server_path) as client:
            print("✅ Connected to MCP server (local)!")
            
            # Discover available tools for LLM context
            available_tools = []
            try:
                tools = await client.list_tools()
                # print(f"tools: {tools}")
                if tools:
                    available_tools = [
                        {"name": tool.name, "description": tool.description} for tool in tools
                    ]
                    print(f"✅ Found {len(available_tools)} tools for LLM context")
                else:
                    # Fallback tool definitions
                    available_tools = [
                        {"name": "calculator", "description": "Perform arithmetic operations"},
                        {"name": "trig", "description": "Performs trigonometric operation on an angle in degree"},
                        {"name": "stock_quote", "description": "Get stock price data"},
                        {"name": "health", "description": "Check server health"},
                        {"name": "echo", "description": "Echo back messages"}
                    ]
            except Exception as e:
                logging.error(f"Tool discovery failed: {e}")
            
            print(f"\n{'='*60}")
            print("🎯 LLM-Powered Interactive Demo Started!")
            print("\n📝 Try natural language queries:")
            print("   • 'What's fifteen plus twenty seven?'")
            print("   • 'Can you multiply 12 by 8?'")
            print("   • 'Find sine of 30 degrees'")
            print("   • 'I need the current Apple stock price'")
            print("   • 'How much is Tesla trading for?'")
            print("   • 'Please echo back: Hello AI!'")
            print("   • 'Is the server working properly?'")
            print("\n💡 Commands:")
            print("   • 'tools' - List available tools")
            print("   • 'switch' - Switch parsing mode")
            print("   • 'exit' - Quit the demo")
            print(f"{'='*60}")
            
            use_llm = llm_parser.client is not None
            
            while True:
                try:
                    user_input = input(f"\n💬 Your query {'🤖' if use_llm else '🔧'}: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ('exit', "quit", "bye", "q"):
                        print("👋 Goodbye!")
                        break
                    
                    if user_input.lower() == 'switch':
                        use_llm = not use_llm
                        mode = "LLM" if use_llm else "Rule-based"
                        print(f"🔄 Switched to {mode} parsing mode")
                        continue
                    
                    if user_input.lower() == 'tools':
                        print("\n🔧 Available tools:")
                        for tool in available_tools:
                            print(f"   • {tool['name']}: {tool['description']}")
                        continue
                    
                    # Parse the query
                    parsed_query = None
                    
                    if use_llm and llm_parser.client:
                        parsed_query = await llm_parser.parse_query_with_llm(user_input, available_tools)
                    
                    # Fallback to rule-based if LLM fails
                    if not parsed_query:
                        if use_llm:
                            print("🔄 LLM parsing failed, trying rule-based parser...")
                        parsed_query = fallback_parser.parse_query(user_input)
                    
                    if not parsed_query:
                        print("❓ I couldn't understand your query. Try rephrasing or being more specific.")
                        continue
                    
                    # Execute the tool call
                    tool_name = parsed_query["tool"]
                    parameters = parsed_query["params"]
                    
                    print(f"🔧 Calling tool: {tool_name}")
                    if parsed_query.get("reasoning"):
                        print(f"💭 Reasoning: {parsed_query['reasoning']}")
                    if parameters:
                        print(f"📝 Parameters: {json.dumps(parameters, indent=2)}")
                    
                    try:
                        result = await client.call_tool(tool_name, parameters)
                        result_data = extract_result_data(result)
                        print(format_result(tool_name, result_data))
                            
                    except Exception as e:
                        print(f"❌ Error calling tool: {e}")
                        logging.error(f"Tool call error: {e}", exc_info=True)
                
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    break
                except Exception as e:
                    logging.error(f"Unexpected error: {e}", exc_info=True)
                    print(f"❌ Unexpected error: {e}")
                    
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        print("\nMake sure the server file exists and FastMCP is installed:")
        print("  pip install fastmcp yfinance")
        print(f"  Ensure {server_path} exists in the current directory")

def main():
    """Run the LLM-powered async demo"""
    print("🤖 LLM-Powered MCP Client")
    print("=" * 40)
    print(f"Selected LLM Provider: {LLM_PROVIDER}")
    
    if LLM_PROVIDER == "ollama":
        print("📋 Ollama Setup Instructions:")
        print("1. Install Ollama: https://ollama.ai")
        print("2. Run: ollama pull llama3.2")
        print("3. Start Ollama service")
    elif LLM_PROVIDER == "openai":
        print("📋 Set environment variable: OPENAI_API_KEY")
    elif LLM_PROVIDER == "anthropic":
        print("📋 Set environment variable: ANTHROPIC_API_KEY")
    elif LLM_PROVIDER == "gemini":
        print("📋 Set environment variable: GEMINI_API_KEY")
    elif LLM_PROVIDER == "bedrock":
        print("📋 AWS Bedrock Setup Instructions:")
        print("1. Install boto3: pip install boto3")
        print("2. Configure AWS credentials (choose one):")
        print("   • AWS CLI: aws configure")
        print("   • Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION")
        print("   • IAM roles (if running on AWS)")
        print("   • AWS SSO: aws sso login")
        print("3. Ensure you have access to Claude 3.5 Sonnet in Bedrock")
        print("4. Set AWS_DEFAULT_REGION if needed (default: us-east-1)")
    
    print("=" * 40)
    
    asyncio.run(run_llm_demo())

if __name__ == '__main__':
    main()