from utils import *

st.set_page_config(layout="wide")
is_rag = 0 if st.session_state.get("config_disable_rag", False) else 1
# print(f"is_rag = {is_rag}")
page_title = STR_MENU_ASK_RAG if is_rag else STR_MENU_ASK_LLM
st.header(f"{page_title} ❓")

TABLE_NAME = CFG["TABLE_QA"]
KEY_PREFIX = f"col_{TABLE_NAME}"

cfg_data = db_current_cfg()
DB_URL = cfg_data.get("db_url")


sample_questions = {

    DEFAULT_DB_NAME : f"""
    #### Sample prompts for "Chinook" dataset
    - List all the tables
    - List all the tables , ignore tables starting with "sqlite_"
    - How many customers are there
    - What tables store customer order information? 
    - Find top 5 customers by sales
    - what are the top 5 countries that customers come from
    - List all customers from Canada and their email addresses
    - Find the top 5 most expensive tracks (based on unit price)
    - Identify artists who have albums with tracks appearing in multiple genres (Hint: join artists and albums tables on ArtistId column)
    - Count number of customers by country
    - List all albums and their corresponding artist names
    - Find all tracks with a name containing "What" (case-insensitive)
    - Get the total number of invoices for each customer
    - Find the total number of invoices per country
    - List top 5 invoices with a total exceeding $10
    - Find top 10 invoices with the larges total amount since 2010 
    - List all employees and their reporting manager's name (if any)
    - Show the top 10 customers from United States by the average invoice total
    - Find the top 5 most expensive tracks (based on unit price)
    - List top 10 genres and the number of tracks in each genre
    - Get all genres that do not have any tracks associated with them
    - There are 3 tables: artists, albums and tracks, where albums and artists are linked by ArtistId, albums, Can you find the top 10 most popular artists based on the number of tracks
    - Find top 10 customer with the most invoices
    - Find top 5 customer who bought the most albums in total quantity (across all invoices).  Hint: album quantity is found in invoice_items,
    - Find the top 5 customers who spent the most money overall (Hint: order total can be found on invoices table, calculation using invoice_items detail table is unnecessary)
    - Get all playlists containing at least 10 tracks and the total duration of those tracks
    - Identify top 10 artists who have albums with tracks appearing in multiple genres:

    see [text-to-SQL questions](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/note_book/gongai/test-2/ollama-llama3-chromadb-sqlite-test-2.ipynb)
    """,

    "imdb" : f"""
    #### Sample prompts for "Movie" dataset
    - how many movies are there
    - how many movie directors are there
    - Find these 3 directors: James Cameron ; Luc Besson ; John Woo
    - What movies have Steven Spielberg directed, please list them alphabetically
    - Find 10 best comedy films from the 1980s ranked by votes (Classic starting point)
    - Show me top 10 drama movies from the 1990s with over 100k votes (Mainstream hits)
    - List 10 highest-rated documentary films from 2000-2010 (Genre exploration)
    - What are the top 10 movies featuring Tom Hanks ranked by votes? (Actor focus)
    - Who are the top 10 directors based on total votes across their films? (Creator discovery)
    - Show me movies longer than 3 hours with highest votes (Runtime pattern)
    - List TV series that ran for more than 10 seasons (TV exploration)
    - I like to watch movies about wall street, show me top 10 titles

    - For any interesting film from above queries:
        - Tell me about [movie title] (Get plot, reception, impact)
        - What makes [movie title] a significant film in its genre?
    
    More info:
    - [IMDb Wikipedia](https://www.wikiwand.com/en/articles/IMDb)
    - [imdb-sqlite at pypi.org](https://pypi.org/project/imdb-sqlite/)
    - [imdb-sqlite at github](https://github.com/jojje/imdb-sqlite)
    - [IMDB notebook at kaggle](https://www.kaggle.com/code/priy998/imdb-sqlite/notebook)
    """,

    "stock" : f"""
    #### Sample prompts for "Company Ranks" dataset
    - What are the tables in this database
    - what are the top 10 companies by market cap in United States
    - how many companies are there in United States
    - Show me the key financial metrics for the top 5 companies
    - for the top 5 companies from Europe, show their key financial metrics
    - show their key financial metrics for the top 5 companies from Asia

    see [kaggle](https://www.kaggle.com/datasets/patricklford/largest-companies-analysis-worldwide)
    """,

}


