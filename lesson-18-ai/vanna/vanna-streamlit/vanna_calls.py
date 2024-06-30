import streamlit as st
# from vanna.remote import VannaDefault

from vanna.ollama import Ollama
from vanna.google import GoogleGeminiChat
from vanna.openai import OpenAI_Chat
from vanna.anthropic import Anthropic_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from api_key_store import ApiKeyStore

LLM_MODEL_MAP = {
    "OpenAI GPT 4": 'gpt-4',
    "OpenAI GPT 3.5 Turbo": 'gpt-3.5-turbo',
    "Google Gemini 1.5 Pro": 'gemini-1.5-pro',
    "Anthropic Claude 3.5 Sonnet": 'claude-3-5-sonnet-20240620',
    "Meta Llama 3 (Open)": 'llama3',
    "Alibaba QWen 2 (Open)": 'qwen2',
    "Google CodeGemma (Open)": 'codegemma',
    "Google Gemma (Open)": 'gemma',
    "Mistral (Open)": 'mistral',
}


def lookup_llm_api_key(llm_model, llm_vendor):
    """
        return 
            API_KEY for closed model
            "OLLAMA" for open-source model
            None for unknown model
    """
    reverse_map = {v:k for k, v in LLM_MODEL_MAP.items()}
    if llm_model not in reverse_map:
        st.error(f"Unknown LLM model: {llm_model}")
        return None
    
    model_spec = reverse_map.get(llm_model)
    if "(Open)" in model_spec:
        return "OLLAMA"

    vendor = model_spec.split()[0].upper()
    aks = ApiKeyStore()

    if vendor == "GOOGLE":
        return aks.get_api_key(provider="GOOGLE/VERTEX_AI")
    elif vendor == "ANTHROPIC":
        return aks.get_api_key(provider="ANTHROPIC")
    elif vendor == "OPENAI":
        return aks.get_api_key(provider="OPENAI")
    else:
        st.error(f"Unknown LLM vendor: {vendor} | {llm_vendor}")
        return None



class MyVannaOpenAI(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

class MyVannaGoogle(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config=config)

class MyVannaAnthropic(ChromaDB_VectorStore, Anthropic_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Anthropic_Chat.__init__(self, config=config)

class MyVannaOllama(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

@st.cache_resource(ttl=3600)
def setup_vanna(_cfg_data):

    llm_vendor = _cfg_data.get("llm_vendor")
    llm_model = _cfg_data.get("llm_model")
    llm_api_key = lookup_llm_api_key(llm_model, llm_vendor)
    vector_db = _cfg_data.get("vector_db")
    db_type = _cfg_data.get("db_type")
    db_url = _cfg_data.get("db_url")

    if db_type not in ["SQLite"]:
        st.error(f"Unsupported db_type: {db_type}")
        return None

    if vector_db not in ["chromadb"]:
        st.error(f"invalid vector_db: {vector_db}")
        return None

    if llm_api_key is None:
        st.error(f"invalid LLM model")
        return None

    elif llm_api_key == "OLLAMA":
        config = {
            'model': llm_model,  # 'llama3' 
        }
        vn = MyVannaOllama(config=config)
    else:
        config = {
            'api_key': llm_api_key, 
            'model': llm_model,  # 'llama3' 
        }
        if llm_vendor == "OpenAI":  
            vn = MyVannaOpenAI(config=config)
        elif llm_vendor == "Google":  
            vn = MyVannaGoogle(config=config)
        elif llm_vendor == "Anthropic":  
            vn = MyVannaAnthropic(config=config)
        else:
            st.error(f"Unsupported LLM vendor: {llm_vendor}")
            return None

    vn.connect_to_sqlite(db_url)

    if not vn.run_sql_is_set:
        st.error(f"Failed to connect to DB")
        return None

    return vn

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached(_cfg_data):
    vn = setup_vanna(_cfg_data)
    return vn.generate_questions()

## Streamlit will not hash an argument with a leading underscore
@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(_cfg_data, question, sql, df):
    vn = setup_vanna(_cfg_data)
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

# @st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(_cfg_data, question: str):
    vn = setup_vanna(_cfg_data)
    raw_sql = vn.generate_sql(question=question, allow_llm_to_see_data=True)
    if raw_sql.strip()[-1] != ";":
        raw_sql += ";"
    my_sql = vn.extract_sql(raw_sql)
    return my_sql

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(_cfg_data, sql: str):
    vn = setup_vanna(_cfg_data)
    return vn.is_sql_valid(sql=sql)

def is_sql_valid(_cfg_data, sql: str):
    vn = setup_vanna(_cfg_data)
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(_cfg_data, sql: str):
    vn = setup_vanna(_cfg_data)
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(_cfg_data, question, sql, df):
    vn = setup_vanna(_cfg_data)
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(_cfg_data, question, sql, df):
    vn = setup_vanna(_cfg_data)
    return vn.generate_plotly_code(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(_cfg_data, code, df):
    vn = setup_vanna(_cfg_data)
    return vn.get_plotly_figure(plotly_code=code, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(_cfg_data, question, df):
    vn = setup_vanna(_cfg_data)
    return vn.generate_summary(question=question, df=df)

@st.cache_data(show_spinner="Show training data ...")
def show_training_data_cached(_cfg_data):
    vn = setup_vanna(_cfg_data)
    return vn.get_training_data()