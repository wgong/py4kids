from utils import *

st.set_page_config(
     page_title=f'{STR_MENU_EVAL} ',
     layout="wide",
     initial_sidebar_state="expanded",
)
st.header(f"{STR_MENU_EVAL} 💯")

st.markdown(f"""
#### Summary
Results by asking 24 questions on Chinook dataset using the following LLM models
- **Closed models**: gpt-4o, gpt-4, claude-3.5-sonnet, gemini-1.5-pro 
- **Open models**: qwen2.5, deepseek, llama3, gemma2, codegemma,  mistral
""", unsafe_allow_html=True)

# st.image("./docs/model-cross-comparison-2024-06-21.png")
st.image("https://github.com/gongwork/data-copilot/blob/main/docs/Text2SQL-benchmark-2024-11-16_11-50-42.png?raw=true")

st.markdown(f"""
#### Details
- [openai-gpt-4o-mini-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/openai-gpt-4o-mini-chromadb-sqlite-test-1.pdf)
- [ollama-gemma2-chromadb-sqlite-test-2.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/ollama-gemma2-chromadb-sqlite-test-2.pdf)
- [openai-gpt-4-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/openai-gpt-4-chromadb-sqlite-test-1.pdf)
- [openai-gpt-3-5-turbo-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/openai-gpt-35-turbo-chromadb-sqlite-test-1.pdf)
- [google-gemini-1-5-pro-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/google-gemini-1-5-pro-chromadb-sqlite-test-1.pdf)
- [antropic-claude-3-5-sonnet-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/antropic-claude-3-5-sonnet-chromadb-sqlite-test-1.pdf)
- [ollama-llama3-chromadb-sqlite-test-2.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/ollama-llama3-chromadb-sqlite-test-2.pdf)
- [ollama-qwen2-chromadb-sqlite-test-2.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/ollama-qwen2-chromadb-sqlite-test-2.pdf)
- [ollama-codegemma-chromadb-sqlite-test-2.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/ollama-codegemma-chromadb-sqlite-test-2.pdf)
- [ollama-mistral-chromadb-sqlite-test-1.pdf](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/docs/ollama-mistral-chromadb-sqlite-test-1.pdf)
""", unsafe_allow_html=True)

