"""
build ui on pyathena (instead of notebook) as an alternative to Hue 

- see https://confluence.vanguard.com/display/CAPT/Athena+Jupyter+notebook+connection+in+Anaconda

# bootstrap icons
- https://icons.getbootstrap.com/

"""
__author__ = 'Wen_Gong@vanguard.com'

import streamlit as st
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
from st_aggrid import (
    AgGrid,
    DataReturnMode,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
)

# std
from datetime import datetime
from os.path import splitext, exists
import inspect
from functools import partial
from io import StringIO
import keyring
import platform
import subprocess
from PIL import Image
from traceback import format_exc
import time
import hashlib

# ds
import numpy as np
import pandas as pd
import sqlite3

# vgi
from identity import Identity as id_
import antiphony
from pyathena import connect
from pyathena.pandas.util import as_pandas
from sql_metadata import Parser
import vg_sql_utils as vsu
from hivo import HivoServer

# my
# import shutil
# shutil.copy("C:/work/bitbucket_extra/coworkers/WEN_GONG/work/SQL/dst_query_utils.py", "./dst_query_utils.py")
# from dst_query_utils import *

# Initial page config
st.set_page_config(
     page_title='Streamlit Query Editor',
     layout="wide",
     initial_sidebar_state="expanded",
)


_APPNAME = "query_editor"
_CURRENT_USER = id_.username.casefold()

_DB_NAME = "query_editor.sqlite"
_CREATE_TABLE_SQL = """
create table if not exists sql_history (
    hash_key text,
    sql_stmt text,
    query_engine text,
    ts text,
    is_inactive integer
);

"""
_CREATE_TBL_INDEX = """
create unique index if not exists sql_idx on sql_history(hash_key,query_engine)
"""
_SQL_HISTORY_COLUMNS = Parser(_CREATE_TABLE_SQL).columns


def _create_db_table():
    if not exists(_DB_NAME):
        conn_sqlite = sqlite3.connect(f"file:{_DB_NAME}?mode=rwc", uri=True)
        conn_sqlite.execute(_CREATE_TABLE_SQL)
        conn_sqlite.execute(_CREATE_TBL_INDEX)
        conn_sqlite.close()

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


SYS_LVL = {
    "int": "e", "eng": "e", "test": "t", "prod": "p"
}

AWS_PROFILE = {
    "vgi-ess-eng" : ["SIAPPENGINEER", "DSTANALYTICS"], 
    "vgi-ess-test" : ["SIAPPDEVELOPER", "DSTANALYTICS"], 
    "vgi-ess-prod" : ["DSTANALYTICS"],
}

# Aggrid options
_GRID_OPTIONS = {
    "grid_height": 360,
    "return_mode_value": DataReturnMode.__members__["FILTERED"],
    "update_mode_value": GridUpdateMode.__members__["MODEL_CHANGED"],
    "fit_columns_on_grid_load": False,
    "selection_mode": "single",  # "multiple",
    "allow_unsafe_jscode": True,
    "groupSelectsChildren": True,
    "groupSelectsFiltered": True,
    "enable_pagination": True,
    "paginationPageSize": 10,
    "wrapText": True,
}

_FORM_CONFIG = {
    "view": {"read_only": True, "key_pfx": "view", "selectable": True},
    "create": {"read_only": False, "key_pfx": "add", "selectable": False},
    "update": {"read_only": False, "key_pfx": "upd", "selectable": True},
    "delete": {"read_only": True, "key_pfx": "del", "selectable": True},
}

_TOP_QUERY_LIMIT = 20  # No. of most recent queries to fetch

##
## Helper functions
###############################################################
def establish_conn(json_dict, master_dns, connection_trial=2):
    connection_counter = 0
    while connection_counter < connection_trial:
        try:
            # checking if the connection can be established
            hconn = HivoServer(
                host=master_dns,
                **json_dict["hive_parameters"]).get_connection()
            pconn = HivoServer(
                host=master_dns,
                query_engine="presto",
                **json_dict["hive_parameters"],
            ).get_connection()
            return hconn, pconn
        except Exception as err:
            # after cluster spins up successfully, there seems to have a slight
            # lag occasionally to establish connection
            connection_counter += 1
            if connection_counter == connection_trial:
                raise Exception(
                    f"Could not establish connection after {connection_counter} attemps."
                )
            time.sleep(180)

