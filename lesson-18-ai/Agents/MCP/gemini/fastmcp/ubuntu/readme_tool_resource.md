# MCP : Tool and Resource

## 🆕 New Features Added:

### 1. **Resource Discovery & Usage**
- Added resource listing with `client.list_resources()`
- Enhanced LLM parser to understand resource queries
- Added resource reading with `client.read_resource(uri)`

### 2. **Enhanced Query Parsing**
- **LLM Parser**: Now recognizes resource requests like "Tell me about Apple as a company"
- **Rule-based Parser**: Enhanced to distinguish between tool calls and resource reads
- **Combined Actions**: Can execute both tool calls and resource reads for queries like "Get Apple stock price and company info"

### 3. **New Demo Commands**
- `resources` - Lists available resources
- Enhanced help text with resource examples

### 4. **Standalone Resource Demo**
- Added `demo_resources()` function for focused resource testing
- Demonstrates reading `info://server` and `stock://{ticker}` resources
- Shows combined tool + resource usage

### 5. **Smart Query Examples**
The client now handles queries like:
- **Resource-only**: "Tell me about Apple as a company" → reads `stock://AAPL`
- **Tool-only**: "What's Apple's stock price?" → calls `stock_quote` tool
- **Combined**: "Get Apple stock price and company info" → both tool + resource

## 🚀 Usage Examples:

```bash
# Interactive mode with resource support
python mcp_tool_resource.py

# Resource-only demonstration  
python mcp_tool_resource.py
# Then choose option 2
```

## 🎯 Try These Queries:
- "Tell me about Microsoft as a company"
- "What is Tesla?" 
- "Give me server information"
- "Get Apple stock price and company info"
- "I want both Tesla's price and company details"

The enhanced client now provides a complete MCP experience with both tools and resources, powered by intelligent LLM parsing that can distinguish between different types of requests!


## ✅ **The resources ARE working correctly!**

Here's what we can see:

1. **Only `info://server` shows up in `list_resources()`** - This is expected because it's a static resource
2. **The templated `stock://{ticker}` resource pattern doesn't appear in the list** - This is normal MCP behavior for dynamic resources
3. **BUT the resources actually work!** 
   - ✅ `stock://AAPL` successfully returns: "Apple Inc. (AAPL) - A publicly traded company"
   - ✅ `info://server` successfully returns the server description

## 🔧 **The Fix**

The issue is in the enhanced MCP client - it's looking for `stock://{ticker}` in the resource list, but dynamic resources don't show up there. We need to update the client to:

1. **Hard-code knowledge of the dynamic resource patterns** since they don't appear in discovery
2. **Still try to read them even if they're not listed**Now your enhanced MCP client will:

1. ✅ **Discover static resources** from the server (like `info://server`)
2. ✅ **Add knowledge of dynamic resources** that don't appear in discovery (like `stock://{ticker}`)
3. ✅ **Successfully read both types** when requested

## 🎯 **Test it now!**

Try these queries in your enhanced client:

```bash
python mcp_client_llm.py
```

Then test:
- `"Tell me about Apple as a company"` → should read `stock://AAPL`
- `"Give me server information"` → should read `info://server`  
- `"Get Apple stock price and company info"` → should do both tool call + resource read

The resources are working perfectly - it was just a discovery issue! Dynamic/templated resources in MCP don't show up in `list_resources()` but are still accessible via `read_resource()`.


# key conceptual differences between **Tools** and **Resources** in MCP:

## 🔧 **Tools** - Actions & Operations
**Tools are functions that DO something**

- **Purpose**: Perform actions, calculations, or operations
- **Nature**: Dynamic, stateful, can change things
- **Input**: Accept parameters to customize behavior
- **Output**: Return results based on computation/action
- **Examples**: 
  - `calculator(operation="add", num1=15, num2=27)` → performs calculation
  - `stock_quote(ticker="AAPL")` → fetches live data from APIs
  - `send_email(to="user@example.com", subject="Hello")` → performs action

```python
@mcp.tool()
def calculator(operation: str, num1: float, num2: float) -> dict:
    # DOES something - performs calculation
    return {"result": num1 + num2}
```

## 📚 **Resources** - Information & Content
**Resources are content that IS something**

- **Purpose**: Provide static/semi-static information or content
- **Nature**: Informational, read-only, descriptive
- **Input**: URI-based addressing (like web URLs)
- **Output**: Return content/information about something
- **Examples**:
  - `info://server` → returns server description
  - `stock://AAPL` → returns company information about Apple
  - `file://report.pdf` → returns document content

```python
@mcp.resource("stock://{ticker}")
def stock_info(ticker: str) -> str:
    # IS something - returns information
    return f"Apple Inc. (AAPL) - A publicly traded company"
```

## 🆚 **Key Differences**

| Aspect | Tools | Resources |
|--------|-------|-----------|
| **Verb vs Noun** | "Calculate this" | "What is this?" |
| **Action vs Info** | Performs operations | Provides information |
| **Dynamic** | Can change state/external systems | Read-only content |
| **Parameters** | Function parameters | URI-based addressing |
| **Use Cases** | APIs, calculations, actions | Documentation, descriptions, content |

## 🎯 **Real-World Analogy**

Think of it like a **library**:

- **Tools** = **Librarian** 📖
  - "Please find me books about Python" (search action)
  - "Calculate my late fees" (computation)
  - "Check out these books" (state-changing action)

- **Resources** = **Books/Content** 📚
  - "Python Programming Guide" (static content)
  - "Library Rules and Policies" (informational content)
  - "Map of the Library" (descriptive content)

## 🔄 **When to Use Each**

**Use Tools when you want to:**
- Perform calculations
- Fetch live/dynamic data
- Change system state
- Execute operations
- Process inputs

**Use Resources when you want to:**
- Provide static information
- Share documentation
- Describe entities/concepts
- Offer reference content
- Give context about something

## 💡 **Your MCP Server Example**

```python
# TOOL - Does something (fetches live stock price)
@mcp.tool()
def stock_quote(ticker: str) -> dict:
    # Actively fetches current price from Yahoo Finance API
    return {"current_price": 150.25, "volume": 1000000}

# RESOURCE - Is something (provides company info)
@mcp.resource("stock://{ticker}")
def stock_info(ticker: str) -> str:
    # Returns descriptive information about the company
    return "Apple Inc. (AAPL) - A publicly traded company"
```

This is why your enhanced client can do **both** for queries like *"Get Apple stock price and company info"* - it calls the tool for live data and reads the resource for descriptive information!