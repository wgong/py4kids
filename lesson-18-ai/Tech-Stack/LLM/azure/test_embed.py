import os
from openai import AzureOpenAI
import numpy as np

# Azure OpenAI configuration
endpoint = os.getenv("AZURE_ENDPOINT", "https://papa-gpt4.openai.azure.com/")
subscription_key = os.getenv("AZURE_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")
embedding_deployment = "text-embedding-ada-002"  # Your embedding deployment name

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# Text to embed
text_to_embed = "What is gluonscope? how to use it"

try:
    # Generate embedding
    response = client.embeddings.create(
        model=embedding_deployment,
        input=text_to_embed
    )
    
    # Extract the embedding vector
    embedding_vector = response.data[0].embedding
    
    # Check dimensions and properties
    print(f"Original text: {text_to_embed}")
    print(f"Embedding dimension: {len(embedding_vector)}")
    print(f"Vector type: {type(embedding_vector)}")
    print(f"First 5 values: {embedding_vector[:5]}")
    print(f"Last 5 values: {embedding_vector[-5:]}")
    
    # Convert to numpy array for easier manipulation
    embedding_array = np.array(embedding_vector)
    print(f"Numpy array shape: {embedding_array.shape}")
    print(f"Vector norm (magnitude): {np.linalg.norm(embedding_array):.6f}")
    
    # Optional: Show some statistics
    print(f"Min value: {np.min(embedding_array):.6f}")
    print(f"Max value: {np.max(embedding_array):.6f}")
    print(f"Mean value: {np.mean(embedding_array):.6f}")
    
except Exception as e:
    print(f"Error generating embedding: {e}")


"""
$ python test_embed.py 
Original text: What is gluonscope? how to use it
Embedding dimension: 1536
Vector type: <class 'list'>
First 5 values: [-0.025215202942490578, 0.008963446132838726, 0.002092083217576146, -0.04813811555504799, 0.0069907535798847675]
Last 5 values: [-0.01251943688839674, -0.0281981211155653, -0.02046898566186428, 0.013188021257519722, -0.014833768829703331]
Numpy array shape: (1536,)
Vector norm (magnitude): 1.000000
Min value: -0.597641
Max value: 0.211831
Mean value: -0.000766

"""