def _prepare_grid(df, context="view"):
    enable_selection = _FORM_CONFIG[context]["selectable"]
    gb = GridOptionsBuilder.from_dataframe(df)
    if enable_selection:
        gb.configure_selection(_GRID_OPTIONS["selection_mode"],
                use_checkbox=True,
                groupSelectsChildren=_GRID_OPTIONS["groupSelectsChildren"], 
                groupSelectsFiltered=_GRID_OPTIONS["groupSelectsFiltered"]
            )
    gb.configure_pagination(paginationAutoPageSize=False, 
        paginationPageSize=_GRID_OPTIONS["paginationPageSize"])
    gb.configure_grid_options(domLayout='normal')
    gb.configure_column("sql_stmt", wrapText=True)
    grid_response = AgGrid(
        df, 
        gridOptions=gb.build(),
        height=_GRID_OPTIONS["grid_height"], 
        # width='100%',
        data_return_mode=_GRID_OPTIONS["return_mode_value"],
        update_mode=_GRID_OPTIONS["update_mode_value"],
        fit_columns_on_grid_load=_GRID_OPTIONS["fit_columns_on_grid_load"],
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    )

    if enable_selection:
        selected_df = pd.DataFrame(grid_response['selected_rows'])
        return selected_df
    else:
        return None

def _gen_key(key_pfx, table_name, key_name=""):
    return f"{key_pfx}_{table_name}_{key_name}"

def _default_val(row, col_name):
    return row[col_name][0] if row and col_name in row else ""


def _build_sql_form(ctx, row=None):
    key_pfx = _FORM_CONFIG[ctx]["key_pfx"]   
    _disabled = _FORM_CONFIG[ctx]["read_only"]
    table_name = "sql_history"
    st.text_area('SQL statement:', value=_default_val(row, "sql_stmt"), height=320, key=_gen_key(key_pfx, table_name, "sql_stmt"), disabled=False)
    # col_left, col_right = st.columns(2)
    # with col_left:
    #     st.text_input("sentiment", value=_default_val(row, "sentiment"), key=_gen_key(key_pfx, table_name, "sentiment"), disabled=_disabled if ctx != "update" else True)
    # with col_right:
    #     st.text_area("topic_terms", value=_default_val(row, "topic_terms"), key=_gen_key(key_pfx, table_name, "topic_terms"), disabled=_disabled)

def _gen_csv_filename_from_sql(sql):
    tables = Parser(sql).tables
    if len(tables):
        fn = tables[0].split(".")[-1]
    else:
        fn = "data"
    now = datetime.now()
    return f'{fn}_{now:%Y-%m-%d-%H-%M-%S}.csv'

def _get_lang(file_ext, file_type):
    "return lang for accepted files: text, sql, py"
    if file_type == 'application/octet-stream' and file_ext.lower() == ".sql":
        lang = "sql"
    elif file_type == 'text/plain':
        lang = LANGUAGE_MAP.get(file_ext.lower(), "sql")
    else:
        lang = "sql"
    return lang

def _show_editor_settings():
    with st.expander("Editor settings"):
        st.selectbox("Language", options=["sql"]+sorted(list(LANGUAGE_MAP.values())), index=0, key="ace_lang")
        st.selectbox("Theme", options=["pastel_on_dark", "chrome"], index=0, key="ace_theme")
        st.select_slider("Height", options=[str(i*100) for i in range(3,7)], key="ace_height")
        st.select_slider("Font", options=[str(i) for i in range(14,19,2)], key="ace_font")
        st.select_slider("Tab", options=[2,4,8], key="ace_tab")
        st.checkbox("Readonly", value=False, key="ace_readonly")
        st.checkbox("Auto-update", value=False, key="ace_autoupdate")
        st.checkbox("Wrap", value=False, key="ace_wrap")
        st.checkbox("Show gutter", value=True, key="ace_gutter")
        st.number_input("Top recent queries", value=_TOP_QUERY_LIMIT, min_value=10, key="top_query_limit")


