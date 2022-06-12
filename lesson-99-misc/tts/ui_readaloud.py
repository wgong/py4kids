"""
How to run:

1) download this script to your local environment

2) install streamlit 
    $ pip install streamlit streamlit-option-menu pdfplumber python-docx
    or
    $ pip install -r requirements-readaloud.txt

3) launch the app
    $ streamlit run ui_readaloud.py

4) browse to http://localhost:8501

"""

import streamlit as st
from streamlit_option_menu import option_menu
import pdfplumber
import docx
from io import StringIO, BytesIO
# import pandas as pd
# import platform
# import socket
import urllib
from bs4 import BeautifulSoup
from os.path import splitext

import pyttsx3

# Initial page config
st.set_page_config(
     page_title='Streamlit Text-to-Speech',
     layout="wide",
     initial_sidebar_state="expanded",
)

def _rename_voice(nm):
    return ' - '.join(reversed([i.strip() for i in nm.split('-')]))

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

def do_welcome():
    st.subheader("Welcome to ReadAloud Tool")
    st.markdown("""
    This app is built on [<span style="color:red">__streamlit__ </span>](https://streamlit.io/) data app framework 
    and [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/engine.html) python pkg
    to listen to text document rather than read.
    """, unsafe_allow_html=True)

def do_tts():
    st.subheader('Read Text')
    engine, voice_map = get_engine()
    voice_name = st.session_state["voice_name"] if "voice_name" in st.session_state else list(voice_map.keys())[0]
    voice_rate = st.session_state["voice_rate"] if "voice_rate" in st.session_state else 200
    voice_volume = st.session_state["voice_volume"] if "voice_volume" in st.session_state else 1.0

    col_left,col_right = st.columns([3,1])

    readme_text = SAMPLE_TEXT
    with col_right:
        uploaded_file = st.file_uploader("Upload a document file in .txt, .docx, .pdf format")
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_ext = splitext(file_name)[-1]
            file_type = uploaded_file.type
            st.write(f"file_name={file_name}, file_ext={file_ext}, file_type = {file_type}")

            # pdf2txt - https://stackoverflow.com/questions/55767511/how-to-extract-text-from-pdf-in-python-3-7
            if file_type == "application/pdf" or file_ext == ".pdf":
                pdf = pdfplumber.open(BytesIO(uploaded_file.getvalue()))
                texts = []
                for page in pdf.pages:
                    text = page.extract_text()
                    texts.append(text)
                pdf.close()
                # st.write(texts)
                readme_text = "\n".join(texts)

            # docx2txt - http://automatetheboringstuff.com/chapter13/
            elif file_type == "application/octet-stream" and file_ext == ".docx":
                doc = docx.Document(BytesIO(uploaded_file.getvalue()))
                texts = []
                for para in doc.paragraphs:
                    texts.append(para.text)
                readme_text = "\n".join(texts)

            # text
            elif file_type == "text/plain" or file_ext == ".txt":
                readme_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            
    with col_left:
        with st.form(key='read_me'):
            readme_text = st.text_area('', value=readme_text, height=200, key="readme_text")
            if st.form_submit_button("Listen"): 
                for txt in [l.strip() for l in readme_text.split('\n') if l.strip()]:
                    engine.setProperty('voice', voice_map[voice_name])
                    engine.setProperty('rate', voice_rate)
                    engine.setProperty('volume', voice_volume)
                    engine.say(txt)
                engine.runAndWait()

        # if st.button("Stop"):
        #     if engine.isBusy():
        #         engine.stop()
        #     # st.stop()

def do_fetch_text():
    st.subheader('Fetch Text from a Web URL')
    with st.form(key='fetch_text'):
        webpage_url = st.text_input("Web URL:", value="", key="webpage_url")
        if st.form_submit_button("Fetch Text"):
            st.session_state["url_text"] = _fetch_text_from_url(webpage_url)

    url_text = st.text_area('Text:', value=st.session_state.get("url_text", ""), height=100, key="url_text")
    with st.form(key='save_text'):
        file_name = st.text_input("Filename", value="Untitled.txt", key="file_name")
        if url_text.strip() and st.form_submit_button("Save"):
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(url_text.strip()) 

menu_dict = {
    "Welcome": {"fn": do_welcome, "icon": "caret-right-square"},
    "Text-to-Speech": {"fn": do_tts, "icon": "chat-text-fill"},
    "Fetch Text": {"fn": do_fetch_text, "icon": "cloud-download"},
}

## Menu
def do_sidebar():

    options = list(menu_dict.keys())
    icons = [menu_dict[i]["icon"] for i in options]
    # st.write(icons)

    with st.sidebar:
        menu_item = option_menu("ReadAloud", options, 
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
            st.radio("Voice", sorted(list(voice_map.keys())), index=1, key="voice_name")
            st.slider("Rate", min_value=100, max_value=300, value=200, step=20, key="voice_rate")
            st.slider("Volume", min_value=0.0, max_value=1.0, value=1.0, step=0.2, key="voice_volume")
            
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
