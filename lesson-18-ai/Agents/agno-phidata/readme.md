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

