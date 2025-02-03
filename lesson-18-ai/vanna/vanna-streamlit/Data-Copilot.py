from utils import *


from dotenv import load_dotenv  # type: ignore
load_dotenv()

st.set_page_config(
    page_title=f'{STR_APP_NAME}',
    layout="wide",
    initial_sidebar_state="expanded",
)


header_html = f"""
<table style="border: none; border-collapse: collapse; width: 100%; max-width: 1200px;">
    <tr style="border: none;">
        <td style="width: 100px; vertical-align: top; padding: 1rem; border: none;">
            <!-- Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 80px; height: 80px;">
                <circle cx="50" cy="50" r="45" fill="#E3F2FD"/>
                <rect x="25" y="60" width="10" height="20" fill="#2196F3"/>
                <rect x="45" y="40" width="10" height="40" fill="#1976D2"/>
                <rect x="65" y="30" width="10" height="50" fill="#0D47A1"/>
                <path d="M25 45 L45 35 L65 25" fill="none" stroke="#4CAF50" stroke-width="3" stroke-linecap="round"/>
                <circle cx="25" cy="45" r="3" fill="#4CAF50"/>
                <circle cx="45" cy="35" r="3" fill="#4CAF50"/>
                <circle cx="65" cy="25" r="3" fill="#4CAF50"/>
                <circle cx="60" cy="40" r="12" fill="none" stroke="#FF5722" stroke-width="3"/>
                <line x1="68" y1="48" x2="75" y2="55" stroke="#FF5722" stroke-width="3" stroke-linecap="round"/>
            </svg>
        </td>
        <td style="vertical-align: top; padding: 1rem; line-height: 1.5; border: none;">
            <!-- Text -->
            <span style="color: red;"><strong>Data-Copilot</strong></span>
is an AI Assistant, speaks both natural language (like English) and machine languages (such as SQL and Python), acts like an interpreter between Analysts and Data, Analysts can now talk to data and derive insight faster than ever. With gained productivity, they can spend more time on deep analysis and strategic decision-making.
        </td>
    </tr>
</table>
"""

msg_features = """
#### <span style="color: black;">Features</span>
- **<span style="color: red;">RAG</span>**: ask dataset-specific question via Retrieval Augmented Generation
    - <span style="color: blue;">Semantic Search</span>: discover data schema
    - <span style="color: blue;">Text-to-SQL</span>: generate SQL from plain text
    - <span style="color: blue;">Data-to-Plot</span>: generate Python code to visualize data 
- **<span style="color: red;">ChatGPT</span>**: ask general question on <span style="color: blue;">Large-Language-Model </span> (LLM) of choice 
- **<span style="color: red;">Data Privacy</span>** (_optional_) : leverage  <span style="color: blue;">Ollama</span> and open-source LLM models locally 
- **<span style="color: red;">Note-Taking</span>**:
- **<span style="color: red;">Knowledge-Sharing</span>**:
- **<span style="color: red;">Chat-History</span>**:
"""

def render_header():
    st.markdown(header_html, unsafe_allow_html=True)


DEBUG_KEY = False
if DEBUG_KEY:
  x = os.getenv("GOOGLE_MODEL")
  y = os.getenv("GOOGLE_API_KEY")
  # x = os.getenv("ANTHROPIC_MODEL")
  # x = os.getenv("ANTHROPIC_API_KEY")
  # x = os.getenv("OPENAI_MODEL")
  # x = os.getenv("OPENAI_API_KEY")
  st.info(f"Model = {x} , API_Key = {y}")

## Welcome page
st.markdown(f"""
### <span style="color: black;">Self-Service Analytics</span>
""", unsafe_allow_html=True)

render_header()

st.markdown(f"""
#### <span style="color: black;">Architecture </span>
""", unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/gongwork/data-copilot/refs/heads/main/docs/00-data-copilot-arch-design.png")

st.markdown(msg_features, unsafe_allow_html=True)

# st.markdown(f"""
# #### <span style="color: blue;">Demo Video</span>
# https://www.youtube.com/watch?v=RKSlUAFmbaM
            
# #### <span style="color: blue;">GitHub Repo </span>
# https://github.com/gongwork/data-copilot
# """, unsafe_allow_html=True)

def insert_default_user():
    count = db_get_row_count(table_name="t_user")
    if count < 1:
        curr_ts = get_ts_now()
        insert_user = f""" 
            insert into t_user(
                email, created_by, updated_by, 
                username, password, created_at, updated_at
            ) 
            values(
                '{DEFAULT_USER}', '{DEFAULT_USER}', '{DEFAULT_USER}', 
                '{DEFAULT_USER}', '{DEFAULT_USER}', '{curr_ts}', '{curr_ts}'
            );
        """
        with DBConn() as _conn:
            db_run_sql(insert_user, _conn)        

def create_tables():
    # run a test query
    try:
        db_get_row_count(table_name=CFG["TABLE_CONFIG"])
    except Exception as e:
        ddl_script = open(CFG["META_DB_DDL"]).read()
        logging.error(ddl_script)
        with DBConn() as _conn:
            db_run_sql(ddl_script, _conn)
            
if __name__ == '__main__':
    # create tables if missing
    create_tables()
    insert_default_user()
