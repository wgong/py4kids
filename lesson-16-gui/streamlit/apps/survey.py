"""

# Streamlit Concepts
- https://docs.streamlit.io/library/get-started/main-concepts


# bootstrap icons
- https://icons.getbootstrap.com/

"""
__author__ = "Wen_Gong@vanguard.com"

import inspect
import platform

# my
import shutil
import subprocess
from functools import partial
from io import StringIO

# std
from os.path import splitext

import altair as alt
import keyring

# ds
import numpy as np
import pandas as pd
import streamlit as st

# vgi
from identity import Identity as id_
from PIL import Image
from st_aggrid import (
    AgGrid,
    DataReturnMode,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
)
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu

shutil.copy(
    "C:/work/bitbucket_extra/coworkers/WEN_GONG/work/SQL/dst_query_utils.py",
    "./dst_query_utils.py",
)
from dst_query_utils import *

# Initial page config
st.set_page_config(
    page_title="Streamlit Medallia",
    layout="wide",
    initial_sidebar_state="expanded",
)


_APPNAME = "medallia"
_CURRENT_USER = id_.username.casefold()


_FIX_FLAG = True
if _FIX_FLAG and platform.system().casefold() == "windows":
    # workaround for windows
    # https://stackoverflow.com/questions/61071022/pywintypes-com-error-2147221008-coinitialize-has-not-been-called-none-n
    import pythoncom
    import win32com.client

    xl = win32com.client.Dispatch(
        "Excel.Application", pythoncom.CoInitialize()
    )


# add more using https://github.com/okld/streamlit-ace/blob/main/streamlit_ace/__init__.py
LANGUAGE_MAP = {
    ".py": "python",
    ".sql": "sql",
    ".js": "javascript",
    ".java": "java",
    ".json": "json",
    ".html": "html",
    ".c": "c_cpp",
    ".cpp": "c_cpp",
    ".css": "css",
}


SYS_LVL = {"int": "e", "eng": "e", "test": "t", "prod": "p"}

# AWS_PROFILE = {
#     "eng" : {
#         "vgi-platform-int" : ["ACCTVIEWONLY", "SIAPPENGINEER", "EDPQUERY"],
#         "vgi-ess-eng" : ["ACCTVIEWONLY", "SIAPPENGINEER", "DSTANALYTICS"],
#     },
#     "test" : {
#         "vgi-platform-test" : ["ACCTVIEWONLY", "SIAPPDEVELOPER", "EDPQUERY"],
#         "vgi-ess-test" : ["ACCTVIEWONLY", "SIAPPDEVELOPER", "DSTANALYTICS"],
#     },
#     "prod" : {
#         "vgi-platform-prod" : ["ACCTVIEWONLY", "EDPQUERY"],
#         "vgi-ess-prod" : ["ACCTVIEWONLY", "DSTANALYTICS"],
#     },
# }

AWS_PROFILE = {
    "vgi-ess-eng": ["SIAPPENGINEER", "DSTANALYTICS"],
    "vgi-ess-test": ["SIAPPDEVELOPER", "DSTANALYTICS"],
    "vgi-ess-prod": ["DSTANALYTICS"],
}

# Aggrid options
_GRID_OPTIONS = {
    "grid_height": 400,
    "return_mode_value": DataReturnMode.__members__["FILTERED"],
    "update_mode_value": GridUpdateMode.__members__["MODEL_CHANGED"],
    "fit_columns_on_grid_load": False,
    "selection_mode": "single",  # "multiple",
    "allow_unsafe_jscode": True,
    "groupSelectsChildren": True,
    "groupSelectsFiltered": True,
    "enable_pagination": True,
    "paginationPageSize": 11,
}

_FORM_CONFIG = {
    "view": {"read_only": True, "key_pfx": "view", "selectable": True},
    "create": {"read_only": False, "key_pfx": "add", "selectable": False},
    "update": {"read_only": False, "key_pfx": "upd", "selectable": True},
    "delete": {"read_only": True, "key_pfx": "del", "selectable": True},
}

SCHEMA_MAP = {
    "medallia": [
        "data_src",
        "surveyid",
        "comments",
        "program",
        "segment",
        "positivity",
        "creationdate",
        "sentiment",
    ]
}

