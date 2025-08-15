# [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)

```bash

# ### 1. Create a directory for global packages
# # this works around permission error on Ubuntu
# mkdir -p ~/.npm-global

# ### 2. Configure npm to use it
# npm config set prefix ~/.npm-global

# ### 3. Add to your PATH
# echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
# source ~/.bashrc

# ensure to use nvm (see https://claude.ai/chat/97d14170-9d9d-40b9-a912-f5c4a4502f8f)

### 4. Install Claude Code
# claude code - https://docs.anthropic.com/en/docs/claude-code/quickstart
npm install -g @anthropic-ai/claude-code

### 5. Setup Anthropic env vars
export ANTHROPIC_API_KEY="sk-ant-api03-AXc***123DTGB-456"
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
## export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"  # Latest 3.5 Sonnet
export ANTHROPIC_MODEL="claude-sonnet-4-20250514"    # Default for Claude Code

### 6. Launch
# cd <project folder>
claude

```


ANTHROPIC_AUTH_TOKEN - Used for Claude Console (web interface) authentication
ANTHROPIC_API_KEY - Used for direct API access

Solution 1: Use API Key Only (Recommended for CLI)

```bash
# Clear the auth token
unset ANTHROPIC_AUTH_TOKEN
```

Solution 2: Use Console Auth Only
```bash
# Clear the API key
unset ANTHROPIC_API_KEY

# Logout and re-login to Claude Console
claude /logout
claude /login
# When prompted, say "No" to API key approval
```

check current env
```bash
env | grep ANTHROPIC

unset ANTHROPIC_AUTH_TOKEN
ccr code
```