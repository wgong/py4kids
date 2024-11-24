from utils import *
from time import time

from vanna_calls import (
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    should_generate_chart_cached,
    is_sql_valid,
    generate_summary_cached,
)


st.set_page_config(layout="wide")
st.header(f"{STR_MENU_ASK} ❓")

TABLE_NAME = CFG["TABLE_QA"]
KEY_PREFIX = f"col_{TABLE_NAME}"

cfg_data = db_current_cfg()
DB_URL = cfg_data.get("db_url")


sample_questions = {
    "chinook" : f"""
        #### Sample prompts for Chinook dataset
        - List all the tables
        - What tables store order information? Hint: table_name is stored in column called "name" from table called sqlite_master
        - Find top 5 customers by sales
        - List all customers from Canada and their email addresses
        - Find the top 5 most expensive tracks (based on unit price)
        - Identify artists who have albums with tracks appearing in multiple genres (Hint: join artists and albums tables on ArtistId column)

        see [text-to-SQL questions](https://github.com/wgong/py4kids/blob/master/lesson-18-ai/vanna/note_book/gongai/test-2/ollama-llama3-chromadb-sqlite-test-2.ipynb)
        """,

    "movie" : f"""
        #### Sample prompts for Movie dataset
        - What are the tables in the movie database
        - what are the top 5 movies with highest budget? use bar chart to visualize data
        - how many movies are there
        - how many directors are there
        - Find these 3 directors: James Cameron ; Luc Besson ; John Woo
        - Find all directors with name starting with Steven
        - What movies have Steven Spielberg directed, please list them alphabetically

        see [kaggle IMDB notebook](https://www.kaggle.com/code/priy998/imdb-sqlite/notebook)
        """,

}

## sidebar Menu
def do_sidebar():
    with st.sidebar:
        with st.expander("Output Settings", expanded=False):

            st.checkbox("Show SQL Query", value=True, key="show_sql")
            st.checkbox("Show Dataframe", value=True, key="show_table")
            st.checkbox("Show Python Code", value=True, key="show_plotly_code")
            st.checkbox("Show Plotly Chart", value=True, key="show_chart")
            st.checkbox("Show Summary", value=False, key="show_summary")
            # st.checkbox("Show Follow-up Questions", value=False, key="show_followup")

            st.checkbox("Debug", value=False, key="debug_ask_ai")

            # st.button("Reset", on_click=lambda: reset_my_state(), use_container_width=True)

        sample_q = ""
        for db_name in sample_questions.keys():
            if db_name in DB_URL:
                sample_q = sample_questions.get(db_name,"")

        if sample_q:
            st.markdown(sample_q, unsafe_allow_html=True)  

 
def db_insert_qa_result(qa_data):
    """Insert Q&A results to DB 
    """
    id_config = qa_data.get("id_config")
    question = escape_single_quote(qa_data.get("my_question"))
    answer = qa_data.get("my_answer")

    my_sql = answer.get("my_sql", {})
    sql_generated = escape_single_quote(my_sql.get("data", "")) if my_sql else ""
    sql_ts_delta = my_sql.get("ts_delta", "")  if my_sql else ""
    
    sql_is_valid = "Y" if answer.get("my_valid_sql")["data"] else "N"

    my_plot = answer.get("my_plot", {})
    py_generated = escape_single_quote(my_plot.get("data", "")) if my_plot else ""
    py_ts_delta = my_plot.get("ts_delta", "") if my_plot else ""

    my_fig = answer.get("my_fig", {})
    fig_generated = escape_single_quote(str(my_fig.get("data"))) if my_fig else ""

    my_summary = answer.get("my_summary", {})   
    summary_generated = escape_single_quote(my_summary.get("data", "")) if my_summary else ""
    summary_ts_delta = my_summary.get("ts_delta", "") if my_summary else ""

    id = get_uuid()
    curr_ts = get_ts_now()

    # insert
    sql_script = f"""
        insert into {TABLE_NAME} (
            id,
            id_config,
            question,
            sql_generated,
            sql_ts_delta,
            sql_is_valid,
            py_generated,
            py_ts_delta,
            fig_generated,
            summary_generated,
            summary_ts_delta,
            created_ts,
            ts,
            is_active
        ) values (
            '{id}',
            '{id_config}',
            '{question}',
            '{sql_generated}',
            '{sql_ts_delta}',
            '{sql_is_valid}',
            '{py_generated}',
            '{py_ts_delta}',
            '{fig_generated}',
            '{summary_generated}',
            '{summary_ts_delta}',
            '{curr_ts}',
            '{curr_ts}',
            'Y'
        );
    """
    with DBConn() as _conn:
        # print(sql_script)
        db_run_sql(sql_script, _conn)

