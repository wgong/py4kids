"""
Source: git@github.com:sugarforever/autogen-streamlit.git

"""

import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent
import json
from datetime import datetime 

import api_key_store as aks
s = aks.ApiKeyStore()
api_key = s.get_api_key("OPENAI")

ts = datetime.now().strftime("%Y-%m-%d")
file_chat = f"autogen_chat_{ts}.log"

st.write("""# AutoGen Chat Agents""")

LOG_MSG_FLAG = False

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def update_msg(msg_item):
    """track chat history

    Parameter:
        msg_item (list) - [ts, sender.name, message]

    Return:
        append to messages list
    
    """
    q = st.session_state.get("messages")
    q.append(msg_item)
    st.session_state["messages"] = q

def log_msg(msg_item):

    # write out messages
    with open(file_chat, "a", encoding="utf-8") as f:
        if msg_item:
            f.write(", ".join(msg_item) + "\n")


class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
            ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
            if LOG_MSG_FLAG:
                log_msg([f"[ {ts} ]", sender.name, message])
            else:
                update_msg([ts, sender.name, message])
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
            ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
            if LOG_MSG_FLAG:
                log_msg([f"[ {ts} ]", sender.name, message])
            else:
                update_msg([ts, sender.name, message])
        return super()._process_received_message(message, sender, silent)

# use OpenAI GPT
MODELS = [
        'gpt-3.5-turbo', 
        # 'gpt-4'
    ]


selected_key = api_key
with st.sidebar:
    st.header("OpenAI Configuration")
    selected_model = st.selectbox("Model", MODELS, index=MODELS.index('gpt-3.5-turbo'))
    # selected_key = st.text_input("API Key", type="password")

    st.radio("Human Input Mode:", ["ALWAYS", "NEVER"], index=0, key="human_input_mode")

with st.container():
    # for message in st.session_state["messages"]:
    #    st.markdown(message)

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
        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        file_chat = f"autogen_chat_{ts}.json"
        st.write(f"Goodbye! Your chat history is saved into {file_chat}")
        # write out messages
        with open(file_chat, "w", encoding="utf-8") as f:
            json.dump(st.session_state["messages"], f)
        st.stop()
