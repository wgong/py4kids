import jsonlines
from pathlib import Path
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

VANNA_ICON_URL  = "https://vanna.ai/img/vanna.svg"
VANNA_AI_PROCESS_URL = "https://private-user-images.githubusercontent.com/7146154/299417072-1d2718ad-12a8-4a76-afa2-c61754462f93.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTczMzUxMjEsIm5iZiI6MTcxNzMzNDgyMSwicGF0aCI6Ii83MTQ2MTU0LzI5OTQxNzA3Mi0xZDI3MThhZC0xMmE4LTRhNzYtYWZhMi1jNjE3NTQ0NjJmOTMuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDYwMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA2MDJUMTMyNzAxWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MmQ4MzU0ZDg1ZDg3ZWEzYjZlMWQxMDkzMTBiYjk1NGExNzYxYjQ4Y2YwMTNjYTkzZGU2N2IxMjU2YTgyZTZjNSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.o-Q0S0zOeCJrfF4XP5WKc41Eh5qIdwEwEl2n_ZA_AoM"

_STR_APP_NAME   = "Data Copilot"
_STR_MENU_HOME            = "Data Copilot"
_STR_MENU_ASK             = "Ask AI"
_STR_MENU_CONFIG          = "Configure"
_STR_MENU_TRAIN           = "Train"
_STR_MENU_RESULT          = "Result History"
_STR_MENU_VERIFY          = "Verify"


st.set_page_config(
     page_title=f'{_STR_APP_NAME}',
     layout="wide",
     initial_sidebar_state="expanded",
)

def load_jsonl(file_path):
    if not file_path.exists():
        return
    
    chats = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            chats.append(obj)
        st.session_state["my_results"] = chats

def dump_jsonl(file_path):
    if "my_results" not in st.session_state:
        return 
    
    with jsonlines.open(file_path, mode='w') as writer:
        for obj in st.session_state["my_results"]:
            writer.write(obj)  

# init
file_chat_records = Path("chat_record.jsonl")
if "my_results" not in st.session_state:
    st.session_state["my_results"] = [] # ts : ts, Q: query, A: answer
    load_jsonl(file_chat_records)


def reset_my_state():
    """Clear session states with "my_" prefix
    """
    st.session_state["my_result"] = {
        "my_question": "",
        "my_answer": {},
    }

def update_my_results(my_question, my_answer):
    if not my_question:
        return
   
    my_results = st.session_state.get("my_results")
    my_result = {
        "my_question": my_question,
        "my_answer": my_answer,
    }
    my_results.append(my_result)
    st.session_state["my_results"] = my_results

 
if "my_result" not in st.session_state:
    reset_my_state()

if "my_results" not in st.session_state:
    st.session_state["my_results"] = []


#####################################################
# Menu Handlers
#####################################################
def do_welcome():
    st.header(f"What is {_STR_MENU_HOME}?")

    st.markdown(f"""
    Data Copilot is a game-changer that streamlines the data-to-insight life-cycle. It is an AI-powered assistant, built on cutting-edge LLM models, empowers data scientists, engineers, and analysts to unlock insights from data faster than ever, 
    allows them to focus on deeper analysis and strategic decision-making. Imagine asking questions in plain English, having them translated into SQL query and python script on the fly, then receiving results in informative texts and visual plots.
                
    Tech-stack:
    - [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
    - [Vanna.AI](https://github.com/vanna-ai)
    - [Ollama](https://ollama.com/)
    - [Streamlit](https://streamlit.io/)

    """, unsafe_allow_html=True)

    st.image(VANNA_AI_PROCESS_URL)

def do_ask_ai():
    """ Ask Vanna.AI questions

    TODO 
    - store question/SQL/python/dataframe/Plotly chart/summary in session state

    """
    st.title(_STR_MENU_ASK)

    my_answer = {}

    my_question = st.chat_input(
        "Ask me a question about your data",
    )
    if my_question:
        # store question/results in session_state, prefix vars with "my_"
        # so that they can be displayed in another page or persisted
        user_message = st.chat_message("user")
        user_message.write(f"{my_question}")

        my_sql = generate_sql_cached(question=my_question)
        if not my_sql:
            assistant_message_error = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_error.error("I wasn't able to generate SQL for that question")
            return

        my_answer.update({"my_sql":my_sql})

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

        my_answer.update({"my_valid_sql":my_valid_sql})
        if not my_valid_sql:
            update_my_results(my_question, my_answer)
            return

        if st.session_state.get("show_sql", True):
            assistant_message_sql = st.chat_message(
                "assistant", avatar=VANNA_ICON_URL
            )
            assistant_message_sql.code(my_sql, language="sql", line_numbers=True)

        my_df = run_sql_cached(sql=my_sql)
        my_answer.update({"my_df":my_df})

        if my_df is not None:
            if st.session_state.get("show_table", True):
                assistant_message_table = st.chat_message(
                    "assistant",
                    avatar=VANNA_ICON_URL,
                )
                assistant_message_table.dataframe(my_df)

            if should_generate_chart_cached(question=my_question, sql=my_sql, df=my_df):

                my_plot = generate_plotly_code_cached(question=my_question, sql=my_sql, df=my_df)
                my_answer.update({"my_plot":my_plot})

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
                        my_answer.update({"my_fig":my_fig})
                        if my_fig is not None:
                            assistant_message_chart.plotly_chart(my_fig)
                        else:
                            assistant_message_chart.error("I couldn't generate a chart")

            # display summary
            my_summary = generate_summary_cached(question=my_question, df=my_df)
            my_answer.update({"my_summary":my_summary})
            if my_summary is not None and my_summary != "":
                if st.session_state.get("show_summary", True):
                    assistant_message_summary = st.chat_message(
                        "assistant",
                        avatar=VANNA_ICON_URL,
                    )
                    assistant_message_summary.text(my_summary)

        update_my_results(my_question, my_answer)


