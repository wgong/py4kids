import os.path
import streamlit as st
# from vanna.remote import VannaDefault

from vanna.ollama import Ollama
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

@st.cache_resource(ttl=3600)
def setup_vanna(model_name='llama3'):

    config = {
        'model': model_name,  # 'llama3'  # 'mistral'
    }
    vn = MyVanna(config=config)
    # file_db = "~/Downloads/chinook.sqlite"
    # file_db = os.path.abspath(os.path.expanduser(file_db))
    file_db = "./db/chinook.sqlite3"
    vn.connect_to_sqlite(file_db)

    ## api_key = st.secrets.get("VANNA_API_KEY")
    ## vn = VannaDefault(api_key=api_key, model=model_name)

    ## original
    # vn = VannaDefault(api_key=st.secrets.get("VANNA_API_KEY"), model='chinook')
    # vn.connect_to_sqlite("https://vanna.ai/Chinook.sqlite")

    return vn

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached(model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.generate_questions()

@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code

@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.get_plotly_figure(plotly_code=code, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df, model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.generate_summary(question=question, df=df)

@st.cache_data(show_spinner="Show training data ...")
def show_training_data_cached(model_name='llama3'):
    vn = setup_vanna(model_name=model_name)
    return vn.get_training_data()