from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_CONFIG} 🛠")

TABLE_NAME = CFG["TABLE_CONFIG"]
KEY_PREFIX = f"col_{TABLE_NAME}"

llm_model_list = filter_by_ollama_model(list(LLM_MODEL_MAP.keys()))
# st.info(llm_model_list)

def db_upsert_cfg(data):
    llm_vendor=data.get("llm_vendor")
    llm_model=data.get("llm_model")
    vector_db=data.get("vector_db")
    db_type=data.get("db_type")
    db_name=data.get("db_name", "default")
    db_url=data.get("db_url")
    # cfg_note = escape_single_quote(data.get("cfg_note",""))

    with DBConn() as _conn:
        curr_ts = get_ts_now()

        # check t_resource for SQL
        select_db = f"""
            select 
                id
            from t_resource
            where 1=1
                and type = 'SQL'
                and vendor = '{db_type}'
                and name = '{db_name}'
                and url = '{db_url}'
                and is_active = 1
                and updated_by = '{DEFAULT_USER}'
            order by updated_at desc
            limit 1
        """
        df_db = pd.read_sql(select_db, _conn)
        is_new_db = False
        if df_db is None or df_db.empty:
            is_new_db = True
            insert_db = f"""
                insert into t_resource (
                    type, vendor, name, url, 
                    created_at, updated_at, created_by, updated_by
                ) values (
                    'SQL', '{db_type}', '{db_name}', '{db_url}',
                    '{curr_ts}', '{curr_ts}', '{DEFAULT_USER}', '{DEFAULT_USER}'
                );
            """
            db_run_sql(insert_db, _conn)
            df_db_new = pd.read_sql(select_db, _conn)
            id_db = df_db_new["id"].to_list()[0]
        else:
            id_db = df_db["id"].to_list()[0]

        # check t_resource for Vector
        select_vector = f"""
            select 
                id
            from t_resource
            where 1=1
                and type = 'VECTOR'
                and vendor = '{vector_db}'
                and name = '{META_APP_NAME}'
                and is_active = 1
                and updated_by = '{DEFAULT_USER}'
            order by updated_at desc
            limit 1
        """
        df_vector = pd.read_sql(select_vector, _conn)
        is_new_vector = False
        if df_vector is None or df_vector.empty:
            is_new_vector = True
            insert_vector = f"""
                insert into t_resource (
                    type, vendor, name, 
                    created_at, updated_at, created_by, updated_by
                ) values (
                    'VECTOR', '{vector_db}', '{META_APP_NAME}', 
                    '{curr_ts}', '{curr_ts}', '{DEFAULT_USER}', '{DEFAULT_USER}'
                );
            """
            db_run_sql(insert_vector, _conn)
            df_vector_new = pd.read_sql(select_vector, _conn)
            id_vector = df_vector_new["id"].to_list()[0]
        else:
            id_vector = df_vector["id"].to_list()[0]

        # Check t_resource for LLM
        select_llm = f"""
            select 
                id
            from t_resource
            where 1=1
                and type = 'LLM'
                and vendor = '{llm_vendor}'
                and name = '{llm_model}'
                and is_active = 1
                and updated_by = '{DEFAULT_USER}'
            order by updated_at desc
            limit 1
        """
        df_llm = pd.read_sql(select_llm, _conn)
        is_new_llm = False
        if df_llm is None or df_llm.empty:
            is_new_llm = True
            insert_llm = f"""
                insert into t_resource (
                    type, vendor, name, 
                    created_at, updated_at, created_by, updated_by
                ) values (
                    'LLM', '{llm_vendor}', '{llm_model}', 
                    '{curr_ts}', '{curr_ts}', '{DEFAULT_USER}', '{DEFAULT_USER}'
                );
            """
            db_run_sql(insert_llm, _conn)
            df_llm_new = pd.read_sql(select_llm, _conn)
            id_llm = df_llm_new["id"].to_list()[0]
        else:
            id_llm = df_llm["id"].to_list()[0]

        # upsert t_config
        select_cfg = f"""
            select 
                id
            from t_config
            where 1=1
                and id_db = {id_db}
                and id_vector = {id_vector}
                and id_llm = {id_llm}
                and is_active = 1
                and updated_by = '{DEFAULT_USER}'
            order by updated_at desc
            limit 1
        """
        df_cfg = pd.read_sql(select_cfg, _conn)
        is_new_cfg = False
        if df_cfg is None or df_cfg.empty:
            is_new_cfg = True
            insert_cfg = f"""
                insert into t_config (
                    id_db, id_vector, id_llm, 
                    created_at, updated_at, created_by, updated_by
                ) values (
                    {id_db}, {id_vector}, {id_llm},
                    '{curr_ts}', '{curr_ts}', '{DEFAULT_USER}', '{DEFAULT_USER}'
                );
            """
            db_run_sql(insert_cfg, _conn)
            df_cfg_new = pd.read_sql(select_db, _conn)
            id_cfg = df_cfg_new["id"].to_list()[0]
        else:
            id_cfg = df_cfg["id"].to_list()[0]

        if not is_new_cfg:
            # update cfg
            sql_script = f"""
                update t_config
                set 
                    updated_at = '{curr_ts}'
                    , id_db = {id_db}
                    , id_vector = {id_vector}
                    , id_llm = {id_llm}
                where id = {id_cfg}
                ;
            """
            db_run_sql(sql_script, _conn)

