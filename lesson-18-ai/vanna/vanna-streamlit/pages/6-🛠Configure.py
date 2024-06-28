from utils import *

from vanna_calls import LLM_MODEL_MAP

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_CONFIG} 🛠")

TABLE_NAME = CFG["TABLE_CONFIG"]
KEY_PREFIX = f"col_{TABLE_NAME}"

llm_model_list = list(LLM_MODEL_MAP.keys())

def parse_llm_model_spec(model_name):
    llm_vendor = model_name.split()[0]
    llm_model = LLM_MODEL_MAP.get(model_name)
    return llm_vendor, llm_model

def db_upsert_cfg(data):
    llm_vendor=data.get("llm_vendor")
    llm_model=data.get("llm_model")
    vector_db=data.get("vector_db")
    db_type=data.get("db_type")
    db_url=data.get("db_url")
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                *
            from {TABLE_NAME}
            where 1=1
                and llm_vendor='{llm_vendor}'
                and llm_model='{llm_model}'
                and vector_db='{vector_db}'
                and db_type='{db_type}'
                and db_url='{db_url}'
                and is_active='Y'
            order by ts desc
            limit 1
            ;
        """
        # print(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)
        curr_ts = get_ts_now()

        if df is None or df.empty:
            id_new = get_uuid()
            # insert
            sql_script = f"""
                insert into {TABLE_NAME} (
                    id,
                    vector_db,
                    llm_vendor,
                    llm_model,
                    db_type,
                    db_url,
                    created_ts,
                    ts,
                    is_active
                ) values (
                    '{id_new}',
                    '{vector_db}',
                    '{llm_vendor}',
                    '{llm_model}',
                    '{db_type}',
                    '{db_url}',
                    '{curr_ts}',
                    '{curr_ts}',
                    'Y'
                );
            """
        else:
            curr_data = df.to_dict("records")[0]
            id_old = curr_data.get("id")
            # update        
            sql_script = f"""
                update {TABLE_NAME} 
                set ts = '{curr_ts}'
                where id = '{id_old}'
                ;
            """
        # print(sql_script)
        db_run_sql(sql_script, _conn)

def get_data():
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                *
            from {TABLE_NAME}
            limit 5
            ;
        """
        # print(sql_stmt)
        return pd.read_sql(sql_stmt, _conn)

def main():

    st.markdown(f"""
    ##### Data Base

    """, unsafe_allow_html=True)

    with st.expander("Specify data source:", expanded=True):
        db_list = ["BigQuery","DuckDB","MSSQL","MySQL","Oracle","Postgres","SnowFlake","SQLite"]
        c1, c2 = st.columns([2,6])
        with c1:
            db_type = st.selectbox(
                "DB Type",
                options=db_list,
                index=db_list.index("SQLite")
            )

        with c2:
            db_url = st.text_input(
                "DB URL",
                value=CFG["DB_APP_DATA"]
            )

    st.markdown(f"""
    ##### Knowledge Base
    """, unsafe_allow_html=True)    

    with st.expander("Specify vector store:", expanded=True):
        vector_db_list = ["chromadb", "marqo", "opensearch","pinecone", "qdrant",]
        vector_db = st.selectbox(
            "Vector DB Type",
            options=vector_db_list,
            index=vector_db_list.index("chromadb")
        )

    st.markdown(f"""
    ##### GenAI Model

    """, unsafe_allow_html=True)    

    with st.expander("Select LLM model:", expanded=True):
    
        model_selected = st.radio(
            "GenAI model name",
            options=llm_model_list,
            index=llm_model_list.index("Anthropic Claude 3.5 Sonnet"),
        )

        llm_vendor, llm_model = parse_llm_model_spec(model_selected)

    cfg_data = dict(
        llm_vendor=llm_vendor, 
        llm_model=llm_model, 
        vector_db=vector_db, 
        db_type=db_type, 
        db_url=db_url
    )

    # st.write(cfg_data)
    if st.button("Save"):
        db_upsert_cfg(cfg_data)


if __name__ == '__main__':
    main()

    # show 
    data = get_data()
    st.dataframe(data)
