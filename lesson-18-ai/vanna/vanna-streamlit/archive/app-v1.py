import time
import streamlit as st
# from code_editor import code_editor
from vanna_calls import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached
)

_STR_APP_NAME   = "Data Copilot"
VANNA_ICON_URL  = "https://vanna.ai/img/vanna.svg"

st.set_page_config(
     page_title=f'{_STR_APP_NAME}',
     layout="wide",
     initial_sidebar_state="expanded",
)

def set_question(question):
    st.session_state["my_question"] = question




_STR_MENU_HOME              = "Data Copilot"
_STR_MENU_VANNA             = "Vanna AI"
_STR_MENU_RESULT            = "Result History"

#####################################################
# Menu Handlers
#####################################################
def do_welcome():
    st.header(f"What is {_STR_MENU_HOME}?")

    st.markdown(f"""
    Data Copilot is a game-changer that streamlines the data-to-insight life-cycle. It is an AI-powered assistant, built on cutting-edge LLM models, empowers data scientists, engineers, and analysts to unlock insights from data faster than ever, 
    allows them to focus on deeper analysis and strategic decision-making. Imagine asking questions in plain English, having them translated into SQL queries and python code on the fly, then receiving results in informative texts and visual plots.
                
    Tech-stack:
    - [Vanna.AI](https://github.com/vanna-ai)
    - [Ollama](https://ollama.com/)
    - [Streamlit](https://streamlit.io/)

    """, unsafe_allow_html=True)



def do_vanna():
    """ Ask Vanna

    TODO 
    - store question/SQL/python/dataframe/Plotly chart/summary in session state

    """
    st.title(_STR_MENU_VANNA)


    my_question = st.chat_input(
        "Ask me a question about your data",
    )

    if my_question:
        st.session_state["my_question"] = my_question
        user_message = st.chat_message("user")
        user_message.write(f"{my_question}")

        sql = generate_sql_cached(question=my_question)

        if sql:
            if is_sql_valid_cached(sql=sql):
                if st.session_state.get("show_sql", True):
                    assistant_message_sql = st.chat_message(
                        "assistant", avatar=VANNA_ICON_URL
                    )
                    assistant_message_sql.code(sql, language="sql", line_numbers=True)
            else:
                assistant_message = st.chat_message(
                    "assistant", avatar=VANNA_ICON_URL
                )
                assistant_message.write(sql)
                return

            df = run_sql_cached(sql=sql)

            if df is not None:
                st.session_state["df"] = df

            if st.session_state.get("df") is not None:
                if st.session_state.get("show_table", True):
                    df = st.session_state.get("df")
                    assistant_message_table = st.chat_message(
                        "assistant",
                        avatar=VANNA_ICON_URL,
                    )
                    assistant_message_table.dataframe(df)

                if should_generate_chart_cached(question=my_question, sql=sql, df=df):

                    code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)

                    if st.session_state.get("show_plotly_code", False):
                        assistant_message_plotly_code = st.chat_message(
                            "assistant",
                            avatar=VANNA_ICON_URL,
                        )
                        assistant_message_plotly_code.code(
                            code, language="python", line_numbers=True
                        )

                    if code is not None and code != "":
                        if st.session_state.get("show_chart", True):
                            assistant_message_chart = st.chat_message(
                                "assistant",
                                avatar=VANNA_ICON_URL,
                            )
                            fig = generate_plot_cached(code=code, df=df)
                            if fig is not None:
                                assistant_message_chart.plotly_chart(fig)
                            else:
                                assistant_message_chart.error("I couldn't generate a chart")

                if st.session_state.get("show_summary", True):
                    assistant_message_summary = st.chat_message(
                        "assistant",
                        avatar=VANNA_ICON_URL,
                    )
                    summary = generate_summary_cached(question=my_question, df=df)
                    if summary is not None:
                        assistant_message_summary.text(summary)


        else:
            assistant_message_error = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_error.error("I wasn't able to generate SQL for that question")

def do_result():
    """ Show result history
    """
    st.header(f"{_STR_MENU_RESULT}")

#####################################################
# setup menu_items 
#####################################################
menu_dict = {
    _STR_MENU_HOME :           {"fn": do_welcome},
    _STR_MENU_VANNA:           {"fn": do_vanna},
    _STR_MENU_RESULT:          {"fn": do_result},
}

## sidebar Menu
def do_sidebar():
    menu_options = list(menu_dict.keys())
    default_ix = menu_options.index(_STR_MENU_HOME)

    with st.sidebar:
        st.markdown(f"<h1><font color=red>{_STR_APP_NAME}</font></h1>",unsafe_allow_html=True) 

        menu_item = st.selectbox("Menu:", menu_options, index=default_ix, key="menu_item")
        # keep menu item in the same order as i18n strings

        if menu_item in [_STR_MENU_VANNA]:

            st.title("Output Settings")
            st.checkbox("Show SQL Query", value=True, key="show_sql")
            st.checkbox("Show Dataframe", value=True, key="show_table")
            st.checkbox("Show Python Code", value=True, key="show_plotly_code")
            st.checkbox("Show Plotly Chart", value=True, key="show_chart")
            st.checkbox("Show Summary", value=True, key="show_summary")
            # st.checkbox("Show Follow-up Questions", value=False, key="show_followup")
            st.button("Reset", on_click=lambda: set_question(None), use_container_width=True)

            # st.write(st.session_state)

# body
def do_body():
    menu_item = st.session_state.get("menu_item", _STR_MENU_HOME)
    menu_dict[menu_item]["fn"]()

def main(): 
    do_sidebar()
    do_body()

if __name__ == '__main__':
    main()