##
## Helper functions
###############################################################
def _prepare_grid(df, context="view"):
    enable_selection = _FORM_CONFIG[context]["selectable"]
    gb = GridOptionsBuilder.from_dataframe(df)
    if enable_selection:
        gb.configure_selection(
            _GRID_OPTIONS["selection_mode"],
            use_checkbox=True,
            groupSelectsChildren=_GRID_OPTIONS["groupSelectsChildren"],
            groupSelectsFiltered=_GRID_OPTIONS["groupSelectsFiltered"],
        )
    gb.configure_pagination(
        paginationAutoPageSize=False,
        paginationPageSize=_GRID_OPTIONS["paginationPageSize"],
    )
    gb.configure_grid_options(domLayout="normal")
    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),
        height=_GRID_OPTIONS["grid_height"],
        # width='100%',
        data_return_mode=_GRID_OPTIONS["return_mode_value"],
        update_mode=_GRID_OPTIONS["update_mode_value"],
        fit_columns_on_grid_load=_GRID_OPTIONS["fit_columns_on_grid_load"],
        allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
    )

    if enable_selection:
        selected_df = pd.DataFrame(grid_response["selected_rows"])
        return selected_df
    else:
        return None


def _gen_key(key_pfx, table_name, key_name=""):
    return f"{key_pfx}_{table_name}_{key_name}"


def _default_val(row, col_name):
    return row[col_name][0] if row and col_name in row else ""


def _form__build(ctx, row=None):
    key_pfx = _FORM_CONFIG[ctx]["key_pfx"]
    _disabled = _FORM_CONFIG[ctx]["read_only"]
    table_name = "medallia"
    st.text_area(
        "comments",
        value=_default_val(row, "comments"),
        key=_gen_key(key_pfx, table_name, "comments"),
        disabled=_disabled,
    )
    col_left, col_right = st.columns(2)
    with col_left:
        st.text_input(
            "sentiment",
            value=_default_val(row, "sentiment"),
            key=_gen_key(key_pfx, table_name, "sentiment"),
            disabled=_disabled if ctx != "update" else True,
        )
        st.text_input(
            "data_src",
            value=_default_val(row, "data_src"),
            key=_gen_key(key_pfx, table_name, "data_src"),
            disabled=_disabled,
        )
        st.text_input(
            "topic_id",
            value=_default_val(row, "topic_id"),
            key=_gen_key(key_pfx, table_name, "topic_id"),
            disabled=_disabled,
        )
    with col_right:
        st.text_input(
            "segment",
            value=_default_val(row, "segment"),
            key=_gen_key(key_pfx, table_name, "segment"),
            disabled=_disabled if ctx != "update" else True,
        )
        st.text_input(
            "program",
            value=_default_val(row, "program"),
            key=_gen_key(key_pfx, table_name, "program"),
            disabled=_disabled,
        )
        st.text_area(
            "topic_terms",
            value=_default_val(row, "topic_terms"),
            key=_gen_key(key_pfx, table_name, "topic_terms"),
            disabled=_disabled,
        )


def _make_sentiment_filename(filename):
    if not filename:
        return "_sentiment.csv"

    tmp = filename.split(".")
    return f"{'.'.join(tmp[0:-1])}_sentiment.{tmp[-1]}"


def _gen_csv_filename_from_sql(sql):
    words = sql.lower()
    if not "from" in words:
        fn = "data"
    else:
        words = words.split()
        for n, w in enumerate(words):
            if w == "from":
                n += 1
                break
        fn = words[n].split(".")[-1]
    now = datetime.now()
    return f"{fn}_{now:%Y-%m-%d-%H-%M-%S}.csv"


def _get_lang(file_ext, file_type):
    "return lang for accepted files: text, sql, py"
    if file_type == "application/octet-stream" and file_ext.lower() == ".sql":
        lang = "sql"
    elif file_type == "text/plain":
        lang = LANGUAGE_MAP.get(file_ext.lower(), "plain_text")
    else:
        lang = None
    return lang


