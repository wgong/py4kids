## Intro

The Agno Agentic Framework is an open-source, model-agnostic framework designed for building multimodal AI agents. It allows developers to create, deploy, and manage AI agents that can handle various types of data inputs, such as text, images, audio, and video. The framework is lightweight and provides a unified API for leveraging large language models (LLMs) with enhanced capabilities like memory, knowledge, and tool integration.

### How It Works
- **Multimodal Capabilities**: Agno supports the integration of different data types, enabling the creation of agents that can process and respond to text, images, audio, and video inputs.
- **Unified API**: It provides a consistent interface for interacting with various LLMs, simplifying the development process.
- **Enhanced Features**: The framework extends the basic functionalities of LLMs by adding features such as memory and knowledge management, which are crucial for building more intelligent and context-aware agents.
- **Open-Source and Extensible**: Being open-source, Agno allows developers to customize and extend its functionalities to suit specific needs.

### Sources
- [Agno on GitHub](https://github.com/agno-agi/agno)
- [Agno Framework Overview - Best AI Agents](https://bestaiagents.ai/agent/agno)
- [How to Build MultiModal AI Agents Using Agno Framework? - Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/03/agno-framework/)

## Setup
```bash
conda create -n agno python=3.11
conda activate agno

# my forked
cd ~/projects/wgong/phidata

# source
cd ~/projects/AI/phidata/agno

# setup key
cd ~/api_keys/apikeystore
pip install -e .

# examples
cd ~/projects/wgong/phidata/cookbook/getting_started

pip install openai agno

```

### local setup

https://docs.agno.com/workspaces/agent-app/local

```
conda activate agno
cd ~/projects/wgong/phidata/cookbook/u8hi_agents/agent-app-chinook

ag ws up
# - Open localhost:8501 to view the streamlit UI.
# - Open localhost:8000/docs to view the FastAPI routes.

ag ws down
```


## Study Notes

### Concept

#### [Probabilistic Progamming](https://chat.qwen.ai/c/72090629-c170-457c-b834-55da56c16e93)

Agents are AI programs that execute tasks autonomously. They solve problems by running tools, accessing knowledge and memory to improve responses. Unlike traditional programs that follow a predefined execution path, agents dynamically adapt their approach based on context, knowledge and tool results.

Instead of a rigid binary definition, let’s think of Agents in terms of agency and autonomy.

- Level 0: Agents with no tools (basic inference tasks).
- Level 1: Agents with tools for autonomous task execution.
- Level 2: Agents with knowledge, combining memory and reasoning.
- Level 3: Teams of specialized agents collaborating on complex workflows.


### Example Use-Cases

https://docs.agno.com/examples/introduction


### Performance

Lightning Fast: Agent creation is 10,000x faster than LangGraph, see [performance](https://github.com/agno-agi/agno#performance).

Playground app uses FastAPI, see `~/phidata/libs/agno/agno/playground/playground.py`