def do_config():
    """ Configure LLM model, Database URL
    """
    st.header(f"{_STR_MENU_CONFIG}")

def do_train():
    """ Add DDL/SQL/Documentation to VectorDB for RAG
    """
    st.header(f"{_STR_MENU_TRAIN}")

def do_result():
    """ Show result history
    """
    st.header(f"{_STR_MENU_RESULT}")

    my_results = st.session_state.get("my_results")

    for my_result in my_results:

        my_question = my_result.get("my_question")
        my_answer = my_result.get("my_answer")

        if not my_question or not my_answer:
            continue
        
        user_message = st.chat_message("user")
        user_message.write(f"{my_question}")

        my_sql = my_answer.get("my_sql", "")
        my_valid_sql = my_answer.get("my_valid_sql", False)
        my_df = my_answer.get("my_df", None)
        my_plot = my_answer.get("my_plot", "")
        my_fig = my_answer.get("my_fig", "")
        my_summary = my_answer.get("my_summary", "")

        if my_sql:

            if my_valid_sql:
                assistant_message_sql = st.chat_message(
                    "assistant", avatar=VANNA_ICON_URL
                )
                assistant_message_sql.code(my_sql, language="sql", line_numbers=True)
            else:
                assistant_message = st.chat_message(
                    "assistant", avatar=VANNA_ICON_URL
                )
                msg = f"""Invalid SQL:
                    {my_sql}
                """
                assistant_message.write(msg)
            
            assistant_message_table = st.chat_message(
                "assistant",
                avatar=VANNA_ICON_URL,
            )
            assistant_message_table.dataframe(my_df)

            assistant_message_plotly_code = st.chat_message(
                "assistant",
                avatar=VANNA_ICON_URL,
            )
            assistant_message_plotly_code.code(
                my_plot, language="python", line_numbers=True
            )

            assistant_message_chart = st.chat_message(
                "assistant",
                avatar=VANNA_ICON_URL,
            )
            if my_fig is not None:
                assistant_message_chart.plotly_chart(my_fig)
            else:
                assistant_message_chart.error("I couldn't generate a chart")


            assistant_message_summary = st.chat_message(
                "assistant",
                avatar=VANNA_ICON_URL,
            )
            assistant_message_summary.text(my_summary)


def do_verify():
    """ Connect to Database and verify generated SQL
    """
    st.header(f"{_STR_MENU_VERIFY}")

#####################################################
# setup menu_items 
#####################################################
menu_dict = {
    _STR_MENU_HOME :         {"fn": do_welcome},
    _STR_MENU_ASK:           {"fn": do_ask_ai},
    _STR_MENU_RESULT:        {"fn": do_result},
    _STR_MENU_VERIFY:        {"fn": do_verify},
    _STR_MENU_TRAIN:         {"fn": do_train},
    _STR_MENU_CONFIG:        {"fn": do_config},
}

## sidebar Menu
def do_sidebar():
    menu_options = list(menu_dict.keys())
    default_ix = menu_options.index(_STR_MENU_HOME)

    with st.sidebar:
        st.markdown(f"<h1><font color=red>{_STR_APP_NAME}</font></h1>",unsafe_allow_html=True) 

        menu_item = st.selectbox("Menu:", menu_options, index=default_ix, key="menu_item")
        # keep menu item in the same order as i18n strings

        if menu_item in [_STR_MENU_ASK]:

            st.title("Output Settings")
            st.checkbox("Show SQL Query", value=True, key="show_sql")
            st.checkbox("Show Dataframe", value=True, key="show_table")
            st.checkbox("Show Python Code", value=True, key="show_plotly_code")
            st.checkbox("Show Plotly Chart", value=True, key="show_chart")
            st.checkbox("Show Summary", value=True, key="show_summary")
            # st.checkbox("Show Follow-up Questions", value=False, key="show_followup")
            st.button("Reset", on_click=lambda: reset_my_state(), use_container_width=True)

        # if menu_item in [_STR_MENU_ASK, _STR_MENU_RESULT]:
        #     st.write(st.session_state)

# body
def do_body():
    menu_item = st.session_state.get("menu_item", _STR_MENU_HOME)
    menu_dict[menu_item]["fn"]()

def main(): 
    do_sidebar()
    do_body()

if __name__ == '__main__':
    main()