def _show_editor_settings():
    with st.expander("Editor settings"):
        st.selectbox(
            "Language",
            options=["plain_text"] + sorted(list(LANGUAGE_MAP.values())),
            index=0,
            key="ace_lang",
        )
        st.selectbox(
            "Theme",
            options=["pastel_on_dark", "chrome"],
            index=0,
            key="ace_theme",
        )
        st.select_slider(
            "Height",
            options=[str(i * 100) for i in range(3, 7)],
            key="ace_height",
        )
        st.select_slider(
            "Font", options=[str(i) for i in range(14, 19, 2)], key="ace_font"
        )
        st.select_slider("Tab", options=[2, 4, 8], key="ace_tab")
        st.checkbox("Readonly", value=False, key="ace_readonly")
        st.checkbox("Auto-update", value=False, key="ace_autoupdate")
        st.checkbox("Wrap", value=False, key="ace_wrap")
        st.checkbox("Show gutter", value=True, key="ace_gutter")

def _clear_cache(pfx="df_"):
    cached_data = []
    cached_keys = []
    for k in st.session_state.keys():
        if k.startswith(pfx):
            cached_keys.append(k)
            cached_data.append(st.session_state[k])
    del cached_data
    for k in cached_keys:
        st.session_state[k] = {}
        del st.session_state[k]

def aws_sentiments_batch(
    comprehend, df, col_map={"id": "surveyid", "comment": "comments"}
):
    """
    This function feeds a list of 'comment' texts to AWS Comprehend batch_detect_sentiment() API
    and adds sentiment score.

    Args:
        comprehend: boto3 client obj
        Input dataframe must contain (id,comment) fields mapped per
            col_map={"id":"surveyid", "comment":"comments"}

    Returns:
        A tuple of (dataframe, msg) with sentiment.

    Note: Abort processing if batch_detect_sentiment() calls failed more than 3 times.
    """
    CHUNK_SIZE = comprehend.get_limits()["MAX_DOC_LIST"]
    COLUMNS = [
        col_map["id"],
        col_map["comment"],
        "sentiment",
    ]  # 0: id, 1: text, 2: sentiment
    df_columns = df.columns
    if col_map["id"] not in df_columns or col_map["comment"] not in df_columns:
        raise Exception(
            f"{list(col_map.values())} not matched with {list(df_columns)}"
        )

    df = df[~df[COLUMNS[1]].isnull()]  # remove null
    dic_id_comment = df[[COLUMNS[0], COLUMNS[1]]].to_dict("list")
    id_list, comments_list = (
        dic_id_comment[COLUMNS[0]],
        dic_id_comment[COLUMNS[1]],
    )

    dic_sent = {}
    num_recs = 0
    start = datetime.now()

    err_msg = []
    err_chunks = 0
    MAX_FAILED_CHUNKS = 3
    for n in range(0, len(id_list), CHUNK_SIZE):

        text_list = comments_list[n : n + CHUNK_SIZE]
        results, errors = comprehend.batch_detect_sentiment(TextList=text_list)

        if results:
            for r in results:
                idx = n + r["Index"]
                dic_sent[id_list[idx]] = r["Sentiment"]
        else:
            err_msg.append(f"results is None: {n}:{n+CHUNK_SIZE}")
            err_chunks += 1

        if errors:
            err_msg.append(str(errors))
            # for e in errors:
            #    idx = n+e['Index']
            #    dic_sent[id_list[idx]] = None

        num_recs += len(text_list)

        # stop processing if failed more than 3 times
        if err_chunks > MAX_FAILED_CHUNKS:
            break

    stop = datetime.now()
    rec_sec = num_recs / (stop - start).total_seconds()

    msg = f"""start = {start}, 
    stop = {stop}, 
    processing {num_recs} rows took {(stop  - start).total_seconds()} secs at a speed of 
    {rec_sec} rows per sec
    
    """
    if len(err_msg):
        msg += f"""\nErrors:\n{err_msg}"""

    data = []
    for k, v in dic_sent.items():
        data.append([k, v])
    df_sent = pd.DataFrame(data, columns=[COLUMNS[0], COLUMNS[2]])
    df_out = pd.merge(df, df_sent, on=[COLUMNS[0]], how="inner")

    return df_out, msg


