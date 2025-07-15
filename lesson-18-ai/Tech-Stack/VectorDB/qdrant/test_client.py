from qdrant_client import QdrantClient
import os

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

print(qdrant_client.get_collections())
