from utils import *

st.set_page_config(
     page_title=f'{STR_APP_NAME}',
     layout="wide",
     initial_sidebar_state="expanded",
)

## Welcome page
st.markdown(f"""
### What is <span style="color: red;">Self Service Analytics</span> ?
It is a game-changer that streamlines the data-to-insight life-cycle. 
            
Built on cutting-edge GenAI models, it empowers data professionals to unlock insights from data faster than ever, therefore allows them to focus on deeper analysis and strategic decision-making. 

#### <span style="color: blue;">Key Features</span>
- **Semantic Search**: discover data schema
- **Text-to-SQL**: generate SQL from plain English
- **df-to-Plot**: generate Python for data visualization
               
#### <span style="color: blue;">Architectural Design </span>
""", unsafe_allow_html=True)

st.image("./docs/data-copilot.drawio.png")


