
## st_rag
~/projects/gongwork/st_rag/readme-u1gwg.md

##  big-agi
~/projects/AI/ollama-webui

##  ollama-webui
~/projects/AI/ollama-webui/readme-u1gwg.md
https://github.com/open-webui/open-webui


##  chat-ollama

### run Docker

### run locally

#### git clone
```
git clone git@github.com:sugarforever/chat-ollama.git
```

#### ollama server
already installed locally

but v0.1.21 failed for embedding:

```
$ curl -X POST http://localhost:11434/api/embeddings -d '{"model":"nomic-embed-text"}'
{"error":"llama runner: failed to load model '/usr/share/ollama/.ollama/models/blobs/sha256:970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6': this model may be incompatible with your version of Ollama. If you previously pulled this model, try updating it by running `ollama pull nomic-embed-text:latest`"}
```

upgrade to v0.1.29

```
curl -fsSL https://ollama.com/install.sh | sh
```

verify nomic-embed-text model again
```
$ curl -X POST http://localhost:11434/api/embeddings -d '{"model":"nomic-embed-text"}'
{"embedding":[]}
```

#### install ChromaDB docker
```
cd chat-ollama
docker pull chromadb/chroma
docker run -d -p 8000:8000 chromadb/chroma
```

#### setup env

```
cp .env.example .env
```

#### setup npm

```
npm install
```

#### database migration

Run a migration to create your database tables with Prisma Migrate

```
npm run prisma-migrate
```

#### run dev server

```
npm run dev
```
open browser at `http://localhost:3000`


##### config ollama server

http://localhost:11434



## git tip
/home/gongai/projects/wgong/py4kids/lesson-99-misc/git/readme-u1gwg.md

## https://github.com/embedchain/embedchain
Embedchain is an Open Source RAG Framework that makes it easy to create and deploy AI apps.


## langchain SQL
https://python.langchain.com/docs/use_cases/sql/

## pgvector
https://github.com/pgvector/pgvector