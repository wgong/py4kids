import requests
import json
import logging
import google.generativeai as genai
import os # For environment variable if preferred for API key

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# IMPORTANT: Replace with your actual Google Gemini API key
# It's recommended to load this from an environment variable in production
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
    logging.warning("GEMINI_API_KEY not set. Please replace 'YOUR_GEMINI_API_KEY' in the script or set the environment variable.")
    # For demonstration, we'll proceed, but it will fail if the key is invalid.

genai.configure(api_key=GEMINI_API_KEY)

MCP_SERVER_URL = "http://127.0.0.1:5000/mcp" # fastmcp default endpoint

# --- MCP Client Class ---
class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def _send_rpc_request(self, method: str, params: dict, request_id: int = 1):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }
        logging.info(f"Sending RPC request to {self.server_url}: Method='{method}', ID='{request_id}'")
        try:
            response = requests.post(self.server_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Network or HTTP error when sending RPC request: {e}")
            return {"error": {"code": -32000, "message": f"Network Error: {e}"}}

    def get_tool_definitions(self):
        """Fetches all available tool definitions from the MCP server."""
        response = self._send_rpc_request("Context.get_tool_definitions", {})
        if "error" in response:
            logging.error(f"Error fetching tool definitions: {response['error']}")
            return []
        return response.get("result", {}).get("tool_definitions", [])

    def call_tool(self, tool_name: str, parameters: dict):
        """Calls a specific tool on the MCP server."""
        response = self._send_rpc_request("Context.call_tool", {
            "tool_name": tool_name,
            "parameters": parameters
        })
        if "error" in response:
            logging.error(f"Error calling tool '{tool_name}': {response['error']}")
            return {"error": response["error"]} # Return error for handling
        return response.get("result", {})

# --- Gemini Integration Functions ---

def get_gemini_tool_output(user_query: str, tools_for_gemini: list):
    """
    Uses Google Gemini to process a user query and output a tool call if applicable.
    """
    model = genai.GenerativeModel(
        model_name="gemini-pro", # Or "gemini-1.5-flash", "gemini-1.5-pro" etc., depending on access
        tools=tools_for_gemini,
        tool_config={"function_calling_config": "AUTO"} # Auto-select tools
    )

    chat = model.start_chat()
    try:
        response = chat.send_message(user_query)
        # Check if the response contains tool_calls
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    tool_call = part.function_call
                    logging.info(f"Gemini identified a tool call: {tool_call.name} with args {tool_call.args}")
                    return tool_call
        else:
            logging.info(f"Gemini did not identify a tool call. Raw response: {response.text}")
            return {"text_response": response.text} # Return text response if no tool call
    except Exception as e:
        logging.error(f"Error sending message to Gemini or parsing response: {e}", exc_info=True)
        return {"error": f"Gemini API error: {e}"}


def format_for_mcp(gemini_tool_call_obj):
    """
    Translates a Gemini FunctionCall object into an MCP Context.call_tool request structure.
    """
    if not gemini_tool_call_obj:
        return None

    # MCP expects 'tool_name' and 'parameters'
    mcp_call_params = {
        "tool_name": gemini_tool_call_obj.name,
        "parameters": dict(gemini_tool_call_obj.args) # Convert A.A.Map to dict
    }

    # The full JSON-RPC 2.0 structure for Context.call_tool
    mcp_request = {
        "jsonrpc": "2.0",
        "method": "Context.call_tool",
        "params": mcp_call_params,
        "id": 1 # A simple request ID, you might generate unique IDs in production
    }
    return mcp_request

# --- Main Execution Loop ---
if __name__ == '__main__':
    client = MCPClient(MCP_SERVER_URL)

    print("--- Discovering Tools from MCP Server ---")
    mcp_tool_defs = client.get_tool_definitions()

    if not mcp_tool_defs:
        print("Failed to discover tools from MCP server. Ensure the server is running.")
        exit()

    print("Discovered tools:")
    for tool_def in mcp_tool_defs:
        print(f"  Name: {tool_def['name']}")
        print(f"  Description: {tool_def['description']}")
        print(f"  Parameters: {json.dumps(tool_def['parameters'], indent=2)}")
        print("-" * 20)

    # Prepare tool definitions for Gemini (should match the structure Gemini expects)
    # Gemini's `tools` argument expects a list of dictionaries, where each dict has
    # 'name', 'description', and 'parameters' (which is a JSON schema object).
    tools_for_gemini = [
        {
            "name": t_def["name"],
            "description": t_def["description"],
            "parameters": t_def["parameters"]
        }
        for t_def in mcp_tool_defs
    ]

    print("\n--- Starting Interactive Demo ---")
    print("Type your queries (e.g., 'What is 10 plus 5?', 'Get stock quote for GOOG'), or 'exit' to quit.")

    while True:
        user_input = input("\nYour query: ")
        if user_input.lower() == 'exit':
            break

        gemini_response = get_gemini_tool_output(user_input, tools_for_gemini)

        if "error" in gemini_response:
            print(f"  Error from Gemini: {gemini_response['error']}")
            continue
        elif "text_response" in gemini_response:
            print(f"  Gemini's text response: {gemini_response['text_response']}")
            continue

        # If Gemini returned a tool call
        mcp_tool_request = format_for_mcp(gemini_response)

        if mcp_tool_request:
            print(f"  -> Gemini detected a tool call: {mcp_tool_request['params']['tool_name']}")
            print(f"  -> Formatted MCP Request (JSON-RPC 2.0):\n{json.dumps(mcp_tool_request, indent=2)}")

            # Send the MCP request to the fastmcp server
            tool_execution_result = client.call_tool(
                mcp_tool_request['params']['tool_name'],
                mcp_tool_request['params']['parameters']
            )

            if "error" in tool_execution_result:
                print(f"  !!! Error executing tool '{mcp_tool_request['params']['tool_name']}': {tool_execution_result['error']['message']}")
            else:
                print(f"  -> Tool execution successful! Result: {json.dumps(tool_execution_result, indent=2)}")
        else:
            print("  -> Gemini did not detect a relevant tool call for this query.")