def db_insert_qa_result(qa_data, DEBUG_FLAG=True):
    """Insert Q&A results to DB 
    """
    if not qa_data: return

    id_config = qa_data.get("id_config")
    my_question = qa_data.get("my_question")
    is_rag = qa_data.get("is_rag")
    question = escape_single_quote(my_question)
    answer = qa_data.get("my_answer")

    if not answer: return

    my_sql = answer.get("my_sql", {})
    if my_sql:
        sql_generated = escape_single_quote(my_sql.get("data"))
        sql_ts_delta = my_sql.get("ts_delta")
    else:
        sql_generated = ""
        sql_ts_delta = ""
    
    is_valid_flag = answer.get("my_valid_sql").get("data")
    if isinstance(is_valid_flag, bool):
        sql_is_valid = "Y" if is_valid_flag else "N"
    else:
        sql_is_valid = is_valid_flag

    my_plot = answer.get("my_plot", {})
    if my_plot:
        py_generated = escape_single_quote(my_plot.get("data"))
        py_ts_delta = my_plot.get("ts_delta")
    else:
        py_generated = ""
        py_ts_delta = ""

    my_fig = answer.get("my_fig", {})
    if my_fig:
        fig_generated = escape_single_quote(str(my_fig.get("data")))
    else:
        fig_generated = ""

    my_summary = answer.get("my_summary", {})
    if my_summary:
        summary_generated = escape_single_quote(my_summary.get("data"))
        summary_ts_delta = my_summary.get("ts_delta")
    else:
        summary_generated = ""
        summary_ts_delta = ""

    # id = get_uuid()
    curr_ts = get_ts_now()

    # insert
    sql_script = f"""
        insert into {TABLE_NAME} (
            id_config,
            question,
            is_rag,
            sql_generated,
            sql_ts_delta,
            sql_is_valid,
            py_generated,
            py_ts_delta,
            fig_generated,
            summary_generated,
            summary_ts_delta,
            is_active,
            created_at,
            updated_at,
            created_by
        ) values (
            {id_config},
            '{question}',
            {is_rag},
            '{sql_generated}',
            '{sql_ts_delta}',
            '{sql_is_valid}',
            '{py_generated}',
            '{py_ts_delta}',
            '{fig_generated}',
            '{summary_generated}',
            '{summary_ts_delta}',
            1,
            '{curr_ts}',
            '{curr_ts}',
            '{DEFAULT_USER}'
        );
    """
    with DBConn() as _conn:
        if DEBUG_FLAG:
            logging.info(sql_script)
        db_run_sql(sql_script, _conn)

    # add to knowledge-base
    if st.session_state.get("out_allow_feedback", True) and sql_is_valid == "Y" and my_question and sql_generated:
        db_name = cfg_data.get("db_name")
        vn = setup_vanna_cached(cfg_data)
        result = vn.train(question=my_question, sql=sql_generated, dataset=db_name)
        st.image("https://raw.githubusercontent.com/gongwork/data-copilot/refs/heads/main/docs/blank_space.png")
        st.success(f"Feedback is added to knowledgebase [id = {result}]")        

def ask_llm_direct(my_question):

    my_answer = {}

    st_cache_enabled = st.session_state.get("enable_st_cache", True)

    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")

    ts_start = time()
    resp = ask_llm(cfg_data, question=my_question, enable_st_cache=st_cache_enabled)
    ts_stop = time()
    ts_delta = f"{(ts_stop-ts_start):.2f}"

    if resp:
        assistant_message = st.chat_message(
            "assistant", avatar=VANNA_ICON_URL
        )
        assistant_message.write(resp)
        # store response in my_sql column
        my_answer.update({"my_sql":{"data":resp, "ts_delta": ts_delta}})
        my_answer.update({"my_valid_sql":{"data":"N"}})

    return my_answer

