"""
conda activate ag

python mag1-2.py 

see mag1-2.log.md

"""

import asyncio
# from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console

from utils_u8hi import *

model_id = "qwen2.5" # "gpt-4o-mini"  # "gpt-4o"
framework = "magnetic-one" # "agno" # 

# "Provide a different proof for Fermat's Last Theorem"
task = "how to prove Pythagorean theorom"

async def main() -> None:
    # model_client = OpenAIChatCompletionClient(model=model_id)
    kwargs = {"model_id": model_id}
    model_client = create_chat_client(model_name=model_id, 
                                      agent_framework=framework, 
                                      **kwargs)

    assistant = AssistantAgent(
        "Assistant",
        model_client=model_client,
    )
    team = MagenticOneGroupChat([assistant], model_client=model_client)
    await Console(team.run_stream(task=task))


asyncio.run(main())
