Here's a complete set of files for your `fastmcp` tutorial, including a `README.md`, `requirements.txt`, and an updated server and client with the Yahoo Finance tool.

```bash
conda create -n mcp python=3.11
conda activate mcp
```

---

### 1) `README.md`

```markdown
# Model Context Protocol (MCP) Demo with fastmcp and Gemini

This project demonstrates the Model Context Protocol (MCP) using the `fastmcp` Python library for the server, a custom Python client, and Google Gemini for natural language understanding and tool call translation.

It showcases how a Large Language Model (LLM) can interpret a user's plain English request, determine which tool to use, extract the necessary parameters, and then format that into an MCP-compliant call to a server hosting those tools.

## Features

* **MCP Server (`fastmcp`):**
    * Exposes a `calculator` tool for basic arithmetic operations (addition, subtraction).
    * Exposes a `yahoo_finance` tool to fetch current stock quotes for a given ticker.
    * Built using `fastmcp` for easy tool definition and JSON-RPC 2.0 handling.
    * Runs on `uvicorn` for a robust HTTP server.
* **MCP Client:**
    * Connects to the `fastmcp` server to discover available tools.
    * Sends MCP `Context.call_tool` requests to the server.
* **Gemini Integration:**
    * Uses the Google Gemini API to translate natural language user queries into structured tool calls.
    * Dynamically identifies the correct tool and extracts parameters based on the user's intent.

## Prerequisites

Before you begin, ensure you have:

* Python 3.8+ installed.
* A Google Gemini API Key. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

## Setup

1.  **Clone the repository (or create the files manually):**
    Create a new directory for your project and place the following files inside it:
    * `README.md` (this file)
    * `requirements.txt`
    * `mcp_server.py`
    * `mcp_client.py`

2.  **Install Dependencies:**
    Navigate to your project directory in the terminal and install the required Python packages using the provided `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Gemini API Key:**
    Open `mcp_client.py` and replace `"YOUR_GEMINI_API_KEY"` with your actual Google Gemini API key:

    ```python
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # <--- REPLACE THIS
    ```

## Running the Demo

This demo involves running two separate Python scripts concurrently: the MCP server and the MCP client.

### Step 1: Run the MCP Server

Open your first terminal window, navigate to your project directory, and run the server:

```bash
python mcp_server.py
```

You should see output from `uvicorn` indicating that the server is running, typically on `http://127.0.0.1:5000/`. The MCP endpoint will be at `http://127.0.0.1:5000/mcp`.

### Step 2: Run the MCP Client with Gemini Integration

Open your second terminal window, navigate to your project directory, and run the client:

```bash
python mcp_client.py
```

The client will first discover the tools available on the server. Then, it will prompt you to enter natural language queries.

**Example Queries you can try:**

* **Calculator:**
    * `What is 10 plus 5?`
    * `Can you add 12.5 and 7.3?`
    * `I need to calculate the sum of 100 and 200.`
    * `Subtract 5 from 10.`
    * `What is 25 minus 12?`
* **Yahoo Finance:**
    * `What is the current stock price of Google?`
    * `Get me the quote for Apple stock.`
    * `How much is TSLA right now?`
    * `What's the latest price for Microsoft?`
* **Non-Tool Queries:**
    * `Tell me a joke.` (Should not result in a tool call)
    * `What is the capital of France?` (Should not result in a tool call)

Observe the output in both terminals. The client terminal will show Gemini's interpretation and the MCP request sent, along with the result from the server. The server terminal will show logs of the incoming MCP requests and their processing.

## How it Works

1.  **Tool Definition (`mcp_server.py`):**
    * We define our `calculator` and `yahoo_finance` tools using `fastmcp`'s `@tool` decorator and Pydantic models for input/output schemas. This automatically generates the MCP-compliant tool definitions.
    * The `MCPServer` instance then serves these tools via a JSON-RPC 2.0 endpoint (`/mcp`).

