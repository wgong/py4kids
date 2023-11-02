"""
Source: git@github.com:sugarforever/autogen-streamlit.git

"""

from datetime import datetime 
import sqlite3
import jsonlines
import asyncio
import pandas as pd

from autogen import AssistantAgent, UserProxyAgent
import streamlit as st

# see https://github.com/wgong/py4kids/tree/master/lesson-10-pkg/apikeystore
import api_key_store as aks

###################################
# init
###################################
s = aks.ApiKeyStore()
api_key = s.get_api_key("OPENAI")

# TODATE = datetime.now().strftime("%Y-%m-%d")
FILE_LOG = f"data/autogen_chat.log"
FILE_JSONL = f"data/autogen_chat.jsonl"
FILE_DB = f"data/autogen_chat.sqlite"

# use OpenAI GPT
MODELS = [
        'gpt-3.5-turbo', 
        # 'gpt-4'
    ]

HUMAN_INPUT_MODE = ["ALWAYS", "NEVER"]
PERSIST_MODE = ["log", "json", "sqlite"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

###################################
# helpers
###################################

class DBConn(object):
    def __init__(self, db_file=FILE_DB):
        self.conn = sqlite3.connect(db_file)

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()

def run_sql(sql_stmt, conn=None, DEBUG_SQL=False):
    if conn is None: 
        raise Exception("No database connection")

    if sql_stmt is None or not sql_stmt: 
        return

    if DEBUG_SQL:  
        print(f"[DEBUG] {sql_stmt}")

    if sql_stmt.lower().strip().startswith("select"):
        return pd.read_sql(sql_stmt, conn)
            
    cur = conn.cursor()
    cur.executescript(sql_stmt)
    conn.commit()
    return

def escape_single_quote(s):
    return s.replace("\'", "\'\'")


def msg_save2db(msg_item):
    if not msg_item: return

    ts = msg_item["ts"]
    sender = escape_single_quote(msg_item["sender"])
    message = escape_single_quote(msg_item["message"])
    sql_stmt = f"""
        insert into messages (
            ts, sender, message
        ) values (
            '{ts}', '{sender}', '{message}'
        );
    """
    with DBConn() as _conn:
        run_sql(sql_stmt, conn=_conn)

def msg_append(msg_item):
    """track chat history

    Parameter:
        msg_item (list) - [ts, sender.name, message]

    Return:
        append to messages list
    
    """
    q = st.session_state.get("messages")
    q.append(msg_item)
    st.session_state["messages"] = q

def msg_log(msg_item):
    """Write message to a log file
    """
    with open(FILE_LOG, "a", encoding="utf-8") as f:
        if msg_item:
            ts = msg_item["ts"]
            sender = msg_item["sender"]
            message = msg_item["message"]
            f.write(", ".join([f"[{ts}]", sender, message]) + "\n")

def msg_persist(msg_item):
    persist_mode=st.session_state["persist_mode"]
    if persist_mode == "log":
        msg_log(msg_item)
    elif persist_mode == "json":
        msg_append(msg_item)
    elif persist_mode == "sqlite":
        msg_save2db(msg_item)
    else:
        st.warning(f"Unknown persist mode: {persist_mode}")

class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
            ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
            msg_item = dict(ts=ts, sender=sender.name, message=message)
            msg_persist(msg_item)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
            ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
            msg_item = dict(ts=ts, sender=sender.name, message=message)
            msg_persist(msg_item)
        return super()._process_received_message(message, sender, silent)


###################################
# Streamlit App
###################################
with st.sidebar:
    st.header("OpenAI Configuration")
    selected_model = st.selectbox("Model", MODELS, index=MODELS.index('gpt-3.5-turbo'))
    # selected_key = st.text_input("API Key", type="password")

    st.radio("Human Input Mode:", HUMAN_INPUT_MODE, index=HUMAN_INPUT_MODE.index("ALWAYS"), key="human_input_mode")

    st.radio("Persist Mode:", PERSIST_MODE, index=PERSIST_MODE.index("sqlite"), key="persist_mode")

with st.container():
    st.write("""### AutoGen Chat Agents""")
    # for message in st.session_state["messages"]:
    #    st.markdown(message)
    selected_key = api_key
    user_input = st.chat_input("Type something ...     (QUIT, EXIT or TERMINATE to end conversation)")
    if user_input and str(user_input).upper() not in ["QUIT" ,"EXIT","TERMINATE"]:
        if not selected_key or not selected_model:
            st.warning(
                'You must provide valid OpenAI API key and choose preferred model', icon="⚠️")
            st.stop()

        llm_config = {
            "request_timeout": 600,
            "config_list": [
                {
                    "model": selected_model,
                    "api_key": selected_key
                }
            ]
        }
        # create an AssistantAgent instance named "assistant"
        assistant = TrackableAssistantAgent(
            name="assistant", llm_config=llm_config)

        # create a UserProxyAgent instance named "user"
        user_proxy = TrackableUserProxyAgent(
            name="user", llm_config=llm_config, 
            human_input_mode=st.session_state["human_input_mode"])

        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Define an asynchronous function
        async def initiate_chat():
            await user_proxy.a_initiate_chat(
                assistant,
                message=user_input,
            )

        # Run the asynchronous function within the event loop
        loop.run_until_complete(initiate_chat())
    else:
        if st.session_state["persist_mode"] == "json":
            st.write(f"Goodbye! Your chat history is saved into {FILE_JSONL}")
            # write out messages
            with jsonlines.open(FILE_JSONL, "a") as writer:
                msgs = st.session_state["messages"]
                if len(msgs):
                    writer.write_all(msgs)
        st.stop()

