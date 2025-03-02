
# FastAPI app

## Get started - Qwen2.5-Max
https://chat.qwen.ai/c/716a5bf2-28fd-4451-ac96-183349dbb4c4


## SQLite + ChromaDB
https://chat.qwen.ai/c/716a5bf2-28fd-4451-ac96-183349dbb4c4

### Embedding model - LaBSE

Use `LaBSE` for its excellent Chinese support and cross-lingual capabilities.

The `LaBSE` (Language-Agnostic BERT Sentence Embedding) model generates embeddings with a dimensionality of 768 . This is a standard size for many transformer-based models, including BERT and its variants.

#### Details

- Dimensionality:

Each embedding produced by LaBSE is a vector of 768 dimensions .
These dimensions capture rich semantic information about the input text, making it suitable for tasks like similarity search, cross-lingual retrieval, and clustering.

- Why 768 Dimensions?

The 768-dimensional space is large enough to encode complex linguistic features while remaining computationally efficient.
It strikes a good balance between expressiveness and resource usage compared to larger models (e.g., 1024 or 1536 dimensions).

- Compatibility with Vector Databases:

Many vector databases, such as ChromaDB , Milvus , and Pinecone , are optimized to handle embeddings of this size.
You can efficiently index and query 768-dimensional vectors using approximate nearest neighbor (ANN) algorithms like HNSW or IVF_FLAT .