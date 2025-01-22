from utils import *

st.set_page_config(layout="wide")
st.header("Notes 📝")

DB_URL = CFG["META_DB_URL"]
TABLE_NAME = CFG["TABLE_NOTE"]
KEY_PREFIX = f"col_{TABLE_NAME}"

def get_tags():
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                distinct tags
            from {TABLE_NAME}
            ;
        """
        return pd.read_sql(sql_stmt, _conn)["tags"].to_list()

def do_note():
    # get distinct tags
    tags = get_tags()

    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                note_name
                , note 
                , url 
                , tags
                , is_active
                , updated_at
                , id
            from {TABLE_NAME}
            order by updated_at desc
            ;
        """
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, 
                                   clickable_columns=["url"],
                                   selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # streamlit-aggrid==0.3.3
    # selected_row = selected_rows[0] if len(selected_rows) else None
    # streamlit-aggrid==1.0.5
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    # display form
    ui_layout_form(selected_row, TABLE_NAME)

    c_1, c_2 = st.columns([3,3])
    with c_1:
        if df is not None and not df.empty:
            st.download_button(
                label="Download CSV",
                data=df_to_csv(df, index=False),
                file_name=f"notes-{get_ts_now()}.csv",
                mime='text/csv',
            )
    with c_2:
        tags_new = []
        for t in tags:
            if t is None or not t: continue
            if "," in t:
                tags_new.extend([i.strip().upper() for i in t.split(",") if i.strip()])
            else:
                tags_new.append(t.strip().upper())
        tag_str = " , ".join(sorted(list(set(tags_new))))
        st.markdown(f"""
            ##### Tags
            {tag_str}
        """, unsafe_allow_html=True)

def main():
    try:
        do_note()
    except Exception as e:
        st.error(str(e))   

if __name__ == '__main__':
    main()
