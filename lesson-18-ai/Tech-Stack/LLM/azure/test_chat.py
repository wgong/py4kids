
import os
from openai import AzureOpenAI

endpoint = os.getenv("AZURE_ENDPOINT", "https://papa-gpt4.openai.azure.com/")
subscription_key = os.getenv("AZURE_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")


# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a helpful AI assistant."
            },
        ]
    },
    {
        "role": "user",
        "content": "I like to learn geometry, give me a short introduction",
    }

]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
response = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

# print(response.to_json())

print(response.choices[0].message.content)
    