def _is_valid_cred(username,passwd):
    system = platform.system().casefold()
    validator = partial(subprocess.run, shell=True, check=True)
    if system == "windows":
        proc = validator(["powershell.exe", "-command",
                          f'(new-object directoryservices.directoryentry "", {username}, {passwd}).psbase.name -ne $null'],
                         stdout=subprocess.PIPE)
        retcode = 0 if b"True" in proc.stdout else 1
    elif system == "darwin":
        retcode = validator([f"dscl /Local/Default -authonly {username} {passwd}"]).returncode
    elif system == "linux":
        retcode = validator([f"su {username}"], input=passwd.encode())
    else:
        raise OSError(f"Unsupported OS (system) '{system}', "
                      "please submit a feature request.")
    return True if retcode == 0 else False


def _clear_login_form():
    keyring.delete_password(_APPNAME, st.session_state["vg_username"])
    st.session_state["vg_username"] = ""
    st.session_state["vg_password"] = ""
    
def _validate_tablename(sql_stmt):
    for table in Parser(sql_stmt).tables:
        if len(table.split(".")) != 3:
            st.error(f"Table '{table}' must be fully qualified like <catalog.db.table>")
            return False
    return True

def _drop_data_source(sql_stmt):
    sql_stmt_new = (sql_stmt + ";")[:-1]  # create a copy
    dic = {}
    for table in Parser(sql_stmt_new).tables:
        ts = table.split(".")
        if len(ts) == 1:
            raise Exception(f"Missing data_base qualifier in '{sql_stmt}'")
        elif len(ts) == 2:
            continue
        else:
            dic[table] = ".".join(ts[-2:])
    for k,v in dic.items():
        sql_stmt_new = sql_stmt_new.replace(k,v)
    return sql_stmt_new

def _add_data_source(sql_stmt, data_source="PlatformCatalog"):
    sql_stmt_new = (sql_stmt + ";")[:-1]  # create a copy
    dic = {}
    for table in Parser(sql_stmt_new).tables:
        ts = table.split(".")
        if len(ts) == 1:
            raise Exception(f"Missing data_base qualifier in '{sql_stmt}'")
        elif len(ts) == 2:
            ts2 = [data_source] + ts
        else:
            continue
        dic[table] = ".".join(ts2)
    for k,v in dic.items():
        sql_stmt_new = sql_stmt_new.replace(k,v)
    return sql_stmt_new if _validate_tablename(sql_stmt_new) else sql_stmt


def _hash_sql(sql):
    """Consistent hashing of str:
        https://stackoverflow.com/questions/2511058/persistent-hashing-of-strings-in-python
    """
    # return hashlib.sha256(sql.encode('utf-8')).hexdigest()
    return hashlib.md5(sql.encode('utf-8')).hexdigest()

def _reformat_sql(sql_text, query_engine):
    """ For Athena, prepend data_source prefix "PlatformCatalog" to database.table if missing
        For EMR, remove "catalog" prefix if present

        return a list of reformated SQLs split by ";"
    """
    sql_queries = []
    for sql_stmt in [s.strip() for s in sql_text.split(";") if s.strip() and not s.strip().startswith("--")]:
        if sql_stmt.lower().strip().startswith("show "):
            sql_stmt_new = sql_stmt
        else:
            if query_engine == "athena":
                sql_stmt_new = _add_data_source(sql_stmt, st.session_state["data_source"])
            else:
                sql_stmt_new = _drop_data_source(sql_stmt)
        if not sql_stmt_new in sql_queries:   # avoid duplicate
            sql_queries.append(sql_stmt_new)
    return sql_queries

