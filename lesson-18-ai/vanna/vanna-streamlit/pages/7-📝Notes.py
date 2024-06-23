from utils import *

st.set_page_config(layout="wide")
st.header("Notes 📝")

TABLE_NAME = CFG["TABLE_NOTE"]
KEY_PREFIX = f"col_{TABLE_NAME}"

def get_data():
    with DBConn(CFG["DB_META_DATA"]) as _conn:
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
    data = get_data()
    st.dataframe(data)

if __name__ == '__main__':
    main()
