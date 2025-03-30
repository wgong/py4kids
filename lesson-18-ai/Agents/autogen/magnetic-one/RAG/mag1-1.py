"""
conda activate ag

python mag1-1.py 

see mag1-1.log.md

"""

import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console



model_id = "gpt-4o-mini"  # "gpt-4o"

# "Provide a different proof for Fermat's Last Theorem"
task = """
how to prove Pythagorean theorom
"""

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model=model_id)

    assistant = AssistantAgent(
        "Assistant",
        model_client=model_client,
    )
    team = MagenticOneGroupChat([assistant], model_client=model_client)
    await Console(team.run_stream(task=task))


asyncio.run(main())
