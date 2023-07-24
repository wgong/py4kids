import streamlit as st
from io import StringIO 
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
from datetime import datetime

DEBUG_FLAG = False
NOISE_WORDS = ['Copy code','Copy']
CHAT_SCHEMA = ["ChatBot", "SessionTitle", "TimeStamp", "SeqNum", "Question", "Answer"]
CHAT_BOTS = ["Claude"]
SUPPORTED_CHAT_BOTS = ["Claude"]

def convert_df2csv(df, index=True):
    return df.to_csv(index=index).encode('utf-8')

def create_new_cell(contents):
    # https://discourse.jupyter.org/t/how-to-programmatically-add-serveral-new-cells-in-a-notebook-in-jupyterlab/4323
    from IPython.core.getipython import get_ipython
    shell = get_ipython()
    payload = dict(
        source='set_next_input',
        text=contents,
        replace=False,
    )
    shell.payload_manager.write_payload(payload, single = False)

def convert_htm2txt(html_txt):
    return html.fromstring(html_txt).text_content().strip()

def is_noise_word(html_txt):
    return convert_htm2txt(html_txt) in NOISE_WORDS
    
st.set_page_config(
     page_title='Save Claude chat',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    INPUT_FILENAME = ""
    cells = []

    st.subheader("Import Chat Records")

    c0, c1 = st.columns([6,4])
    with c1:
        st.markdown("""##### <span style="color:green">Upload a saved chat HTML file</span>""", unsafe_allow_html=True)
        bot_name = st.selectbox("Select ChatBot Name", CHAT_BOTS, index=0)

        if bot_name not in SUPPORTED_CHAT_BOTS:
            st.error(f"Unsupported Chatbot: {bot_name}")
            return

        txt_file = st.file_uploader("", key="upload_txt")

        if txt_file is not None:
            INPUT_FILENAME = txt_file.name
            # To convert to a string based IO:
            html_txt = StringIO(txt_file.getvalue().decode("utf-8")).read()
            
            soup = BeautifulSoup(html_txt, "html.parser")
            results = soup.findAll("div", class_="contents")
            
            for i in range(len(results)):
                v = results[i].prettify()
                if is_noise_word(v): continue
                # important to preserve HTML string because python code snippets are formatted
                cells.append(v)
                
    if not cells or not INPUT_FILENAME:
        return

    with c0:
        session_title = " ".join(INPUT_FILENAME.split(".")[:-1])
        st.markdown(f"""##### <span style="color:green">{session_title}</span>
- {int(len(cells)/2)} questions are asked in this session
            """, unsafe_allow_html=True)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_data = []
    seq_num = 1
    for i in range(0, len(cells), 2):
        st.markdown(f"""##### <span style="color:red">Q [{seq_num}] :</span>""", unsafe_allow_html=True)
        st.markdown(cells[i], unsafe_allow_html=True)
        st.markdown(f"""##### <span style="color:blue">A [{seq_num}] :</span>""", unsafe_allow_html=True)
        st.markdown(cells[i+1], unsafe_allow_html=True)
        chat_data.append([bot_name, session_title, ts, seq_num, cells[i], cells[i+1]])
        seq_num += 1

    if not chat_data: return

    df_chat = pd.DataFrame(chat_data, columns=CHAT_SCHEMA)
    if DEBUG_FLAG:
        st.dataframe(df_chat)

    st.markdown("""#### <span style="color:green">Download chat to a CSV file</span>""", unsafe_allow_html=True)
    if chat_data and INPUT_FILENAME:
        out_filename = ".".join(INPUT_FILENAME.split(".")[:-1]) + ".csv"
        st.download_button(
            label="Download",
            data=convert_df2csv(df_chat, index=False),
            file_name=out_filename,
            mime='text/csv',
        )

if __name__ == "__main__":
    main()