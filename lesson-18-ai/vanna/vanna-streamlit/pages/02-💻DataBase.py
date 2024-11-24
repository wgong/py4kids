from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_DB} 💻")

cfg_data = db_current_cfg()
DB_NAME = cfg_data.get("db_name")
DB_URL = cfg_data.get("db_url")

db_info = {
    "chinook": f"""  
    ##### <span style="color: blue;">Chinook music store </span>
    https://www.sqlitetutorial.net/sqlite-sample-database/
    """,

    "movie": f"""
    ##### <span style="color: blue;">Movies DB</span>
    https://pypi.org/project/imdb-sqlite/
    """,

    "company_rank": f"""
    ##### <span style="color: blue;">World Top Company Ranks</span>
    https://www.kaggle.com/datasets/patricklford/largest-companies-analysis-worldwide
    """,
}

def _execute_code_sql(code):
    with DBConn(DB_URL) as _conn:
        if code.strip().lower().startswith("select") or code.strip().lower().startswith("with"):
            df = pd.read_sql(code, _conn)
            st.dataframe(df)
        elif code.strip().split(" ")[0].lower() in ["create", "insert","update", "delete", "drop"]:
            cur = _conn.cursor()
            cur.executescript(code)
            _conn.commit()

def do_database():

    st.markdown(f"""
    #### SQL Editor
    """, unsafe_allow_html=True)    

    tables = db_list_tables_sqlite(DB_URL)
    idx_default = 0
    schema_value = st.session_state.get("TABLE_SCHEMA", "")
    c1, _, c2  = st.columns([3,1,8])
    with c1:
        table_name = st.selectbox("Table:", tables, index=idx_default, key="table_name")
        if st.button("Show schema"):
            with DBConn(DB_URL) as _conn:
                df_schema = pd.read_sql(f"select sql from sqlite_schema where name = '{table_name}'; ", _conn)
                schema_value = df_schema["sql"].to_list()[0]
                st.session_state.update({"TABLE_SCHEMA" : schema_value})

    with c2:
        st.text_area("Schema:", value=schema_value, height=150)

    sql_stmt = st.text_area("SQL:", value=f"select * from {table_name} limit 10;", height=100)
    if st.button("Execute Query ..."):
        try:
            _execute_code_sql(code=sql_stmt)
        except:
            st.error(format_exc())


    st.subheader("Dataset info")
    st.markdown(db_info.get(DB_NAME), unsafe_allow_html=True)    

    if DB_NAME == "chinook":
        st.image("./docs/sqlite-sample-database-chinook.jpg")


## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Show Configuration", expanded=False):
            cfg_show_data(cfg_data)

def main():
    do_sidebar()
    do_database()

if __name__ == '__main__':
    main()