def db_get_cfg_data(LIMIT=20):
    with DBConn() as _conn:
        sql_stmt = f"""
            with cfg_db as (
                select * 
                from t_resource
                where type = 'SQL'
                    and updated_by = '{DEFAULT_USER}'
                    and is_active = 1
            )
            , cfg_vector as (
                select * 
                from t_resource
                where type = 'VECTOR'
                    and updated_by = '{DEFAULT_USER}'
                    and is_active = 1            
            )
            , cfg_llm as (
                select * 
                from t_resource
                where type = 'LLM'
                    and updated_by = '{DEFAULT_USER}'
                    and is_active = 1            
            )
            select 
                cfg_llm.vendor as llm_vendor
                , cfg_llm.name as llm_model
                , cfg_vector.vendor as vector_db
                , cfg_db.vendor as db_type
                , cfg_db.name as db_name
                , cfg_db.url as db_url
                , cfg.*
            from {TABLE_NAME} cfg
            left join cfg_db 
                on cfg_db.id = cfg.id_db
            left join cfg_vector 
                on cfg_vector.id = cfg.id_vector
            left join cfg_llm 
                on cfg_llm.id = cfg.id_llm
            order by cfg.updated_at desc
            limit {LIMIT}
            ;
        """
        return pd.read_sql(sql_stmt, _conn)