# @st.experimental_singleton
# def _copy_dst_query_utils():
#     import shutil
#     shutil.copy("C:/work/bitbucket_extra/coworkers/WEN_GONG/work/SQL/dst_query_utils.py", "./dst_query_utils.py")
#     from dst_query_utils import *
### SyntaxError: import * only allowed at module level

# cached functions


def is_valid_cred(username, passwd):
    system = platform.system().casefold()
    validator = partial(subprocess.run, shell=True, check=True)
    if system == "windows":
        proc = validator(
            [
                "powershell.exe",
                "-command",
                f'(new-object directoryservices.directoryentry "", {username}, {passwd}).psbase.name -ne $null',
            ],
            stdout=subprocess.PIPE,
        )
        retcode = 0 if b"True" in proc.stdout else 1
    elif system == "darwin":
        retcode = validator(
            [f"dscl /Local/Default -authonly {username} {passwd}"]
        ).returncode
    elif system == "linux":
        retcode = validator([f"su {username}"], input=passwd.encode())
    else:
        raise OSError(
            f"Unsupported OS (system) '{system}', "
            "please submit a feature request."
        )
    return True if retcode == 0 else False


def clear_login_form():
    keyring.delete_password(_APPNAME, st.session_state["vg_username"])
    st.session_state["vg_username"] = ""
    st.session_state["vg_password"] = ""


def do_welcome():
    st.header("Welcome")
    st.markdown(
        """
    This data app is built on [streamlit](http://streamlit.io) framework to explore Medallia survey data.

    AWS Comprehend NLP tool is used for sentiment analysis and topic model.
    """,
        unsafe_allow_html=True,
    )

    st.write("package dependency:")
    for line in open("requirements-ui_medallia.txt").read().split("\n"):
        st.write("\t" + line)


