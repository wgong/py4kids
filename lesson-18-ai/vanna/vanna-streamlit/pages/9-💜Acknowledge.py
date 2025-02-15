from utils import *

st.set_page_config(
     page_title=f'{STR_MENU_ACKNOWLEDGE} ',
     layout="wide",
     initial_sidebar_state="expanded",
)
st.header(f"{STR_MENU_ACKNOWLEDGE} 💜")

st.markdown(f"""
- [Vanna.ai](https://github.com/vanna-ai)
- [Streamlit](https://streamlit.io/)            
- [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- [Ollama](https://ollama.com/)
- [SQLite](https://www.sqlite.org/)
- [SQL Assistant](https://medium.com/@romina.elena.mendez/sql-assistant-text-to-sql-application-in-streamlit-b54f65d06b97)
- [Emoji Cheatsheet](https://www.webfx.com/tools/emoji-cheat-sheet/)
""", unsafe_allow_html=True)

st.image("./docs/thank-you.png")