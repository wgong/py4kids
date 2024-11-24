from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_RESULT} 🚀")

DB_URL = CFG["DB_META_DATA"]
TABLE_NAME = CFG["TABLE_QA"]
KEY_PREFIX = f"col_{TABLE_NAME}"

def main():
    data = db_query_data(DB_URL, TABLE_NAME, limit=100, order_by=" ts desc ")
    st.dataframe(data)

if __name__ == '__main__':
    main()
