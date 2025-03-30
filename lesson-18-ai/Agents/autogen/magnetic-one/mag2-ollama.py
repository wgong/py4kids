"""
conda activate ag

python mag2-ollama.py 

see mag2-ollama.log.md

"""
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient


model_id = "qwen2.5"
# Assuming your Ollama server is running locally on port 11434.
ollama_model_client = OllamaChatCompletionClient(model=model_id)

async def ask_ai(prompt: str) -> None:
    response = await ollama_model_client.create([UserMessage(content=prompt, source="user")])
    return response.content


questions = [
    "What is the capital of France?",
    "what is square root of 3",
]

async def main() -> None:

    for prompt in questions:
        print(f"## Question\n {prompt}\n")
        resp = await ask_ai(prompt)
        print(f"### Answer\n {resp}\n")

asyncio.run(main())


