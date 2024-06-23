from utils import *

st.set_page_config(
     page_title=f'{STR_APP_NAME}',
     layout="wide",
     initial_sidebar_state="expanded",
)

## Welcome page
st.markdown(f"""
### <span style="color: red;">Self-Service Analytics</span>
By streamlining the data-to-insight life-cycle, **<span style="color: red;">Data Copilot</span>** is a game-changer tool for Self-Service Analytics.
  Built on cutting-edge GenAI models, it empowers data professionals to unlock insights from data faster than ever, therefore allows them to focus on deeper analysis and strategic decision-making. 

#### <span style="color: blue;">Key Features</span>
- **<span style="color: red;">Semantic Search</span>**: discover data schema
- **<span style="color: red;">Text-to-SQL</span>**: generate SQL from plain text
- **<span style="color: red;">Data-to-Plot</span>**: generate Python code to visualize data 
- **<span style="color: red;">Data Privacy</span>**: achievable by using Ollama and open-source LLM models locally
               
#### <span style="color: blue;">Architectural Design </span>
""", unsafe_allow_html=True)

st.image("./docs/data-copilot.drawio.png")


