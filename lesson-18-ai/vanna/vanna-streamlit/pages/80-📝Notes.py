from utils import *

st.set_page_config(layout="wide")
st.header("Notes 📝")

DB_URL = CFG["DB_META_DATA"]
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
        # print(sql_stmt)
        return pd.read_sql(sql_stmt, _conn)["tags"].to_list()

def main():
    # get distinct tags
    tags = get_tags()

    # c1, c2, c3, c3_2, c4 = st.columns([3,6,2,2,1])
    # with c1:
    #     search_term = st.text_input("🔍Search:", key=f"{KEY_PREFIX}_search_term").strip()
    # with c2:
    #     search_others = st.text_input("🔍Free-form where-clause:", key=f"{KEY_PREFIX}_search_others").strip()
    # with c3:
    #     search_type = st.selectbox("🔍Note Type", CFG["NOTE_TYPE"], index=CFG["NOTE_TYPE"].index(""), key=f"{KEY_PREFIX}_search_type")
    # with c3_2:
    #     search_status = st.selectbox("🔍Status Code", CFG["STATUS_CODE"], index=CFG["STATUS_CODE"].index("Others"), key=f"{KEY_PREFIX}_search_status")
    # with c4:
    #     active = st.selectbox("🔍Active?", BI_STATES, index=BI_STATES.index("Y"), key=f"{KEY_PREFIX}_active")

    # where_clause = " 1=1 " 
    # where_clause += " " if not active else f" and is_active = '{active}' "
    # if not search_status:
    #     where_clause += " "
    # elif search_status == "Others":
    #     where_clause += " and (status_code is null or status_code not in ('Complete', 'De-Scoped') ) "
    # else:
    #     where_clause += f" and status_code = '{search_status}' "
    # where_clause += " " if not search_type else f" and note_type = '{search_type}' "

    # if search_term:
    #     where_clause += f""" and (
    #         title like '%{search_term}%'
    #         or note like '%{search_term}%'
    #         or tags like '%{search_term}%'       
    #     )
    #     """
    # if search_others:
    #     where_clause += f""" 
    #         and (
    #             {search_others}
    #     ) """


    df = None
    with DBConn() as _conn:
        sql_stmt = f"""
            select 
                title
                , ifnull(note, '')  as note 
                , ifnull(link_url, '')  as link_url 
                , tags
                , ifnull(is_active, '')  as is_active
                , ts
                , id
            from {TABLE_NAME}
            order by ts desc
            ;
        """
        # # print(sql_stmt)
        df = pd.read_sql(sql_stmt, _conn)

    grid_resp = ui_display_df_grid(df, 
                                   clickable_columns=["link_url"],
                                   selection_mode="single")
    selected_rows = grid_resp['selected_rows']

    # streamlit-aggrid==0.3.3
    # selected_row = selected_rows[0] if len(selected_rows) else None
    # streamlit-aggrid==1.0.5
    selected_row = None if selected_rows is None or len(selected_rows) < 1 else selected_rows.to_dict(orient='records')[0]

    # display form
    ui_layout_form(selected_row, TABLE_NAME)

    # display download CSV button
    c_1, c_2 = st.columns([3,3])
    with c_1:
        st.markdown(f"""
            ##### Download CSV
        """, unsafe_allow_html=True)
        st.download_button(
            label="Submit",
            data=df_to_csv(df, index=False),
            file_name=f"{TABLE_NAME}-{get_ts_now()}.csv",
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






if __name__ == '__main__':
    main()
