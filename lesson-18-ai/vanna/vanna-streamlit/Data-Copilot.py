from utils import *

st.set_page_config(
     page_title=f'{STR_APP_NAME}',
     layout="wide",
     initial_sidebar_state="expanded",
)

## Welcome page
st.subheader(f"What is {STR_APP_NAME}?")
st.markdown(f"""
Data Copilot is a game-changer that streamlines the data-to-insight life-cycle. It is an AI-powered assistant, built on cutting-edge LLM models, empowers data scientists, engineers, and analysts to unlock insights from data faster than ever, 
allows them to focus on deeper analysis and strategic decision-making. Imagine asking questions in plain English, having them translated into SQL query and python script on the fly, then receiving results in informative texts and visual plots.
               
### Tech-stack:
- [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- [Vanna.AI](https://github.com/vanna-ai)
- [Ollama](https://ollama.com/)
- [Streamlit](https://streamlit.io/)

""", unsafe_allow_html=True)

st.image("./docs/how-vanna-works.png")

st.markdown(f"""
### Resources
- [SQL Assistant](https://medium.com/@romina.elena.mendez/sql-assistant-text-to-sql-application-in-streamlit-b54f65d06b97)
""", unsafe_allow_html=True)
