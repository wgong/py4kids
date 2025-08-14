# claude-code-demo
claude code examples


## Setup

see https://github.com/wgong/py4kids/blob/master/lesson-18-ai/SWE/Code-Collab/readme-claude-code.md



## How to use Claude Code with OpenRouter.ai
Not working

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_AUTH_TOKEN="sk-or-v1-your-openrouter-key-here"
export ANTHROPIC_MODEL="anthropic/claude-3-5-sonnet-20241022"
```

Test OpenRouter API connectivity with curl  :

```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions"  \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -d '{  
     "model": "anthropic/claude-3-5-sonnet-20241022",  
     "messages": [{"role": "user", "content": "Hello"}], 
     "max_tokens": 10  
    }' --silent --show-error    
```