def _execute_query_emr(sql_stmt, conn):
    """Execute query on EMR, 

    Returns:
        df if "SELECT" query else None
    """
    sql_tokens = [t.value for t in Parser(sql_stmt).tokens]
    if sql_tokens[0].lower() in ["create", "update", "insert", "delete"]:
        vsu.query_utils._runquery(sql_stmt, conn)
        return None
    else:
        return pd.read_sql(sql_stmt, conn)

def _execute_emr(sql_stmt):
    if "query_results_emr" not in st.session_state:
        st.session_state["query_results_emr"] = {}

    ts_start = time.time()

    try:
        with st.spinner("Running query ..."):
            df = _execute_query_emr(sql_stmt, st.session_state["pconn"])
            st.session_state["query_results_emr"][sql_stmt] = df
    except:
        st.error(f"Try with Hive connection since Presto connection has the following issue:\n{format_exc()}")
        try:
            df = _execute_query_emr(sql_stmt, st.session_state["hconn"])
            st.session_state["query_results_emr"][sql_stmt] = df
        except:
            st.error(f"Hive connection has the following issue:\n{format_exc()}")

    ts_stop = time.time()
    st.info(f"completed in {(ts_stop-ts_start):.2f} sec")


def _execute_athena(sql_stmt):
    if "query_results_athena" not in st.session_state:
        st.session_state["query_results_athena"] = {}

    ts_start = time.time()

    try:
        with st.spinner("Running query ..."):
            _cursor = st.session_state["cursor"]
            _cursor.execute(sql_stmt)
            df = as_pandas(_cursor)
            st.session_state["query_results_athena"][sql_stmt] = df
    except:
        st.error(f"{format_exc()}")

    ts_stop = time.time()
    st.info(f"completed in {(ts_stop-ts_start):.2f} sec")


def _display_cache(sql_stmt, query_engine="athena"):
    if f"query_results_{query_engine}" in st.session_state:
        res = st.session_state[f"query_results_{query_engine}"]
        if res and sql_stmt in res:
            df = res[sql_stmt]
            st.dataframe(df)
            st.download_button('Download', data=df.to_csv(), mime='text/csv', 
                file_name=_gen_csv_filename_from_sql(sql_stmt), key=f"{_hash_sql(sql_stmt)}_{query_engine}")


def _display_cache_all(query_engine="athena"):
    st.subheader("Query results:")
    if f"query_results_{query_engine}" in st.session_state:
        res = st.session_state[f"query_results_{query_engine}"]
        if not res: return
        for sql_stmt, df in res.items():
            st.code(sql_stmt)
            st.dataframe(df)
            st.download_button('Download', data=df.to_csv(), mime='text/csv', 
                file_name=_gen_csv_filename_from_sql(sql_stmt), key=f"{_hash_sql(sql_stmt)}_{query_engine}")

def _clear_cache(query_engine="athena"):
    if f"query_results_{query_engine}" in st.session_state:
        res = st.session_state[f"query_results_{query_engine}"]
        if res:
            cached_data = list(res.keys()) + list(res.values())
            del cached_data
    st.session_state[f"query_results_{query_engine}"] = {}

def _get_new_sql_stmt(data, conn):
    """Identify new SQL statements to be saved to DB based on user-key: (hash_key,query_engine)
    """
    data_new = []
    for d in data:
        hash_key, query_engine = d[0], d[2]
        df_tmp = pd.read_sql(f"select * from sql_history where hash_key='{hash_key}' and query_engine='{query_engine}';", conn)
        if df_tmp.shape[0] == 0:
            data_new.append(d)
    return data_new



