# [Claude Code Router](https://github.com/musistudio/claude-code-router)

```bash
cd ~/projects/wgong

# 0. Install Claude Code
npm install -g @anthropic-ai/claude-code

# 1. Clone and setup CCR
git clone https://github.com/musistudio/claude-code-router.git
cd claude-code-router
npm install

# 1. Optionally install it from pkg hub
npm install -g @musistudio/claude-code-router

# 2. Create .env file for single model mode
export ENABLE_ROUTER=false
export OPENAI_API_KEY="<your-openrouter-key>"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export OPENAI_MODEL="moonshotai/kimi-k2:free"
# model catalog: https://openrouter.ai/models
# "meta-llama/llama-3.1-70b-instruct"  # or any OpenRouter model

# 2. Optionally, use ~/.claude-code-router/config.json


# 3. Start Claude Code using the router:
ccr code

# 3. Start the proxy server
node index.mjs
# not found

# 4. In another terminal, use Claude Code with the proxy
export ANTHROPIC_AUTH_TOKEN="dummy"
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
export DISABLE_PROMPT_CACHING=1
claude
```