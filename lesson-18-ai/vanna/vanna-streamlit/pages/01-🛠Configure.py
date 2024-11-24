from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_CONFIG} 🛠")


TABLE_NAME = CFG["TABLE_CONFIG"]
KEY_PREFIX = f"col_{TABLE_NAME}"

llm_model_list = list(LLM_MODEL_MAP.keys())

def db_upsert_cfg(data):
    llm_vendor=data.get("llm_vendor")
    llm_model=data.get("llm_model")
    vector_db=data.get("vector_db")
    db_type=data.get("db_type")
    db_name=data.get("db_name", "default")
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
                and db_name='{db_name}'
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
                    db_name,
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
                    '{db_name}',
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

def db_get_cfg_data(LIMIT=20):
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                *
            from {TABLE_NAME}
            order by ts desc
            limit {LIMIT}
            ;
        """
        # print(sql_stmt)
        return pd.read_sql(sql_stmt, _conn)

def do_config():
    db_type = "SQLite"
    avail_dbs = list_datasets(db_type)
    # st.write(avail_dbs)
    try:
        cfg_data = db_current_cfg()
    except Exception as e:
        print(str(e))
    if not cfg_data:
        db_name = "chinook"
        db_info = avail_dbs.get(db_name, {})
        if not db_info:
            st.error(f"Missing dataset {db_name}")
            return 
        
        cfg_data = {
            "vector_db": "chromadb",
            "llm_vendor": "Alibaba",
            "llm_model": "qwen2.5-coder:latest",
            "db_type": db_info.get("db_type"),
            "db_name": db_name,
            "db_url": db_info.get("db_url"),
        }

    # st.write(cfg_data)
    st.markdown(f"""
    ##### Data Base

    """, unsafe_allow_html=True)
    
    with st.expander("Specify data source: (default - SQLite)", expanded=True):
        db_list = sorted(SQL_DIALECTS)
        c1, c2, c3 = st.columns([2,2,6])
        with c1:
            db_name = st.selectbox(
                "DB Name",
                options=avail_dbs.keys(),
                index=list(avail_dbs.keys()).index(cfg_data.get("db_name"))
            )
        with c2:
            db_type = st.selectbox(
                "DB Type",
                options=db_list,
                index=db_list.index(cfg_data.get("db_type"))
            )
        with c3:
            db_url = st.text_input(
                "DB URL",
                value=avail_dbs[db_name].get("db_url"),
                disabled=True
            )

    st.markdown(f"""
    ##### Knowledge Base
    """, unsafe_allow_html=True)    

    with st.expander("Specify vector store: (default - ChromaDB)", expanded=True):
        vector_db_list = sorted(VECTOR_DB_LIST)
        vector_db = st.selectbox(
            "Vector DB Type",
            options=vector_db_list,
            index=vector_db_list.index(cfg_data.get("vector_db"))
        )

    st.markdown(f"""
    ##### GenAI Model

    """, unsafe_allow_html=True)    

    with st.expander("Specify LLM model: (default - Alibaba QWen 2.5 Coder) ", expanded=True):
        ollama_link = """
        <span style="color: red;"><a href=https://ollama.com/search>Ollama</a></span> is required to run open-source LLM models (with '(Open)'-suffix)
        """
        st.markdown(ollama_link, unsafe_allow_html=True)
        llm_model_name = LLM_MODEL_REVERSE_MAP.get(cfg_data.get("llm_model"), DEFAULT_LLM_MODEL)
        model_selected = st.radio(
            "Model name",
            options=llm_model_list,
            index=llm_model_list.index(llm_model_name),
        )
        # st.write(f"selected model: {model_selected}")
        llm_vendor, llm_model = parse_llm_model_spec(model_selected)

    if st.button("Save"):
        cfg_data = dict(
            llm_vendor=llm_vendor, 
            llm_model=llm_model, 
            vector_db=vector_db, 
            db_type=db_type, 
            db_name=db_name, 
            db_url=db_url
        )
        db_upsert_cfg(cfg_data)

    with st.expander("Show Config Data:", expanded=False):
        data = db_get_cfg_data()
        st.dataframe(data)

## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Show Configuration", expanded=False):
            cfg_data = db_current_cfg()
            cfg_show_data(cfg_data)

def main():
    do_sidebar()
    do_config()

if __name__ == '__main__':   
    main()


