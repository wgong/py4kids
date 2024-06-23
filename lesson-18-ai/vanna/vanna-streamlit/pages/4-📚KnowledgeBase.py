from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_TRAIN} 📚")

def main():
    cfg_data = db_query_config()
    # st.write(cfg_data)

    vn = setup_vanna(cfg_data)

    st.subheader("Show Training data")
    if st.button("Show"):
        df = vn.get_training_data()
        st.dataframe(df)

    st.subheader("Add Training data")
    ddl_sample = """CREATE TABLE IF NOT EXISTS t_person (
        id INT PRIMARY KEY,
        name text,
        email text
    );
    """
    ddl_text = st.text_area("DDL script", value="", height=100, key="add_ddl"
                           ,placeholder=ddl_sample)
    if st.button("Add DDL script") and ddl_text:
        ddl_text = strip_brackets(ddl_text)
        result = vn.train(ddl=ddl_text)
        st.write(result)

    sql_sample = """select * from t_book;    """
    sql_text = st.text_area("SQL query", value="", height=100, key="add_sql"
                           ,placeholder=sql_sample)
    if st.button("Add SQL query") and sql_text:
        result = vn.train(sql=sql_text)
        st.write(result)

    doc_sample = """table "t_book" stores information on book title and author """
    doc_text = st.text_area("Documentation", value="", height=100, key="add_doc"
                           ,placeholder=doc_sample)
    if st.button("Add Documentation") and doc_text:
        result = vn.train(documentation=doc_text)
        st.write(result)

    df_ddl = None
    if st.button("Add ALL DDL scripts"):
        df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
        for ddl in df_ddl['sql'].to_list():
            ddl_text = strip_brackets(ddl)
            vn.train(ddl=ddl_text)
    if df_ddl is not None:
        st.dataframe(df_ddl)

    st.subheader("Remove Training data")
    collection_id = st.text_input("Enter collection ID", value="", key="del_collection")
    if collection_id and st.button("Remove"):
        vn.remove_training_data(id=collection_id)

    if st.button("Remove ALL collections"):
        for c in ["sql", "ddl", "documentation"]:
            vn.remove_collection(c)


if __name__ == '__main__':
    main()