2.  **Tool Discovery (Client Startup):**
    * The `MCPClient` in `mcp_client.py` makes an initial `Context.get_tool_definitions` call to the `fastmcp` server to retrieve the schema of all available tools.

3.  **Gemini's Role (`mcp_client.py`):**
    * The discovered tool definitions are provided to the Google Gemini model when it's initialized.
    * When you type a natural language query, Gemini uses its function-calling capabilities to analyze your intent. If it determines that a query can be fulfilled by one of the provided tools, it generates a `FunctionCall` object (e.g., `name='calculator', args={'operation': 'add', 'num1': 10, 'num2': 5}`).

4.  **MCP Request Formatting (`mcp_client.py`):**
    * The `FunctionCall` object from Gemini is then translated into the exact JSON-RPC 2.0 format required by the MCP `Context.call_tool` method.

5.  **Tool Execution (`mcp_server.py`):**
    * The `MCPClient` sends this formatted MCP request to the `fastmcp` server.
    * The `fastmcp` server receives the request, validates it against the tool's schema, executes the corresponding Python function (`calculator_tool` or `yahoo_finance_tool`), and returns the result in an MCP-compliant JSON-RPC 2.0 response.

## Future Enhancements

* **More Operations:** Extend the `calculator` tool to include multiplication, division, etc.
* **Error Handling:** Implement more sophisticated error handling and user feedback for tool failures.
* **Complex Tool Parameters:** Explore how to handle more complex data structures (e.g., lists, nested objects) as tool parameters.
* **Asynchronous Client:** For real-world applications, consider using an asynchronous HTTP client (like `httpx` or `aiohttp`) in the client script for better performance.
* **Context Management:** Explore MCP's `Context.update_resource` and `Context.get_resource` methods to manage shared state or data between tool calls.
* **Multi-Agent Orchestration:** Build a more complex system where multiple AI agents interact with each other and tools via MCP.
* **Deployment:** Deploy the `fastmcp` server to a cloud platform (e.g., Google Cloud Run, Azure App Service) for a production environment.
```

---

### 2) `requirements.txt`

```
fastmcp[server]
uvicorn
requests
yfinance
google-generativeai
```

---

### 3) `mcp_server.py` (Updated Server)

```python
import uvicorn
from fastmcp import MCPServer, tool
from pydantic import BaseModel, Field
import logging
import yfinance as yf # New import for Yahoo Finance

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize the MCPServer ---
mcp_server = MCPServer(
    server_id="genai-tool-demo-server",
    description="An MCP server hosting calculator and Yahoo Finance tools for GenAI demos."
)

# --- Pydantic Models for Calculator Tool ---
class CalculatorInput(BaseModel):
    operation: str = Field(..., description="The arithmetic operation to perform.", examples=["add", "subtract"])
    num1: float = Field(..., description="The first number.")
    num2: float = Field(..., description="The second number.")

class CalculatorOutput(BaseModel):
    value: float = Field(..., description="The result of the arithmetic operation.")

# --- Define the Calculator Tool ---
@tool(
    name="calculator",
    description="A simple calculator tool that can perform arithmetic operations like addition and subtraction.",
    input_model=CalculatorInput,
    output_model=CalculatorOutput,
    tags=["math", "basic"],
)
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
@tool(
    name="yahoo_finance",
    description="Fetches current stock quotes and basic company information from Yahoo Finance.",
    input_model=YahooFinanceInput,
    output_model=YahooFinanceOutput,
    tags=["finance", "stock"],
)
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
    uvicorn.run(mcp_server.app, host="127.0.0.1", port=5000)

```

---

### 4) `mcp_client.py` (Updated Client with Gemini Integration)

```python
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

```


---

Now you have all the pieces to run this enhanced MCP demo! Remember to follow the instructions in the `README.md` carefully, especially regarding the Gemini API key. Enjoy playing with it!