# ollama server

make sure it is running at http://localhost:11434/

# docker desktop

launch if not running

# ChromaDB
```
docker run -d -p 8000:8000 chromadb/chroma
```

open browser at http://localhost:8000/ : got response `{"detail":"Not Found"}`

# launch dev server

```
cd ~/projects/AI/lighthouse-learning-machine/chat-ollama
npm run dev -- --port 3003
```
running at http://localhost:3003/