def _layout_editor(query_engine="athena"):

    # display text in ACE editor
    initial_sql_text = _load_sql_history(query_engine=query_engine, 
            top_query_limit=st.session_state.get("top_query_limit", _TOP_QUERY_LIMIT))
    # st.info(initial_sql_text)

    st.session_state[f"sql_text_{query_engine}"] = st_ace(value=initial_sql_text, 
        language="sql", 
        theme=st.session_state.get("ace_theme", "pastel_on_dark"), 
        height=int(st.session_state.get("ace_height", "500")),
        font_size=int(st.session_state.get("ace_font", "14")),
        tab_size=int(st.session_state.get("ace_tab", "4")),
        readonly=st.session_state.get("ace_readonly", False),
        auto_update=st.session_state.get("ace_autoupdate", False),
        wrap=st.session_state.get("ace_wrap", False),
        show_gutter=st.session_state.get("ace_gutter", True),
        key=f"ace_{query_engine}"
    )
    btn_write = st.button("Save Queries", key=f"save_sql_{query_engine}")
    if btn_write:
        conn_sqlite = sqlite3.connect(f"file:{_DB_NAME}?mode=rwc", uri=True)
        sql_text = st.session_state[f"sql_text_{query_engine}"]
        sql_queries = _reformat_sql(sql_text, query_engine)
        if query_engine == "athena":
            # drop catalog name and de-dup so that hash_key would be the same across emr/athena
            sql_queries_new = []
            for sql_stmt in sql_queries:
                sql_stmt_new = _drop_data_source(sql_stmt)
                if not sql_stmt_new in sql_queries_new:
                    sql_queries_new.append(sql_stmt_new)
            sql_queries = sql_queries_new
        data = [[_hash_sql(sql_stmt), sql_stmt, query_engine, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0] for sql_stmt in sql_queries]
        data_new = _get_new_sql_stmt(data, conn=conn_sqlite)
        if data_new:
            df_new = pd.DataFrame(data_new, columns=_SQL_HISTORY_COLUMNS)
            df_new.to_sql("sql_history", conn_sqlite, if_exists='append', index=False)
        conn_sqlite.close()


def _load_sql_history(query_engine="athena", top_query_limit=_TOP_QUERY_LIMIT):
    conn_sqlite = sqlite3.connect(_DB_NAME)
    df = pd.read_sql(f"""
        select sql_stmt from sql_history where query_engine='{query_engine}' order by ts desc limit {top_query_limit}
        """, conn_sqlite)
    conn_sqlite.close()
    sql_text = ";\n".join(df["sql_stmt"].to_list())
    if sql_text:
        sql_text += ";\n"
    return sql_text

def do_welcome():
    st.subheader("Welcome")
    st.markdown("""
    This data app is built on [streamlit](http://streamlit.io) framework to run SQL query over __Athena__ and/or __EMR__.

    """, unsafe_allow_html=True)

    st.write("package dependency:")
    st.code(open("requirements-ui_query_editor.txt").read())

    st.warning("Disclaimer: Not all SQL statements are supported!")

def do_query_emr():
    st.subheader("Query EMR")
    st.warning("Use semicolon ';' to end an SQL statement")
    query_engine="emr"
    _layout_editor(query_engine)

    sql_queries = _reformat_sql(st.session_state[f"sql_text_{query_engine}"], query_engine)    # drop catalog if present
    # Execute SQL
    if "pconn" in st.session_state and "hconn" in st.session_state:
        if st.session_state["EXECUTE_ALL_SQLS_EMR"]:
            btn_execute_all = st.button("Execute All SQLs", key=f"execute_sql")
            if btn_execute_all:
                for n,sql_stmt in enumerate(sql_queries):
                    st.code(sql_stmt)
                    _execute_emr(sql_stmt)
            _display_cache_all(query_engine)

        else:
            for n,sql_stmt in enumerate(sql_queries):
                st.code(sql_stmt)
                btn_execute = st.button("Execute SQL", key=f"execute_sql_{n}")
                if btn_execute:
                    _execute_emr(sql_stmt)
                _display_cache(sql_stmt, query_engine)


def do_query_athena():
    st.subheader("Query Athena")
    st.warning("Use semicolon ';' to end an SQL statement")
    query_engine="athena"
    _layout_editor(query_engine)

    sql_queries = _reformat_sql(st.session_state[f"sql_text_{query_engine}"], query_engine)    # drop catalog if present
    # Execute SQL
    if "cursor" in st.session_state:

        if st.session_state["EXECUTE_ALL_SQLS_ATHENA"]:
            btn_execute_all = st.button("Execute All SQLs", key=f"execute_sql_all")
            if btn_execute_all:
                for n,sql_stmt in enumerate(sql_queries):
                    st.code(sql_stmt)
                    _execute_athena(sql_stmt)
            _display_cache_all(query_engine)

        else:
            for n,sql_stmt in enumerate(sql_queries):
                st.code(sql_stmt)
                btn_execute = st.button("Execute SQL", key=f"execute_sql_{n}")
                if btn_execute:
                    _execute_athena(sql_stmt)
                _display_cache(sql_stmt, query_engine)
                