def do_query_data():

    st.header("Query data")

    ## editor
    orig_text = """SELECT 
    'medallia_csat_clean' "data_src",
    m.a_surveyid  "surveyid",
    m.q_vgrig_transactional_reason_rate_cmt "comments",
    length(m.q_vgrig_transactional_reason_rate_cmt) "comment_size",
    m.e_vgrig_transactional_program_type  "program",
    m.e_vgrig_transactional_asset_segment "segment",
    m.q_vgrig_transactional_positivity_of_exp "positivity",
    m.q_vgrig_transactional_eff_meet_needs  "eff_scale",
    m.e_creationdate  "creationdate"
    FROM retail_medallia.medallia_csat_clean m 
    where m.q_vgrig_transactional_reason_rate_cmt is not null
    and m.e_creationdate between parse_datetime('2021-12-01', 'yyyy-MM-dd') 
        and parse_datetime('2021-12-31', 'yyyy-MM-dd')
--limit 500
;
    """
    col_editor, col_settings = st.columns([5, 2])
    lang = st.session_state.get("ace_lang", "plain_text")
    with col_settings:

        _show_editor_settings()

        uploaded_file = st.file_uploader("Open SQL file")
        if uploaded_file is not None:
            # st.write(uploaded_file)
            file_name = uploaded_file.name
            file_ext = splitext(file_name)[-1]
            file_type = uploaded_file.type
            file_size = uploaded_file.size

            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)
            lang_detected = _get_lang(file_ext, file_type)
            if not lang_detected:
                st.error(
                    "File not supported by ACE editor: type={file_type}, ext={file_ext}"
                )
            else:
                lang = lang_detected
                # To read file as string:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                #  st.write(stringio)
                orig_text = stringio.read()
                # st.code(orig_text)

    with col_editor:

        # display text in ACE editor
        # st.write("Ace editor")
        sql_text = st_ace(
            value=orig_text,
            language="sql",
            theme=st.session_state.get("ace_theme", "pastel_on_dark"),
            height=int(st.session_state.get("ace_height", "500")),
            font_size=int(st.session_state.get("ace_font", "14")),
            tab_size=int(st.session_state.get("ace_tab", "4")),
            readonly=st.session_state.get("ace_readonly", False),
            auto_update=st.session_state.get("ace_autoupdate", False),
            wrap=st.session_state.get("ace_wrap", False),
            show_gutter=st.session_state.get("ace_gutter", True),
        )

    # Execute SQL
    if "pconn" in st.session_state and "hconn" in st.session_state:
        pconn = st.session_state["pconn"]
        hconn = st.session_state["hconn"]

        if st.session_state["EXECUTE_ALL_SQLS"]:
            btn_execute_all = st.button("Execute All SQLs", key=f"execute_sql")
            if btn_execute_all:
                for n, sql_stmt in enumerate(
                    [s.strip() for s in sql_text.split(";") if s.strip()]
                ):
                    st.code(sql_stmt)
                    try:
                        st.session_state[f"df_sql_{n}"] = pd.read_sql(
                            sql_stmt, pconn
                        )
                        st.dataframe(st.session_state[f"df_sql_{n}"])
                        st.download_button(
                            "Download",
                            data=st.session_state[f"df_sql_{n}"].to_csv(),
                            mime="text/csv",
                            file_name=_gen_csv_filename_from_sql(sql_stmt),
                        )
                    except:
                        st.error(
                            f"Try with Hive connection since Presto connection has the following issue:\n{format_exc()}"
                        )
                        try:
                            st.session_state[f"df_sql_{n}"] = pd.read_sql(
                                sql_stmt, hconn
                            )
                            st.dataframe(st.session_state[f"df_sql_{n}"])
                            st.download_button(
                                "Download",
                                data=st.session_state[f"df_sql_{n}"].to_csv(),
                                mime="text/csv",
                                file_name=_gen_csv_filename_from_sql(sql_stmt),
                            )
                        except:
                            st.error(
                                f"Hive connection has the following issue:\n{format_exc()}"
                            )

        else:
            for n, sql_stmt in enumerate(
                [s.strip() for s in sql_text.split(";") if s.strip()]
            ):
                st.code(sql_stmt)
                btn_execute = st.button("Execute SQL", key=f"execute_sql_{n}")
                if btn_execute:
                    try:
                        st.session_state[f"df_sql_{n}"] = pd.read_sql(
                            sql_stmt, pconn
                        )
                        st.dataframe(st.session_state[f"df_sql_{n}"])
                        st.download_button(
                            "Download",
                            data=st.session_state[f"df_sql_{n}"].to_csv(),
                            mime="text/csv",
                            file_name=_gen_csv_filename_from_sql(sql_stmt),
                        )
                    except:
                        st.error(
                            f"Try with Hive connection since Presto connection has the following issue:\n{format_exc()}"
                        )
                        try:
                            st.session_state[f"df_sql_{n}"] = pd.read_sql(
                                sql_stmt, hconn
                            )
                            st.dataframe(st.session_state[f"df_sql_{n}"])
                            st.download_button(
                                "Download",
                                data=st.session_state[f"df_sql_{n}"].to_csv(),
                                mime="text/csv",
                                file_name=_gen_csv_filename_from_sql(sql_stmt),
                            )
                        except:
                            st.error(
                                f"Hive connection has the following issue:\n{format_exc()}"
                            )


