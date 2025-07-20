
# AI Oriented Insiders
https://nova-loaf-3ea.notion.site/AI-Oriented-Insiders-Club-1ec9276efa0c8096a8d0cdfcdf01baff


# Claude Code Router
https://github.com/musistudio/claude-code-router

how to fix permission error

```bash
# 1. Create a directory for global packages
mkdir -p ~/.npm-global

# 2. Configure npm to use it
npm config set prefix ~/.npm-global

# 3. Add to your PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# claude code - https://docs.anthropic.com/en/docs/claude-code/quickstart
npm install -g @anthropic-ai/claude-code

claude  # launch claude-code
# config
# ~/.claude/ - User-specific configuration
# ~/.claude.json - Global user config file

# Install claude code router
npm install -g @musistudio/claude-code-router
```

Great! Let me give you quick tutorials for both tools. First, let me check out the claude-code-router project you mentioned.Excellent find! 

Claude-code-router is a fascinating project that lets you use different AI models through Claude Code's interface. Let me give you tutorials for both.

## Quick Tutorial: Claude Code

### Basic Setup & Usage

```bash
# Start Claude Code in your project
cd your-project
claude

# Basic commands
/help          # Show all commands
/exit          # Exit Claude Code
/clear         # Clear conversation
```

### Key Features

**1. Natural Language Coding:**
```bash
# Instead of writing code yourself, describe what you want
> Create a Python function that validates email addresses using regex

# Claude will create the file and write the code
```

**2. File Management:**
```bash
> Create a new file called utils.py
> Open the README.md file
> Show me all Python files in this directory
```

**3. Code Analysis:**
```bash
> Explain what the main.py file does
> Find all TODO comments in this project
> Check for potential security issues
```

**4. Git Integration:**
```bash
> Create a commit with message "Add email validation"
> Show me the git status
> Create a pull request
```

### Useful Slash Commands

```bash
/add-dir path/to/folder    # Add additional directories
/memory                    # View/edit project memory
/permissions              # Manage permissions
/mcp                      # Model Context Protocol tools
```

## Quick Tutorial: Claude-Code-Router (CCR)

This is a brilliant tool that lets you use multiple AI models through Claude Code's interface!

### What CCR Does

Use Claude Code as the foundation for coding infrastructure, allowing you to decide how to interact with the model while enjoying updates from Anthropic

It routes different tasks to different models:
- **Router**: Small model (qwen2.5-coder-3b) for request routing
- **Tool Agent**: Model for function calling (qwen-max)
- **Coder**: Coding model (deepseek-v3)
- **Reasoning**: Advanced reasoning (deepseek-r1)

### Installation

```bash
# 1. Make sure you have Claude Code installed
npm install -g @anthropic-ai/claude-code

# 2. Clone the router project
git clone https://github.com/musistudio/claude-code-router.git
cd claude-code-router

# 3. Install dependencies
npm install
```

### Configuration

Create a `.env` file:

**Simple Mode (single model):**
```bash
ENABLE_ROUTER=false
OPENAI_API_KEY="your-key"
OPENAI_BASE_URL="https://openrouter.ai/api/v1"
OPENAI_MODEL="anthropic/claude-3.5-sonnet"
```

**Router Mode (multiple models):**
```bash
ENABLE_ROUTER=true
TOOL_AGENT_API_KEY="your-key"
TOOL_AGENT_BASE_URL="https://openrouter.ai/api/v1"
TOOL_AGENT_MODEL="qwen-max-2025-01-25"
CODER_AGENT_API_KEY="your-key"
CODER_AGENT_BASE_URL="https://api.deepseek.com"
CODER_AGENT_MODEL="deepseek-chat"
THINK_AGENT_API_KEY="your-key"
THINK_AGENT_BASE_URL="https://api.deepseek.com"
THINK_AGENT_MODEL="deepseek-reasoner"
ROUTER_AGENT_API_KEY="your-key"
ROUTER_AGENT_BASE_URL="https://openrouter.ai/api/v1"
ROUTER_AGENT_MODEL="qwen2.5-coder-3b-instruct"
```

### Usage

```bash
# 1. Start the router server
node index.mjs

# 2. In another terminal, start Claude Code with router
export DISABLE_PROMPT_CACHING=1
export ANTHROPIC_AUTH_TOKEN="test"
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
export API_TIMEOUT_MS=600000
claude
```

### Benefits for Your Text2Flow Project

**Cost Efficiency:**
- Use cheaper models for simple tasks
- Reserve expensive models for complex reasoning

**Model Specialization:**
- Coding tasks → DeepSeek (great at code)
- Complex reasoning → DeepSeek R1
- Tool calling → Qwen Max
- Simple routing → Free Qwen 3B

**Perfect for Your Workflow:**
- **Text → Mermaid**: Use reasoning model for understanding intent
- **Mermaid → FlowX**: Use coding model for translation
- **Validation**: Use tool model for checking

### Example Commands

```bash
# The router automatically chooses the right model for each task
> Analyze this mermaid diagram and suggest improvements
# → Routes to reasoning model

> Generate FlowX CLI commands from this mermaid code
# → Routes to coding model

> Check if this workflow is valid
# → Routes to tool model
```

This setup gives you access to dozens of models through OpenRouter while keeping the familiar Claude Code interface! Perfect for experimenting with different models for your text2flow project.



# NPM security

DON'T use `sudo` to `npm install`

```bash
# Check what's in the system-wide npm directory
sudo npm list -g --depth=0

# Check the actual location of global packages
npm config get prefix

# If it shows /usr/local or /usr, those were likely sudo-installed
ls -la $(npm config get prefix)/lib/node_modules/

cd /usr/lib/node_modules

sudo rm -rf @musistudio/ @mermaid-js/ @anthropic-ai/


# See which packages might have root ownership
ls -la /usr/local/lib/node_modules/ 2>/dev/null
ls -la /usr/lib/node_modules/ 2>/dev/null
```