def do_sql_history():
    st.subheader("Query Histories")
    CONTEXT = "view"
    conn_sqlite = sqlite3.connect(_DB_NAME)
    df = pd.read_sql(f"""
        select ts,query_engine,sql_stmt from sql_history where is_inactive < 1 order by ts desc
        """, conn_sqlite)
    conn_sqlite.close()
    selected_row = _prepare_grid(df, context=CONTEXT).to_dict()
    _build_sql_form(CONTEXT, row=selected_row)




# place this after fn defined
st_handler_map = {
    "Home": {"fn": do_welcome, "icon": "house"},
    "Athena": {"fn": do_query_athena, "icon": "table"}, 
    "EMR": {"fn": do_query_emr, "icon": "bounding-box"}, 
    "Query History": {"fn": do_sql_history, "icon": "card-list"}, 
}

def do_login():

    ## handle Login
    with st.sidebar.form(key='login_form'):
        vg_username = st.text_input('Username', value=_CURRENT_USER, key="vg_username").casefold()
        vg_password = st.text_input('Password', type="password", key="vg_password")
        col1,col2 = st.columns(2)
        with col1:
            if st.form_submit_button('Login'):
                if _is_valid_cred(vg_username, vg_password):
                    # update keyring
                    keyring.set_password("vgidentity", vg_username, vg_password)
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
            logout = st.form_submit_button('Logout', on_click=_clear_login_form)

