"""
How to run:
1) download this script to your local environment
2) install streamlit 
    $ pip install -r requirements-app.txt
3) launch the app
    $ streamlit run ui_app.py
4) browse to http://localhost:8501
"""

import streamlit as st
from streamlit_option_menu import option_menu
from io import StringIO, BytesIO
# import pandas as pd
from os.path import splitext

# Initial page config
st.set_page_config(
     page_title='Streamlit App',
     layout="wide",
     initial_sidebar_state="expanded",
)


SAMPLE_TEXT = """
Thank you for using text-to-speech tool.
感谢您使用文字转语音工具。
Vielen Dank, dass Sie das Text-zu-Sprache-Tool verwenden.
"""
# cached functions
# @st.experimental_singleton
def get_engine():
    pass
    

def do_welcome():
    st.subheader("Welcome to ReadAloud Tool")
    st.markdown("""
    This app is built on [<span style="color:red">__streamlit__ </span>](https://streamlit.io/) data app framework 
    and [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/engine.html) python pkg
    to listen to text document rather than read.
    """, unsafe_allow_html=True)

def do_tts():
    pass

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
            st.slider("Rate (default=200)", min_value=100, max_value=300, value=200, step=20, key="voice_rate")
            st.slider("Volume (default=1.0)", min_value=0.0, max_value=1.0, value=1.0, step=0.2, key="voice_volume")
            
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