def do_eda():
    st.header("Exploratory Data Analysis")

    st.subheader("Survey Data")
    b_use_grid = (
        st.session_state["EXPLORE_USE_GRID"]
        if "EXPLORE_USE_GRID" in st.session_state
        else False
    )
    b_show_chart_sentiment = (
        st.session_state["EXPLORE_SHOW_CHART_SENTIMENT"]
        if "EXPLORE_SHOW_CHART_SENTIMENT" in st.session_state
        else False
    )
    b_show_chart_topic = (
        st.session_state["EXPLORE_SHOW_CHART_TOPIC"]
        if "EXPLORE_SHOW_CHART_TOPIC" in st.session_state
        else False
    )

    selected_row = {}
    CONTEXT = "view"
    col_left, col_right = st.columns([4, 1])
    with col_right:
        uploaded_file = st.file_uploader(
            "Choose data file", type=["csv", "xlsx"]
        )
        # st.write(uploaded_file)
        if uploaded_file is not None:
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type == "csv":
                st.session_state["df_eda"] = pd.read_csv(uploaded_file)
                # df = pd.read_csv(StringIO(uploaded_file.getvalue().decode("utf-8")))
            elif file_type in ["xlsx"]:
                st.session_state["df_eda"] = pd.read_excel(
                    uploaded_file, engine="openpyxl"
                )
    with col_left:

        if "df_eda" in st.session_state:
            df = st.session_state["df_eda"]
            if "comment_size" not in df.columns and "comments" in df.columns:
                df["comment_size"] = df["comments"].apply(lambda x: len(x))
            if b_use_grid:
                # use AgGrid
                selected_row = _prepare_grid(df, context=CONTEXT).to_dict()
            else:
                st.dataframe(df)

        else:
            st.empty()

    if "df_eda" not in st.session_state or len(st.session_state["df_eda"]) < 1:
        return

    df = st.session_state["df_eda"]

    # show form
    if b_use_grid and selected_row:
        st.subheader("Form")
        _form__build(CONTEXT, row=selected_row)

    # show charts
    if "sentiment" in df.columns:
        if b_show_chart_sentiment and "df_eda" in st.session_state:
            st.subheader("Charts - Sentiments")
            df = st.session_state["df_eda"]
            # histogram on categorical columns
            for col in ["data_src", "program", "segment", "sentiment"]:
                st.subheader(f"{col}")
                c = (
                    alt.Chart(df)
                    .mark_bar()
                    .encode(y=f"{col}:N", x="count()", color="sentiment")
                )
                st.altair_chart(c, use_container_width=True)

            # scatter segment vs program
            st.subheader(f"segment vs program: ")
            for sent in ["POSITIVE", "NEGATIVE"]:
                df2 = df[df["sentiment"] == sent]
                c2 = (
                    alt.Chart(df2)
                    .mark_circle()
                    .encode(
                        y="segment:N",
                        x="program:N",
                        color="sentiment",
                        size="count()",
                        row="sentiment",
                    )
                )
                st.altair_chart(c2, use_container_width=True)

    if "topic_id" in df.columns:
        if b_show_chart_topic and "df_eda" in st.session_state:
            st.subheader("Charts - Topics")
            df = st.session_state["df_eda"]
            st.write(df[["topic_id", "topic_terms"]].value_counts())

            # histogram on categorical columns
            for col in ["data_src", "program", "segment", "sentiment"]:
                st.subheader(f"{col}")
                c = (
                    alt.Chart(df)
                    .mark_bar()
                    .encode(y=f"{col}:N", x="count()", color="topic_id")
                )
                st.altair_chart(c, use_container_width=True)


def do_sentiment():
    st.header(f"Sentiment Analysis")

    if "df_sent" not in st.session_state:
        st.write(
            "Please upload a spreadsheet with text data to begin sentiment analysis ..."
        )

    b_show_msg = (
        st.session_state["SENTIMENT_SHOW_MSG"]
        if "SENTIMENT_SHOW_MSG" in st.session_state
        else False
    )

    col_left, col_right = st.columns([4, 1])
    filename_input = ""
    with col_right:
        aws_accounts = sorted(list(AWS_PROFILE.keys()))
        default_idx = 0
        for idx, acct in enumerate(aws_accounts):
            if acct.endswith("-eng"):
                default_idx = idx
        aws_account = st.selectbox(
            "AWS account:", aws_accounts, index=default_idx, key="aws_accounts"
        )

        anti_roles = AWS_PROFILE[aws_account]
        default_idx2 = 0
        for idx2, role2 in enumerate(anti_roles):
            if role2.startswith("SIAPP"):
                default_idx2 = idx2
        aws_role = st.selectbox(
            "Antiphony role:", anti_roles, index=default_idx2, key="aws_role"
        )

        # handle file-upload
        uploaded_file = st.file_uploader(
            "Choose data file", type=["csv", "xlsx"]
        )
        if uploaded_file is not None:
            filename_input = uploaded_file.name
            file_type = filename_input.split(".")[-1].lower()
            if file_type == "csv":
                st.session_state["df_sent"] = pd.read_csv(uploaded_file)
                # df = pd.read_csv(StringIO(uploaded_file.getvalue().decode("utf-8")))
            elif file_type in ["xlsx"]:
                st.session_state["df_sent"] = pd.read_excel(
                    uploaded_file, engine="openpyxl"
                )
    with col_left:
        if "df_sent" in st.session_state:
            df_sent = st.session_state["df_sent"]
            # st.write(df_sent)
            if len(df_sent) < 1:
                return

            if "comment_size" not in df_sent.columns:
                df_sent["comment_size"] = df_sent["comments"].apply(
                    lambda x: len(x)
                )

            if st.button("Calculate sentiment"):

                with st.spinner("running ..."):
                    from vg_nlp_toolbox.utils import Comprehend

                    aws_region = "us-east-1"
                    comprehend = Comprehend(aws_account, aws_role, aws_region)
                    df_sent, msg = aws_sentiments_batch(comprehend, df_sent)

                    if b_show_msg and msg:
                        st.info(msg)

                st.session_state["df_sent"] = df_sent  # update

            st.dataframe(df_sent)

            file_sent_csv = _make_sentiment_filename(filename_input)
            st.download_button(
                "Download",
                data=df_sent.to_csv(),
                mime="text/csv",
                file_name=file_sent_csv,
            )

        else:
            st.empty()