## Menu
def do_sidebar():

    do_login()

    login_result = keyring.get_password(_APPNAME, st.session_state["vg_username"])
    if login_result is not None and login_result == "OK":
        menu_item = st.empty()
        st.sidebar.text(f"Logged in")
        
        menu_options = list(st_handler_map.keys()) 
        icons = [st_handler_map[i]["icon"] for i in menu_options]

        with st.sidebar:
            menu_item = option_menu("Query Editor", menu_options, 
                icons=icons, menu_icon="pencil-square",
                default_index=0, 
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "20px"}, 
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "maroon"},
                },
                key="menu_item")

            if menu_item == "Athena":

                with st.form(key='conn_athena_form'):
                    col_left, col_right = st.columns(2)
                    with col_left:
                        aws_account = st.text_input("Account:", value='vgi-ess-prod', key="aws_account")
                        aws_role = st.text_input("Role:", value='DSTANALYTICS', key="aws_role")
                    with col_right:
                        aws_region = st.text_input("Region:", value='us-east-1', key="aws_region")
                        data_source = st.text_input("Catalog:", value='PlatformCatalog', key="data_source")
                    athena_work_group = st.text_input("Work Group:", value='dst_athena_workgroup', key="athena_work_group")
                    s3_loc = f'{aws_account}-{aws_region}-dstanalytics-sandbox/athena-query-results'
                    s3_staging_dir = st.text_area("S3 Staging Dir:", value=s3_loc, key="s3_staging_dir")

                    aws_cfg = {
                        'account': aws_account,
                        'role': aws_role,
                        'region': aws_region,
                        's3_staging_dir': s3_staging_dir,
                        'athena_work_group': athena_work_group,
                        #'encryption_option': encryption_option,
                        #'kms_key': kms_key            
                    }

                    col_left, col_right = st.columns(2)
                    with col_left:
                        btn_connect = st.form_submit_button("Connect")
                    with col_right:
                        btn_disconnect = st.form_submit_button("Disconnect")

                if btn_connect:
                    try:
                        _creds = antiphony.get_aws_creds(aws_cfg['account'], aws_cfg['role'])
                        _cursor = connect(
                                aws_access_key_id=_creds['aws_access_key_id']
                                ,aws_secret_access_key=_creds['aws_secret_access_key']
                                ,aws_session_token=_creds['aws_session_token']
                                ,region_name=aws_cfg['region']
                                ,s3_staging_dir=aws_cfg['s3_staging_dir']
                                ,work_group=aws_cfg['athena_work_group']
                                #,kms_key=aws_cfg['kms_key']
                                #,encryption_option=aws_cfg['encryption_option']                 
                            ).cursor()
                        if "cursor" not in st.session_state:
                            st.session_state["cursor"] = _cursor
                    except:
                        st.error(format_exc())           

                if btn_disconnect and "cursor" in st.session_state:
                    del [st.session_state["cursor"]]  # del cursor obj
                    st.session_state.pop("cursor",None) # del cursor key
                    _clear_cache(query_engine="athena")

                if "cursor" in st.session_state and st.session_state["cursor"]:
                    cursor_state = "Connected!"
                else:
                    cursor_state = "Not connected!"
                st.info(cursor_state)

                st.checkbox("Execute all SQLs at once", value=False, key="EXECUTE_ALL_SQLS_ATHENA")

                btn_clear = st.button("Clear Cache")
                if btn_clear:
                    _clear_cache(query_engine="athena")

            if menu_item == "EMR":

                json_dict = {'hive_parameters': {'hive.execution.engine': 'mr'}}
                USE_DST_DAILY_CLUSTER = st.checkbox("Use DST Daily Cluster", value=True, key="USE_DST_DAILY_CLUSTER")
                if USE_DST_DAILY_CLUSTER:
                    # Skip spin up cluster if you use existing cluster
                    master_dns = 'dst-daily-cluster.us-east-1.essp.c1.vanguard.com'
                else:
                    master_dns = st.text_input("Master DNS:", value='dst-daily-cluster.us-east-1.essp.c1.vanguard.com', key="master_dns")

                col_left, col_right = st.columns(2)
                with col_left:
                    btn_connect = st.button("Connect")

                with col_right:
                    btn_disconnect = st.button("Disconnect")

                if btn_connect:
                    try:
                        hconn, pconn = establish_conn(json_dict, master_dns)
                        if "pconn" not in st.session_state:
                            st.session_state["pconn"] = pconn
                        if "hconn" not in st.session_state:
                            st.session_state["hconn"] = hconn
                    except:
                        st.error(format_exc())           

                if btn_disconnect and "pconn" in st.session_state and "hconn" in st.session_state:
                    del [st.session_state["pconn"], st.session_state["hconn"]]
                    _clear_cache(query_engine="emr")

                if "pconn" in st.session_state and st.session_state["pconn"]:
                    cursor_state = "Connected!"
                else:
                    cursor_state = "Not connected!"
                st.info(cursor_state)

                st.checkbox("Execute all SQLs at once", value=False, key="EXECUTE_ALL_SQLS_EMR")

                btn_clear = st.button("Clear Cache")
                if btn_clear:
                    _clear_cache(query_engine="emr")


            st.image("https://user-images.githubusercontent.com/329928/155828764-b19a08e4-5346-4567-bba0-0ceeb5c2b241.png")
            _show_editor_settings()

## Body
def do_body():
    _create_db_table()

    login_result = keyring.get_password(_APPNAME, st.session_state["vg_username"])
    if login_result == "OK" and "menu_item" in st.session_state:        
        menu_item = st.session_state["menu_item"]
        if menu_item and "fn" in st_handler_map[menu_item]:
            st_handler = st_handler_map[menu_item]["fn"]
            st_handler()

            # st.image("https://user-images.githubusercontent.com/329928/161578699-c78b5b69-7e23-45b0-9b1d-3f8c2a46bc2d.PNG")
            # with st.expander("View code"):
            #     st.code(inspect.getsource(st_handler))
        else:
            do_welcome()
    else:
        do_welcome()

def main():
    do_sidebar()
    do_body()

# Run main()
if __name__ == '__main__':
    main()
