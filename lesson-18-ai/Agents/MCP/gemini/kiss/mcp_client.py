import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"Sending RPC request to {self.server_url}: {method}")
        try:
            response = requests.post(self.server_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Network or HTTP error: {e}")
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
            return None
        return response.get("result", {})

if __name__ == '__main__':
    MCP_SERVER_URL = "http://127.0.0.1:5000/" # No /mcp path now
    client = MCPClient(MCP_SERVER_URL)

    print("--- Discovering Tools ---")
    tools = client.get_tool_definitions()
    if tools:
        print("Discovered tools:")
        for tool_def in tools:
            print(f"  Name: {tool_def['name']}")
            print(f"  Description: {tool_def['description']}")
            print(f"  Parameters: {json.dumps(tool_def['parameters'], indent=2)}")
            print("-" * 20)
    else:
        print("No tools discovered.")

    print("\n--- Calling Calculator Tool (Addition) ---")
    tool_name_to_call = "calculator"
    params_for_call = {
        "operation": "add",
        "num1": 15.0,
        "num2": 7.0
    }

    result = client.call_tool(tool_name_to_call, params_for_call)

    if result is not None:
        print(f"Result of calling '{tool_name_to_call}' with {params_for_call}:")
        print(f"  Value: {result.get('value')}")
    else:
        print("Failed to get a result from the tool call.")

    print("\n--- Calling Calculator Tool with Invalid Operation ---")
    invalid_params = {
        "operation": "subtract",
        "num1": 10.0,
        "num2": 5.0
    }
    client.call_tool(tool_name_to_call, invalid_params)