def ask_ai():
    """ Ask Vanna.AI questions

    TODO 
    """
    # create Vanna instance
    cfg_data = db_current_cfg()
    if st.session_state.get("debug_ask_ai", False):
        st.write(cfg_data)

    # st.image(VANNA_ICON_URL)
    my_answer = {}

    my_question = st.chat_input(
        "Ask me a question about your data",
    )

    if my_question:
        # store question/results in session_state, prefix vars with "my_"
        # so that they can be displayed in another page or persisted
        user_message = st.chat_message("user")
        user_message.write(f"{my_question}")

        ts_start = time()
        my_sql = generate_sql_cached(cfg_data, question=my_question)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"
        my_answer.update({"my_sql":{"data":my_sql, "ts_delta": ts_delta}})
        if not my_sql:
            assistant_message_error = st.chat_message(
                "assistant", 
                avatar=VANNA_ICON_URL
            )
            assistant_message_error.error("I wasn't able to generate SQL for that question")
            return


        my_valid_sql = True
        if not is_sql_valid(cfg_data, sql=my_sql):
            my_valid_sql = False

            assistant_message = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            msg = f"""{my_sql}"""
            assistant_message.write(msg)

        my_answer.update({"my_valid_sql":{"data":my_valid_sql}})
        if not my_valid_sql:
            if st.session_state.get("debug_ask_ai", False):
                st.write(my_answer)
            return

        if st.session_state.get("show_sql", True):
            assistant_message_sql = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_sql.code(my_sql, language="sql", line_numbers=True)

        ts_start = time()
        my_df = run_sql_cached(cfg_data, sql=my_sql)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"        
        my_answer.update({"my_df":{"data":my_df, "ts_delta": ts_delta}})

        if my_df is not None:
            if st.session_state.get("show_table", True):
                assistant_message_table = st.chat_message(
                    "assistant",
                    avatar=VANNA_ICON_URL,
                )
                assistant_message_table.dataframe(my_df)

            if should_generate_chart_cached(cfg_data, question=my_question, sql=my_sql, df=my_df):

                ts_start = time()
                my_plot = generate_plotly_code_cached(cfg_data, question=my_question, sql=my_sql, df=my_df)
                ts_stop = time()
                ts_delta = f"{(ts_stop-ts_start):.2f}"
                my_answer.update({"my_plot":{"data":my_plot, "ts_delta": ts_delta}})

                if st.session_state.get("show_plotly_code", False):
                    assistant_message_plotly_code = st.chat_message(
                        "assistant",
                        avatar=VANNA_ICON_URL,
                    )
                    assistant_message_plotly_code.code(
                        my_plot, language="python", line_numbers=True
                    )

                if my_plot is not None and my_plot != "":
                    if st.session_state.get("show_chart", True):
                        assistant_message_chart = st.chat_message(
                            "assistant",
                            avatar=VANNA_ICON_URL,
                        )
                        my_fig = generate_plot_cached(cfg_data, code=my_plot, df=my_df)
                        my_answer.update({"my_fig":{"data":my_fig}})
                        if my_fig is not None:
                            assistant_message_chart.plotly_chart(my_fig)
                        else:
                            assistant_message_chart.error("I couldn't generate a chart")

            # display summary
            ts_start = time()
            my_summary = generate_summary_cached(cfg_data, question=my_question, df=my_df)
            ts_stop = time()
            ts_delta = f"{(ts_stop-ts_start):.2f}"
            my_answer.update({"my_summary":{"data":my_summary, "ts_delta": ts_delta}})
            if my_summary is not None and my_summary != "":
                if st.session_state.get("show_summary", True):
                    assistant_message_summary = st.chat_message(
                        "assistant",
                        avatar=VANNA_ICON_URL,
                    )
                    assistant_message_summary.text(my_summary)

        qa_data = {
            "id_config": cfg_data.get("id"),
            "my_question": my_question,
            "my_answer": my_answer,
        }
        if st.session_state.get("debug_ask_ai", False):
            st.write(qa_data)

        db_insert_qa_result(qa_data)


def main():
    do_sidebar()
    ask_ai()

if __name__ == '__main__':
    main()
