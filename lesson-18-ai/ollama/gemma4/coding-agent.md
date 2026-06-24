## References

- [Gemma 4 On Claude Code (using Ollama)](https://medium.com/@joe.njenga/i-tried-gemma-4-on-claude-code-and-found-new-free-google-coding-beast-6d0995ba8645)
- [Local LLMs in Real Work: Gemma 4, Qwen 3.6, and Qwen Coder (using llama.cpp)](https://medium.com/@tort_mario/local-llms-in-real-work-gemma-4-qwen-3-6-and-qwen-coder-d43811c7e9b2)
- [I Replaced Codex with Gemma 4 + Ollama](https://faun.pub/i-replaced-codex-with-gemma-4-ollama-heres-my-local-ai-coding-agent-e18307e35d6f)
- [Run Claude Code Free with NVIDIA NIM](https://medium.com/@prince-arora-aws/run-claude-code-free-with-nvidia-nim-bba8d9383bb6)


## Setup

### Nvidia NIM + Claude

sign up at build.nvidia.com
```bash
conda activate spl123
pip install uv
# Successfully installed uv-0.11.23

uv tool install 'litellm[proxy]' --with python-dotenv

litellm --version
# LiteLLM: Current Version = 1.89.3

mkdir ~/projects/AI-Tools/litellm

# browse models at https://build.nvidia.com/models
# model=qwen/qwen3.5-122b-a10b

cd ~/projects/AI-Tools/litellm
litellm --config litellm_config.yaml --port 4000
```

### Ollama + Claude
```bash
# install ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
# ollama version is 0.30.7

ollama (run | pull) gemma4:e2b

# install Claude Code
npm install -g @anthropic-ai/claude-code

# native installer
claude install
# Version: 2.1.186
# Location: ~/.local/bin/claude

# Launching the AI Coding Agent with Gemma 4
ollama launch claude --model gemma4:e2b
# got error - API Error: Claude's response exceeded the 32000 output token maximum.

# requires Ollama plan
ollama launch claude --model glm-5.2:cloud

```

