# LanceDB - easy-to-use, scalable and cost-effective
https://lancedb.github.io/lancedb/

## Overview
LanceDB is an open-source vector database for AI that's designed to store, manage, query and retrieve embeddings on large-scale multi-modal data. The core of LanceDB is written in Rust 🦀 and is built on top of Lance, an open-source columnar data format designed for performant ML workloads and fast random access

### Why

Fast production-scale vector similarity, full-text & hybrid search and a SQL query interface (via DataFusion)

Store, query & manage multi-modal data (text, images, videos, point clouds, etc.), not just the embeddings and metadata

Disk-based index & storage, allowing for massive scalability without breaking the bank

Ingest your favorite data formats directly, like pandas DataFrames, Pydantic objects, Polars


## Setup

```bash
conda activate agno
pip install jupyter
pip install lancedb  # lancedb-0.21.1

cd ~/py4kids/lesson-18-ai/Tech-Stack/VectorDB/LanceDB
```
## Applications

### ZiNets

#### Architecture

AI-native RAG app

##### Back-End

- LanceDB : support multi-modal embeddings and search (full-text, semantic)
- DuckDB : support in-memory fast analytics and personalize recommendation

##### Middleware

FastAPI

##### Front-End
- streamlit for prototype or personalize app
- react.js for web app