def ask_rag(my_question):
    # store question/results in session_state, prefix vars with "my_"
    # so that they can be displayed in another page or persisted
    my_answer = {}

    st_cache_enabled = st.session_state.get("enable_st_cache", True)

    user_message = st.chat_message("user")
    user_message.write(f"{my_question}")

    c_left, c_right = st.columns([4,6])

    with c_left:
        ts_start = time()
        my_sql = generate_sql(cfg_data, question=my_question, enable_st_cache=st_cache_enabled)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"
        my_answer.update({"my_sql":{"data":my_sql, "ts_delta": ts_delta}})

        my_valid_sql = is_sql_valid(cfg_data, sql=my_sql)
        my_answer.update({"my_valid_sql":{"data":my_valid_sql}})
        if not my_valid_sql:
            assistant_message = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message.write(my_sql)
            return my_answer

        if st.session_state.get("out_show_sql", True):
            assistant_message_sql = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_sql.code(my_sql, language="sql", line_numbers=True)
        else:
            with st.expander("Show SQL Query", expanded=False):
                st.code(my_sql, language="sql", line_numbers=True)

        ts_start = time()
        my_df = run_sql(cfg_data, sql=my_sql, enable_st_cache=st_cache_enabled)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"        
        my_answer.update({"my_df":{"data":my_df, "ts_delta": ts_delta}})

        if my_df is None or my_df.empty: 
            return my_answer 

        if st.session_state.get("out_show_table", True):
            assistant_message_table = st.chat_message(
                "assistant",
                avatar=VANNA_ICON_URL,
            )
            assistant_message_table.dataframe(my_df)

    with c_right:

        if should_generate_chart(cfg_data, df=my_df, enable_st_cache=st_cache_enabled):

            ts_start = time()
            my_plot = generate_plotly_code(cfg_data, question=my_question, sql=my_sql, df=my_df, enable_st_cache=st_cache_enabled)
            ts_stop = time()
            ts_delta = f"{(ts_stop-ts_start):.2f}"
            my_answer.update({"my_plot":{"data":my_plot, "ts_delta": ts_delta}})
            if not my_plot:
                return my_answer

            if st.session_state.get("out_show_plotly_code", False):
                assistant_message_plotly_code = st.chat_message(
                    "assistant",
                    avatar=VANNA_ICON_URL,
                )
                assistant_message_plotly_code.code(
                    my_plot, language="python", line_numbers=True
                )
            else:
                with st.expander("Show Python Code", expanded=False):
                    st.code(my_plot, language="python", line_numbers=True)            

            if st.session_state.get("out_show_chart", True):
                assistant_message_chart = st.chat_message(
                    "assistant",
                    avatar=VANNA_ICON_URL,
                )
                my_fig = generate_plot(cfg_data, code=my_plot, df=my_df, enable_st_cache=st_cache_enabled)
                my_answer.update({"my_fig":{"data":my_fig}})
                if my_fig is not None:
                    assistant_message_chart.plotly_chart(my_fig)
                else:
                    assistant_message_chart.error("I couldn't generate a chart")

    # display summary
    if st.session_state.get("out_show_summary", True):
        ts_start = time()
        my_summary = generate_summary(cfg_data, question=my_question, df=my_df, enable_st_cache=st_cache_enabled)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"
        my_answer.update({"my_summary":{"data":my_summary, "ts_delta": ts_delta}})
        if not my_summary:
            return my_answer 

        assistant_message_summary = st.chat_message(
            "assistant",
            avatar=VANNA_ICON_URL,
        )
        assistant_message_summary.text(my_summary)

    return my_answer


def ask_ai():
    """ Question AI
    """
    my_question = st.chat_input(
        "Ask me a question about your data",
    )

    if not my_question: return 

    if is_rag:
        my_answer = ask_rag(my_question)
    else:
        my_answer = ask_llm_direct(my_question)

    qa_data = {
        "id_config": cfg_data.get("id"),
        "my_question": my_question,
        "my_answer": my_answer,
        "is_rag": is_rag,
    }
    if st.session_state.get("debug_ask_ai", False):
        st.write(qa_data)

    try:
        db_insert_qa_result(qa_data)
    except Exception as e:
        logging.error(str(e))

## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Show Configuration", expanded=False):

            st.checkbox("Disable RAG", value=False, key="config_disable_rag")

            # st.write(cfg_data)
            cfg_show_data(cfg_data)

        with st.expander("Output Settings", expanded=False):
            st.checkbox("Show SQL Query", value=False, key="out_show_sql")
            st.checkbox("Show Dataframe", value=True, key="out_show_table")
            st.checkbox("Show Python Code", value=False, key="out_show_plotly_code")
            st.checkbox("Show Plotly Chart", value=True, key="out_show_chart")
            st.checkbox("Show Summary", value=False, key="out_show_summary")
            # st.checkbox("Show Follow-up Questions", value=False, key="show_followup")

            st.checkbox("Allow Feedback", value=True, key="out_allow_feedback")
            st.checkbox("Enable Streamlit Cache", value=True, key="enable_st_cache")
            st.number_input("SQL Limit", value=20, key="out_sql_limit")

            st.checkbox("Debug", value=False, key="debug_ask_ai")

            # st.button("Reset", on_click=lambda: reset_my_state(), use_container_width=True)

        sample_q = ""
        for db_name in sample_questions.keys():
            if db_name in DB_URL:
                sample_q = sample_questions.get(db_name,"")

        if sample_q:
            st.markdown(sample_q, unsafe_allow_html=True)  

def main():
    do_sidebar()
    try:
        ask_ai()
    except Exception as e:
        st.error(str(e))

if __name__ == '__main__':
    main()