def do_topic():
    st.header(f"Topic Model")

    st.markdown(
        """
    [AWS Comprehend - Topic Modeling](https://docs.aws.amazon.com/comprehend/latest/dg/topic-modeling.html) service is used,
    which involves:
    - Upload text data csv file(s) to S3 bucket
    - Configure and submit the analysis job for topic modeling
    - Download and extract result file
    - Merge topic results with the original input text file

    See an example at [medallia_topic_model-aws-automate.ipynb](https://bitbucket.opst.c1.vanguard.com/users/u8hi/repos/work/browse/jupyter-notebooks/NLP/medallia_topic_model-aws-automate.ipynb)
    """,
        unsafe_allow_html=True,
    )

    aws_comprehend_job_img = "aws-comprehend-analysis-job-topic-model.png"
    st.image(Image.open(aws_comprehend_job_img))


def do_edit():
    st.header(f"Edit Code")
    st.write(f"{__file__}")
    orig_content = open(__file__).read()
    content = st_ace(
        value=orig_content,
        language="python",
        theme=st.session_state.get("ace_theme", "pastel_on_dark"),
        height=int(st.session_state.get("ace_height", "400")),
        font_size=int(st.session_state.get("ace_font", "14")),
        tab_size=int(st.session_state.get("ace_tab", "4")),
        readonly=False,
        auto_update=st.session_state.get("ace_autoupdate", False),
        wrap=st.session_state.get("ace_wrap", False),
        show_gutter=st.session_state.get("ace_gutter", True),
    )

    if st.button("Save"):
        open(__file__, "w").write(content)

    _show_editor_settings()


# place this after fn defined
st_handler_map = {
    "Welcome": {"fn": do_welcome, "icon": "caret-right-square"},
    "Query Data": {"fn": do_query_data, "icon": "cloud-download"},
    "Sentiment": {"fn": do_sentiment, "icon": "arrows-expand"},
    "Topic Model": {"fn": do_topic, "icon": "body-text"},
    "Analyze": {"fn": do_eda, "icon": "list-task"},
    "Edit Code": {"fn": do_edit, "icon": "pencil-square"},
}


