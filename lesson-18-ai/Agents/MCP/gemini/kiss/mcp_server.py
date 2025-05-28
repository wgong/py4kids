import http.server
import socketserver
import json
import logging

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PORT = 5000

# --- Mock Calculator Tool ---
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

# --- MCP Tool Definition ---
# This is how the tool is described to MCP clients
CALCULATOR_TOOL_DEFINITION = {
    "name": "calculator",
    "description": "A simple calculator tool that can perform arithmetic operations.",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add"], # We only support 'add' for this demo
                "description": "The arithmetic operation to perform."
            },
            "num1": {
                "type": "number",
                "description": "The first number."
            },
            "num2": {
                "type": "number",
                "description": "The second number."
            }
        },
        "required": ["operation", "num1", "num2"]
    }
}

class MCPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, content, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)

        try:
            rpc_request = json.loads(post_body)
            method = rpc_request.get('method')
            params = rpc_request.get('params', {})
            request_id = rpc_request.get('id')

            logging.info(f"Received RPC request: Method='{method}', ID='{request_id}'")

            if method == "Context.get_tool_definitions":
                # Respond with available tool definitions
                result = {"tool_definitions": [CALCULATOR_TOOL_DEFINITION]}
                self._send_response({"jsonrpc": "2.0", "result": result, "id": request_id})

            elif method == "Context.call_tool":
                tool_name = params.get('tool_name')
                tool_parameters = params.get('parameters', {})

                logging.info(f"Calling tool: {tool_name} with params: {tool_parameters}")

                if tool_name == "calculator":
                    operation = tool_parameters.get('operation')
                    num1 = tool_parameters.get('num1')
                    num2 = tool_parameters.get('num2')

                    if operation == "add":
                        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
                            calculated_result = add_numbers(num1, num2)
                            logging.info(f"Calculation result: {calculated_result}")
                            self._send_response({"jsonrpc": "2.0", "result": {"value": calculated_result}, "id": request_id})
                        else:
                            raise ValueError("Invalid number types for addition.")
                    else:
                        raise ValueError(f"Unsupported operation: {operation}")
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

            else:
                raise ValueError(f"Unknown MCP method: {method}")

        except json.JSONDecodeError:
            logging.error("Invalid JSON in request body.")
            self._send_response({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}}, 400)
        except Exception as e:
            logging.error(f"MCP server error: {e}", exc_info=True)
            # Use the request_id if available, otherwise None
            err_id = rpc_request.get('id') if 'rpc_request' in locals() and rpc_request else None
            self._send_response({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": err_id}, 500)

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MCPRequestHandler) as httpd:
        logging.info(f"Serving MCP Calculator Server on http://127.0.0.1:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("Server shutting down.")
            httpd.shutdown()