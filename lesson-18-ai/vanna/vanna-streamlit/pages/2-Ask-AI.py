from utils import *
from time import time

from vanna_calls import (
    setup_vanna,
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached,
)


st.set_page_config(layout="wide")
st.subheader(f"{STR_MENU_ASK} 📝")

TABLE_NAME = CFG["TABLE_QA"]
KEY_PREFIX = f"col_{TABLE_NAME}"

## sidebar Menu
def do_sidebar():
    with st.sidebar:
        my_llm_model = st.session_state.get("my_llm_model")
        st.write(f"Model '{my_llm_model}' selected")
        st.title("Output Settings")
        st.checkbox("Show SQL Query", value=True, key="show_sql")
        st.checkbox("Show Dataframe", value=True, key="show_table")
        st.checkbox("Show Python Code", value=True, key="show_plotly_code")
        st.checkbox("Show Plotly Chart", value=True, key="show_chart")
        st.checkbox("Show Summary", value=True, key="show_summary")
        # st.checkbox("Show Follow-up Questions", value=False, key="show_followup")
        # st.button("Reset", on_click=lambda: reset_my_state(), use_container_width=True)


def ask_ai():
    """ Ask Vanna.AI questions

    TODO 
        - store results into "t_qa" table
    """

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
        my_sql = generate_sql_cached(question=my_question)
        ts_stop = time()
        ts_delta = f"{(ts_stop-ts_start):.2f}"
        my_answer.update({"my_sql":{"data":my_sql, "ts_delta": ts_delta}})
        if not my_sql:
            assistant_message_error = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_error.error("I wasn't able to generate SQL for that question")
            return


        my_valid_sql = True
        if not is_sql_valid_cached(sql=my_sql):
            my_valid_sql = False

            assistant_message = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            msg = f"""Invalid SQL:
                {my_sql}
            """
            assistant_message.write(msg)

        my_answer.update({"my_valid_sql":{"data":my_valid_sql}})
        if not my_valid_sql:
            st.write(my_answer)
            return

        if st.session_state.get("show_sql", True):
            assistant_message_sql = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_sql.code(my_sql, language="sql", line_numbers=True)

        ts_start = time()
        my_df = run_sql_cached(sql=my_sql)
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

            if should_generate_chart_cached(question=my_question, sql=my_sql, df=my_df):

                ts_start = time()
                my_plot = generate_plotly_code_cached(question=my_question, sql=my_sql, df=my_df)
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
                        my_fig = generate_plot_cached(code=my_plot, df=my_df)
                        my_answer.update({"my_fig":{"data":my_fig}})
                        if my_fig is not None:
                            assistant_message_chart.plotly_chart(my_fig)
                        else:
                            assistant_message_chart.error("I couldn't generate a chart")

            # display summary
            ts_start = time()
            my_summary = generate_summary_cached(question=my_question, df=my_df)
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

        st.write({
            "my_question": my_question,
            "my_answer": my_answer,
        })


def main():
    do_sidebar()
    ask_ai()

if __name__ == '__main__':
    main()