def do_login():

    ## handle Login
    with st.sidebar.form(key="login_form"):
        vg_username = st.text_input(
            "Username", value=_CURRENT_USER, key="vg_username"
        ).casefold()
        vg_password = st.text_input(
            "Password", type="password", key="vg_password"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Login"):
                if is_valid_cred(vg_username, vg_password):
                    # update keyring
                    keyring.set_password(
                        "vgidentity", vg_username, vg_password
                    )
                    # use keyring to store sailpoint login session
                    keyring.set_password(_APPNAME, vg_username, "OK")
                else:
                    st.sidebar.warning("Invalid cred")
                    # remove sailpoint login session
                    try:
                        keyring.delete_password(_APPNAME, vg_username)
                    except:
                        pass
        with col2:
            logout = st.form_submit_button("Logout", on_click=clear_login_form)


## Menu
def do_sidebar():

    do_login()

    login_result = keyring.get_password(
        _APPNAME, st.session_state["vg_username"]
    )
    if login_result is not None and login_result == "OK":
        menu_item = st.empty()
        st.sidebar.text(f"Logged in")

        menu_options = list(st_handler_map.keys())
        icons = [st_handler_map[i]["icon"] for i in menu_options]

        with st.sidebar:
            menu_item = option_menu(
                "Medallia Survey",
                menu_options,
                icons=icons,
                menu_icon="bounding-box",
                default_index=0,
                key="menu_item",
            )

            if menu_item == "Query Data":
                USE_DST_DAILY_CLUSTER = st.checkbox(
                    "Use DST Daily Cluster",
                    value=True,
                    key="USE_DST_DAILY_CLUSTER",
                )
                if USE_DST_DAILY_CLUSTER:
                    # st.session_state["master_dns"] = 'dst-daily-cluster.us-east-1.essp.c1.vanguard.com'

                    # Skip spin up cluster if you use existing cluster
                    master_dns = (
                        "dst-daily-cluster.us-east-1.essp.c1.vanguard.com"
                    )

                    json_dict = EMR_JSON_DICT["DST_Daily_Cluster"]
                else:
                    master_dns = st.text_input(
                        "Master DNS:",
                        value="dst-daily-cluster.us-east-1.essp.c1.vanguard.com",
                        key="master_dns",
                    )

                    json_dict = {
                        "hive_parameters": {"hive.execution.engine": "mr"}
                    }

                st.checkbox(
                    "Execute All SQLs once",
                    value=False,
                    key="EXECUTE_ALL_SQLS",
                )

                col_left, col_right = st.columns(2)
                with col_left:
                    btn_connect = st.button("Connect")
                    if btn_connect:
                        try:
                            hconn, pconn = establish_conn(
                                json_dict, master_dns
                            )
                            if "pconn" not in st.session_state:
                                st.session_state["pconn"] = pconn
                            if "hconn" not in st.session_state:
                                st.session_state["hconn"] = hconn
                        except:
                            st.error(format_exc())

                with col_right:
                    btn_disconnect = st.button("Disconnect")
                    if btn_disconnect:
                        del [
                            st.session_state["pconn"],
                            st.session_state["hconn"],
                        ]

                if "pconn" in st.session_state and st.session_state["pconn"]:
                    cursor_state = "Connected!"
                else:
                    cursor_state = "Not connected!"
                st.info(cursor_state)

                if st.button("Clear Cache"):
                    _clear_cache(pfx="df_sql")


            if menu_item == "Analyze":
                st.checkbox("Use Grid", value=False, key="EXPLORE_USE_GRID")
                st.checkbox(
                    "Show Chart: Sentiment",
                    value=False,
                    key="EXPLORE_SHOW_CHART_SENTIMENT",
                )
                st.checkbox(
                    "Show Chart: Topic",
                    value=False,
                    key="EXPLORE_SHOW_CHART_TOPIC",
                )

                if st.button("Clear Cache"):
                    _clear_cache(pfx="df_eda")

            if menu_item == "Sentiment":
                st.checkbox(
                    "Show Message", value=False, key="SENTIMENT_SHOW_MSG"
                )
                if st.button("Clear Cache"):
                    _clear_cache(pfx="df_sent")


## Body
def do_body():

    login_result = keyring.get_password(
        _APPNAME, st.session_state["vg_username"]
    )
    if login_result == "OK" and "menu_item" in st.session_state:
        menu_item = st.session_state["menu_item"]
        if menu_item and "fn" in st_handler_map[menu_item]:
            st_handler = st_handler_map[menu_item]["fn"]
            st_handler()

            st.image(
                "https://user-images.githubusercontent.com/329928/161578699-c78b5b69-7e23-45b0-9b1d-3f8c2a46bc2d.PNG"
            )
            with st.expander("View code"):
                st.code(inspect.getsource(st_handler))


def main():
    do_sidebar()
    do_body()


# Run main()
if __name__ == "__main__":
    main()
