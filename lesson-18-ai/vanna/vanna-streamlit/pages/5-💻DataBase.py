from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_DB} 💻")

TABLE_NAME = "customers"
KEY_PREFIX = f"col_{TABLE_NAME}"

def get_data():
    with DBConn(CFG["DB_APP_DATA"]) as _conn:
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

    # data = get_data()
    # st.dataframe(data)
    st.markdown(f"""
    #### Schema of SQLite public dataset: <span style="color: blue;">Chinook music store </span>
    """, unsafe_allow_html=True)    

    st.image("./docs/sqlite-sample-database-chinook.jpg")

if __name__ == '__main__':
    main()