def do_config():

    st.markdown(f"""
    ##### Data Base

    """, unsafe_allow_html=True)
    
    cfg_data = {}
    try:
        cfg_data = db_current_cfg()
    except Exception as e:
        st.error(str(e))

    if not cfg_data:
        cfg_data = CFG["DEFAULT_CFG"]

    with st.expander("Specify data source: (default - SQLite)", expanded=True):

        db_dialects = sorted(SQL_DIALECTS)
        c1, c2, c3 = st.columns([2,2,6])
        with c1:
            db_type = st.selectbox(
                "SQL DB Type",
                options=db_dialects,
                index=db_dialects.index(cfg_data.get("db_type")),
                key="cfg_db_type_select"
            )

            if db_type in [DEFAULT_DB_DIALECT]:
                avail_dbs = list_datasets(db_type)
                db_names = sorted(list(avail_dbs.keys()))
            else:
                db_names = ["New DB"]

        with c2:
            if cfg_data.get("db_name") in db_names:
                idx = db_names.index(cfg_data.get("db_name"))
            else:
                idx = 0
            db_name = st.selectbox(
                "DB Name",
                options=db_names,
                index=idx,
                key="cfg_db_name_select"
            )
        with c3:
            if db_name == "New DB":
                db_url_value = ""
            else:
                db_url_value = avail_dbs[db_name].get("db_url")

            db_url = st.text_input(
                "DB URL",
                value=db_url_value,
                key="cfg_db_url"
            )
        if db_name == "New DB":
            c_name, c_user, c_pwd, c_inst, c_port, c_5 = st.columns([3,3,3,3,3,2])
            with c_name:
                db_name_new = st.text_input(
                    "DB Name (New)",
                    value="",
                    key="cfg_db_name_new"
                )
            with c_user:
                db_username = st.text_input(
                    "DB Username", 
                    value="", 
                    key="cfg_db_username"
                )
            with c_pwd:
                db_password = st.text_input(
                    "DB Password", 
                    value="", 
                    type="password", 
                    key="cfg_db_password"
                )
            with c_inst:
                db_instance = st.text_input(
                    "DB Instance", 
                    value="", 
                    key="cfg_db_instance"
                )
            with c_port:
                db_port = st.text_input(
                    "DB port", 
                    value="", 
                    key="cfg_db_port"
                )

            with c_5:
                db_connect = st.button("Connect", key="cfg_db_connect")
                if db_connect:
                    # TODO
                    # try to connect
                    # if successful, capture resource params
                    # see habits7 repo on hashing password
                    pass


    st.markdown(f"""
    ##### Knowledge Base
    """, unsafe_allow_html=True)    

    c_1, _, _ = st.columns([6,1,4])

    with c_1:
        with st.expander(f"Specify vector store: (default - {DEFAULT_VECTOR_DB})", expanded=True):

            vector_db_list = sorted(VECTOR_DB_LIST)
            vector_db = st.selectbox(
                "Vector DB Type",
                options=vector_db_list,
                index=vector_db_list.index(cfg_data.get("vector_db"))
            )

    st.markdown(f"""
    ##### GenAI Model

    """, unsafe_allow_html=True)    
    ollama_link = """
    <span style="color: red;"><a href=https://ollama.com/search>Ollama</a></span> is required to run open-source LLM models (suffix = '(Open)')
    """

    c__1, _, c__2 = st.columns([6,1,4])

    with c__1:
        with st.expander(f"Specify LLM model: (default - {DEFAULT_LLM_MODEL})", expanded=True):
            st.markdown(ollama_link, unsafe_allow_html=True)
            llm_model_name = LLM_MODEL_REVERSE_MAP.get(cfg_data.get("llm_model"), DEFAULT_LLM_MODEL)
            model_selected = st.radio(
                "Model name",
                options=llm_model_list,
                index=llm_model_list.index(llm_model_name),
            )
            # st.write(f"selected model: {model_selected}")
            llm_vendor, llm_model = parse_llm_model_spec(model_selected)

    with c__2:
        st.markdown(f"""
        Chat with LLM:
        - [Gemini by Google](https://gemini.google.com/)
        - [Claude by Anthropic](https://claude.ai/)
        - [ChatGPT by OpenAI](https://chatgpt.com/)
        - [Copilot by Microsoft](https://copilot.microsoft.com/chats)
        - [Qwen by Alibaba](https://huggingface.co/spaces/Qwen/Qwen2.5) - huggingface
        - [DeepSeek](https://chat.deepseek.com/)
        - [NVLM by Nvidia](https://huggingface.co/nvidia/NVLM-D-72B) - huggingface
        - [Llama at Groq](https://chat.groq.com/) - very fast inference
        - [Mistral](https://chat.mistral.ai/) 
        - [You.com](https://you.com/) 
                    
            
        """, unsafe_allow_html=True)    


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
        df = db_get_cfg_data()
        st.dataframe(df)
        if df is not None and not df.empty:
            st.download_button(
                label="Download CSV",
                data=df_to_csv(df, index=False),
                file_name=f"settings-{get_ts_now()}.csv",
                mime='text/csv',
            )

## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Show Configuration", expanded=False):
            cfg_data = db_current_cfg()
            cfg_show_data(cfg_data)

def main():
    do_sidebar()
    try:
        do_config()
    except Exception as e:
        st.error(str(e))    

if __name__ == '__main__':   
    main()


