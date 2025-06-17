
# Agent-zero

- [home](https://agent-zero.ai/#hero)
- [git](https://github.com/wgong/agent-zero)


## setup

### gongai

Install Docker Desktop
```bash
# pull agent-zero image
docker pull frdel/agent-zero-run

# run it at host port=50080, with host volume=~/a0data
docker run -p 50080:80 -v /home/gongai/a0data:/a0 frdel/agent-zero-run

# open browser at URL = http://localhost:50080/
```

#### Settings configure Models as follows:
| provider | model_name | URL |
| -------- | ---------- | --- |
| Google | gemini-2.5-flash-preview-05-20 | https://cloud.google.com/vertex-ai/generative-ai/docs/models | 
| OpenAI | gpt-4o-mini | https://platform.openai.com/docs/models | 
| Anthropic | claude-3-5-sonnet-latest | https://docs.anthropic.com/en/docs/about-claude/models/overview |
| Ollama | qwen2.5 | https://ollama.com/search | 
