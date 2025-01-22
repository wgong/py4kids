from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_TRAIN} 📚")

cfg_data = db_current_cfg()
DB_NAME = cfg_data.get("db_name")
DB_URL = cfg_data.get("db_url")    
# st.write(DB_NAME, DB_URL)

def do_knowledgebase():
    df = None
    
    vn = setup_vanna_cached(cfg_data)

    with st.expander("Manage Knowledge", expanded=True):
        c_1, _, c_2, c_3, c_4 = st.columns([2,1,1,2,1])
        with c_1:
            if st.button("Show"):
                df = vn.get_training_data(dataset=DB_NAME)

        with c_2:
            btn_rm_all = st.button("Remove All")
            if btn_rm_all:
                vn.remove_collection()

        with c_3:
            doc_ids = st.text_input("Enter vector ID(s)", value="", key="del_collection")
        with c_4:
            btn_rm_id = st.button("Remove")
            if btn_rm_id and doc_ids:
                for doc_id in parse_id_list(doc_ids):
                    vn.remove_training_data(id=doc_id)

        if df is not None and not df.empty:
            st.dataframe(df)
            st.download_button(
                label="Download CSV",
                data=df_to_csv(df, index=False),
                file_name=f"knowledgebase-{get_ts_now()}.csv",
                mime='text/csv',
            )

    with st.expander("Add Schema", expanded=False):
        c1, c2 = st.columns([2,2])
        with c1:
            btn_add_all_ddl = st.button("Add All DDL scripts")
            df_ddl = None
            if btn_add_all_ddl:
                sql_stmt = """
                    select * from sqlite_master where type='table' and name not like 'sqlite%';
                """
                df_ddl = vn.run_sql(sql_stmt)
                for ddl in df_ddl['sql'].to_list():
                    ddl_text = strip_brackets(ddl)
                    vn.train(ddl=ddl_text, dataset=DB_NAME)
                if df_ddl is not None and not df_ddl.empty:
                    st.dataframe(df_ddl)

        with c2:
            ddl_sample = """CREATE TABLE IF NOT EXISTS t_person (
                id INT PRIMARY KEY,
                name text,
                email_address text
            );
            """
            ddl_text = st.text_area("DDL script", value="", height=100, key="add_ddl"
                                ,placeholder=ddl_sample)

            btn_add_ddl = st.button("Add DDL")
            if btn_add_ddl and ddl_text:
                ddl_text = strip_brackets(ddl_text)
                result = vn.train(ddl=ddl_text, dataset=DB_NAME)
                # st.write(result)


    with st.expander("Add Documentation", expanded=False):
        doc_sample = """table "t_book" stores information on book title and author """
        doc_text = st.text_area("Documentation", value="", height=100, key="add_doc"
                            ,placeholder=doc_sample)

        if st.button("Add", key="btn_add_a_doc") and doc_text:
            result = vn.train(documentation=doc_text, dataset=DB_NAME)
            st.write(result)
            st.session_state["add_doc"] = ""
                

        df_doc = None
        TABLE_BUS_TERM = CFG["TABLE_BUS_TERM"]
        try:
            df_doc = vn.run_sql(f"select * from {TABLE_BUS_TERM}")       
            st.dataframe(df_doc)
        except Exception as e:
            st.warning(f"table '{TABLE_BUS_TERM}' not found, skip!")

        if st.button("Add Bus Term", key="btn_add_bus_term"):
            try:
                if df_doc is not None and not df_doc.empty:
                    business_docs = convert_to_string_list(df_doc)
                    for doc_text in business_docs:
                        result = vn.train(documentation=doc_text, dataset=DB_NAME)
                        st.write(result)
            except Exception as e:
                st.warning(str(e))

    with st.expander("Add Question/SQL Pair", expanded=False):
        q_sample, sql_sample = "Get book counts", "select count(*) from t_book;"
        c3, c4 = st.columns([3,5])
        with c3:
            q_text = st.text_input("Question", value="", key="add_sql_q"
                            ,placeholder=q_sample)
        with c4:
            sql_text = st.text_area("SQL query", value="", height=100, key="add_sql"
                            ,placeholder=sql_sample)
        if st.button("Add", key="btn_add_question_sql") and sql_text and q_text:
            result = vn.train(question=q_text, sql=sql_text, dataset=DB_NAME)
            st.write(result)
            st.session_state["add_sql_q"] = ""
            st.session_state["add_sql"] = ""



## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Show Configuration", expanded=False):
            cfg_show_data(cfg_data)

def main():
    do_sidebar()
    try:
        do_knowledgebase()
    except Exception as e:
        st.error(str(e))

if __name__ == '__main__':
    main()