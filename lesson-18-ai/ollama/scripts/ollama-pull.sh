## use AutoGen to develop MOE
# solve a problem by using a set of best LLM models
# similar to HTTP (Hyper-Text-Transport-Protocol)

## embeddings
###################################
# ollama pull nomic-embed-text
# ollama pull all-minilm

## general LLM : QA / assistant
###################################
ollama pull nemotron-mini  # 4b
ollama pull qwen2.5        # 7b
ollama pull llama3.1                 # most capable open llm
# ollama pull llama3                 # most capable open llm
# ollama pull dolphin-llama3
ollama pull phi3.5
# ollama pull phi3                   # light-weight open llm
# ollama pull mistral
# ollama pull wizardlm2
# ollama pull neural-chat
# ollama pull openchat
# ollama pull llama3-chatqa        # excel at QA/RAG

ollama pull gemma           # 9b

# ollama pull gemma:2b
# ollama pull gemma:7b
# ollama pull dolphin-mistral
# ollama pull zephyr


## Coding
###################################
# ollama pull starcoder2
# ollama pull wizardcoder
# ollama pull sqlcoder
# ollama pull duckdb-nsql

# ollama pull stable-code
# ollama pull codegemma:2b
# ollama pull codegemma:7b
# ollama pull codellama
# ollama pull deepseek-coder


## Bilingual
###################################
# ollama pull yi
# ollama pull llama2-chinese
# ollama pull stablelm2


# ## multimodal
# ###################################
# ollama pull llava

# ## domain-specific
# ###################################
# ollama pull samantha-mistral        # philosophy/psychology
# ollama pull meditron                # medical
# ollama pull wizard-math             # math/logic

## tiny LLM
###################################
# ollama pull tinyllama

## larger LLM
###################################
# ollama pull command-r  # 35B
