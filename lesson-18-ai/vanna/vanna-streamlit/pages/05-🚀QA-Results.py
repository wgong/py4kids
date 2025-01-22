from utils import *

st.set_page_config(layout="wide")
st.header(f"{STR_MENU_RESULT} 🚀")

TABLE_NAME = CFG["TABLE_QA"]
KEY_PREFIX = f"col_{TABLE_NAME}"

def review_qa_history():
    # if "previous_row" not in st.session_state:
    #     st.session_state.previous_row = None
    df = None 
    selected_cols = [ "question", "sql_generated", "py_generated", "fig_generated", "is_rag", "sql_is_valid", "id", "id_config"]

    search_question = st.text_input("🔍Search question:", key=f"{KEY_PREFIX}_search_question").strip()
    where_clause = f" question like '%{search_question}%'" if search_question else " 1=1 "


    DB_URL = CFG["META_DB_URL"]
    with DBConn(DB_URL) as _conn:
        sql_stmt = f"""
            select 
                {','.join(selected_cols)}
            from {TABLE_NAME}
            where 1=1 and {where_clause}
            order by updated_at desc
            ;
        """
        df = pd.read_sql(sql_stmt, _conn)

    # display grid
    grid_resp = ui_display_df_grid(
            df, 
            selection_mode="single",
            # temp use
            page_size=10,
            grid_height=int(0.95*AGGRID_OPTIONS["grid_height"]),
        )

    selected_rows = grid_resp['selected_rows']
    if selected_rows is None or len(selected_rows) < 1:

        if df is not None and not df.empty:
            st.download_button(
                label="Download CSV",
                data=df_to_csv(df, index=False),
                file_name=f"qa_history-{get_ts_now()}.csv",
                mime='text/csv',
            )

        return

    row = selected_rows.iloc[0].to_dict() if isinstance(selected_rows, pd.DataFrame) else selected_rows[0]
    # if row != st.session_state.previous_row:
    #     st.session_state.previous_row = row
    #     st.rerun()

    # st.write(row)
    row_id = row.get("id") if row else ""
    row_id_config = row.get("id_config") if row else ""
    row_question = row.get("question") if row else ""
    row_is_rag = row.get("is_rag") if row else 1
    row_sql_generated = row.get("sql_generated") if row else ""
    row_sql_is_valid = row.get("sql_is_valid", "N") if row else "N"
    row_py_generated = row.get("py_generated") if row else ""
    # row_fig_generated = row.get("fig_generated") if row else ""
    
    cfg_data = db_current_cfg(row_id_config)
    # st.write(cfg_data)
    cfg_vector_db = cfg_data.get("vector_db") if cfg_data else ""
    cfg_db_type = cfg_data.get("db_type") if cfg_data else ""
    cfg_db_name = cfg_data.get("db_name") if cfg_data else ""
    cfg_db_url = cfg_data.get("db_url") if cfg_data else ""
    cfg_llm_vendor = cfg_data.get("llm_vendor") if cfg_data else ""
    cfg_llm_model = cfg_data.get("llm_model") if cfg_data else ""

    c1, _, c2 = st.columns([8,1,2])
    with c1:
        st.text_area("Question", value=row_question, height=100, disabled=False, key=f"{KEY_PREFIX}_question")
    with c2:
        st.checkbox("Use RAG?", value=(row_is_rag==1), key="{KEY_PREFIX}_is_rag")
        st.checkbox("Valid SQL?", value=(row_sql_is_valid=="Y"), key="{KEY_PREFIX}_valid_sql")
    c_left, c_right = st.columns([4,6])

    if row_sql_is_valid != "Y":
        st.markdown(row_sql_generated, unsafe_allow_html=True)
    else:
        my_df = None
        with c_left:
            with st.expander("Show SQL Query", expanded=False):
                st.code(row_sql_generated, language="sql", line_numbers=True)

            try:
                with DBConn(cfg_db_url) as _conn2:
                    my_df = pd.read_sql(row_sql_generated, _conn2) if row_sql_is_valid == "Y" else None
                    if my_df is not None:
                        st.dataframe(my_df)
            except Exception as e:
                st.error(f"str(e): \n{cfg_db_url}")

        with c_right:
            if row_py_generated:
                with st.expander("Show Python Code", expanded=False):
                    st.code(row_py_generated, language="python", line_numbers=True)

            try:
                if my_df is not None:
                    my_fig = generate_plot_cached(cfg_data, code=row_py_generated, df=my_df)
                    if my_fig:
                        st.plotly_chart(my_fig)
            except Exception as e:
                st.error(str(e))


    with st.expander("Show Config", expanded=False):
        c0_1, c0_2, c0_3, c0_4 = st.columns(4)
        with c0_1:
            st.text_input('llm_vendor', value=cfg_llm_vendor, disabled=True, key=f"{KEY_PREFIX}_llm_vendor")
        with c0_2:
            st.text_input('llm_model', value=cfg_llm_model, disabled=True, key=f"{KEY_PREFIX}_llm_model")
        with c0_3:
            st.text_input('vector_db', value=cfg_vector_db, disabled=True, key=f"{KEY_PREFIX}_vector_db")
        with c0_4:
            st.text_input('id', value=row_id, disabled=True, key=f"{KEY_PREFIX}_row_id")
        c1_1, c1_2, c1_3 = st.columns([1,1,2])
        with c1_1:
            st.text_input('db_name', value=cfg_db_name, disabled=True, key=f"{KEY_PREFIX}_db_name")
        with c1_2:
            st.text_input('db_type', value=cfg_db_type, disabled=True, key=f"{KEY_PREFIX}_db_type")
        with c1_3:
            st.text_input('db_url', value=cfg_db_url, disabled=True, key=f"{KEY_PREFIX}_db_url")

def main():
    try:
        review_qa_history()
    except Exception as e:
        st.error(str(e))

if __name__ == '__main__':
    main()
