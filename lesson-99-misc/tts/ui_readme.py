"""
How to run:

1) download this script to your local environment

2) install streamlit and readme via
    $ pip install streamlit streamlit-option-menu readme identity 

3) launch the app via
    $ streamlit run ui_readme.py

4) browse to http://localhost:8501

"""
__author__ = 'Wen_Gong@vanguard.com'


import streamlit as st
from streamlit_option_menu import option_menu

from io import StringIO
# import pandas as pd
# import platform
# import socket
import urllib
from bs4 import BeautifulSoup

# Vanguard pkg
# from identity import Identity as id_
import pyttsx3

# Initial page config
st.set_page_config(
     page_title='Streamlit Text-to-Speech',
     layout="wide",
     initial_sidebar_state="expanded",
)

def _rename_voice(nm):
    return ' - '.join(reversed([i.strip() for i in nm.split('-')]))

# _CURRENT_USER = id_.username.casefold()
SAMPLE_TEXT = """
Thank you for using text-to-speech tool.
感谢您使用文字转语音工具。
Vielen Dank, dass Sie das Text-zu-Sprache-Tool verwenden.
"""
# cached functions
# @st.experimental_singleton
def get_engine():
    engine = pyttsx3.init()
    voice_map = dict()
    # one-time fix for my laptop where Chinese (Taiwan) is not removed, it actually points to German
    # hostname = socket.gethostname()
    for voice in engine.getProperty('voices'):
        voice_nm = voice.name.replace("Microsoft ", "").replace("Desktop ", "")
        voice_map[_rename_voice(voice_nm)] = voice.id
    return engine, voice_map

def _fetch_text_from_url(url):
    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request)
    soup = BeautifulSoup(content)
    return soup.body.get_text()    

def _parse_uids(uids):
    return sorted(list(set([r.strip().upper() for r in uids.replace(","," ").replace(";"," ").split() if r.strip()])))

def do_welcome():
    st.header("Welcome to ReadMe Tool")
    st.markdown("""
    This app is built on [<span style="color:red">__streamlit__ </span>](https://streamlit.io/) data app framework 
    and [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/engine.html) python pkg
    to listen to text document rather than read.

    """, unsafe_allow_html=True)



def do_tts():
    st.header('Read Text to Me')
    engine, voice_map = get_engine()
    voice_name = st.session_state["voice_name"] if "voice_name" in st.session_state else list(voice_map.keys())[0]

    col_left,col_right = st.columns([3,1])

    readme_text = SAMPLE_TEXT
    with col_right:
        uploaded_file = st.file_uploader("Upload a text file (.txt, .doc, .pdf)")
        if uploaded_file is not None:
            readme_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()

            # TODO: add logic to extract text from .docx and .pdf
            # http://automatetheboringstuff.com/chapter13/
            # pdf2txt - https://stackoverflow.com/questions/55767511/how-to-extract-text-from-pdf-in-python-3-7
            # 
            
    with col_left:

        # with st.form(key='fetch_text'):
        #     webpage_url = st.text_input("Webpage URL:", value="", key="webpage_url")
        #     if st.form_submit_button("Fetch Text"):
        #         url_text = _fetch_text_from_url(webpage_url)

        with st.form(key='read_me'):
            readme_text = st.text_area('Text to Read (*):', value=readme_text, height=200, key="readme_text")
            if st.form_submit_button("ReadMe"): 
                for txt in [l.strip() for l in readme_text.split('\n') if l.strip()]:
                    engine.setProperty('voice', voice_map[voice_name])
                    engine.say(txt)
                engine.runAndWait()

        if st.button("Stop"):
            if engine.isBusy():
                engine.stop()

menu_dict = {
    "Welcome": {"fn": do_welcome, "icon": "caret-right-square"},
    "Text-to-Speech": {"fn": do_tts, "icon": "chat-text-fill"},
}

## Menu
def do_sidebar():

    options = list(menu_dict.keys())
    icons = [menu_dict[i]["icon"] for i in options]
    # st.write(icons)

    with st.sidebar:
        menu_item = option_menu("ReadMe", options, 
            icons=icons, menu_icon="volume-down", 
            default_index=0, 
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "maroon"},
            })
        st.session_state["menu_item"] = menu_item

        if menu_item == "Text-to-Speech":
            _, voice_map = get_engine()
            voice_name = st.radio("Which voice?", sorted(list(voice_map.keys())), index=1, key="voice_name")

## Body
def do_body():
    
    if "menu_item" in st.session_state:
        menu_item = st.session_state["menu_item"]
        if menu_item:
            menu_dict[menu_item]["fn"]()
    else:
        do_welcome()
       

def main():
    do_sidebar()
    do_body()

# Run main()
if __name__ == '__main__':
    main()