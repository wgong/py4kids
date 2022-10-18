"""
build ui on pyathena (instead of notebook) as an alternative to Hue 


# bootstrap icons
- https://icons.getbootstrap.com/

"""


import streamlit as st
from streamlit_option_menu import option_menu


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



from identity import Identity as id_
import antiphony
from pyathena import connect
from pyathena.pandas.util import as_pandas
from sql_metadata import Parser


# my
# import shutil
# shutil.copy("C:/work/bitbucket_extra/coworkers/WEN_GONG/work/SQL/gwg_query_utils.py", "./gwg_query_utils.py")


# Initial page config
st.set_page_config(
     page_title='CE Report',
     layout="wide",
     initial_sidebar_state="expanded",
)


_APPNAME = "ce"
_CURRENT_USER = id_.username.casefold()





SYS_LVL = {
    "int": "e", "eng": "e", "test": "t"
}

AWS_PROFILE = {
    "gwg-eng" : ["APPENGINEER"]
}

##
## Helper functions
###############################################################
def establish_conn(json_dict, master_dns, connection_trial=2):
    connection_counter = 0
    while connection_counter < connection_trial:
        try:
            # checking if the connection can be established
            hconn = IdServer(
                host=master_dns,
                **json_dict["hive_parameters"]).get_connection()
            pconn = IdServer(
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


def _gen_csv_filename_from_sql(sql):
    tables = Parser(sql).tables
    if len(tables):
        fn = tables[0].split(".")[-1]
    else:
        fn = "data"
    now = datetime.now()
    return f'{fn}_{now:%Y-%m-%d-%H-%M-%S}.csv'


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
    keyring.delete_password(_APPNAME, st.session_state["username"])
    st.session_state["username"] = ""
    st.session_state["password"] = ""
    
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


def _execute_athena(sql_stmt):
    if "query_results_athena" not in st.session_state:
        st.session_state["query_results_athena"] = {}

    _is_select_stmt = True if "select" in sql_stmt.lower() and "from" in sql_stmt.lower() else False

    ts_start = time.time()

    if "cursor" not in st.session_state:
        raise ValueError("Please establish Athena connection!")

    try:
        with st.spinner("Running query ..."):
            _cursor = st.session_state["cursor"]
            _cursor.execute(sql_stmt)
            df = as_pandas(_cursor)
            if _is_select_stmt:
                st.session_state["query_results_athena"][sql_stmt] = df
    except:
        st.error(f"{format_exc()}")

    ts_stop = time.time()
    if _is_select_stmt:
        st.info(f"completed in {(ts_stop-ts_start):.2f} sec")


def _display_cache(sql_stmt, query_engine="athena"):
    if f"query_results_{query_engine}" in st.session_state:
        res = st.session_state[f"query_results_{query_engine}"]
        if res and sql_stmt in res:
            df = res[sql_stmt]
            st.dataframe(df)
            st.download_button('Download', data=df.to_csv(), mime='text/csv', 
                file_name=_gen_csv_filename_from_sql(sql_stmt), key=f"{_hash_sql(sql_stmt)}_{query_engine}")

def _add_hyphen_date(dt):
    "from YYYYMMDD to YYYY-MM-DD"
    return f"{dt[0:4]}-{dt[4:6]}-{dt[6:8]}"

def _merge_request_result(query_engine="athena", file_csv="query_result.csv"):
    res = st.session_state.get(f"query_results_{query_engine}", None)
    if not res: return
    df = pd.concat([df for (_, df) in res.items()], ignore_index=True)
    st.dataframe(df)
    st.download_button('Download', data=df.to_csv(), mime='text/csv', 
        file_name=file_csv, key=f"{file_csv}_{query_engine}")

def _display_cache_all(query_engine="athena"):
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


def do_welcome():
    st.subheader("About")
    st.markdown("""
    This data app is built on [streamlit](http://streamlit.io) framework to run SQL query over __Athena__ and/or __EMR__.

    """, unsafe_allow_html=True)

    st.write("package dependency:")
    st.code(open("requirements.txt").read())

    st.warning("Disclaimer: Not all SQL statements are supported!")

def do_query_athena():
    st.header("Contact Event Report")
    tlf = Tealeaf()

    query_engine="athena"
    sql_ce = """
        select distinct
            CM.rpt_po_id CINergy_Client_Id
            ,format_datetime(init_ts,'YYYYMMdd') Contact_Date_Key
            ,format_datetime(init_ts,'HH:mm:ss') Time
            ,CE.comm_chnl_nm as Txn_Processed_Channel_Name
            ,CE.crew_po_id Crew_PO_Id
            ,CE.crew_frst_nm Crew_First_Name
            ,CE.crew_lst_nm Crew_Last_Name
            ,CE.crew_intrnl_phon_no Crew_Internal_Phone_Number
            ,CE.cntct_cd Event_Type_Code_level1
            ,CE.cntct_nm Event_Type_Code_Desc_level1
            ,CE.cntct_abv_nm Event_Type_Code_SN_level1
            ,CE.cntct_typ_cd Event_Code_level2
            ,CE.cntct_typ_nm Event_Code_Desc_level2
            ,CE.cntct_typ_abv_nm Event_Code_SN_level2
            ,CE.cntct_memo_txt Contact_Memo_Text
        from ContactEvent CE
        inner join ClientMerge CM
            on CE.clnt_po_id=CM.po_id
        where CM.rpt_po_id in {poid_clause}
            and CE.init_dt >= cast('{start_dt}' as date)  
            and CE.init_dt <= cast('{end_dt}' as date)  
        order by Contact_Date_Key, Time, Contact_Memo_Text, Event_Type_Code_level1, Event_Code_level2
        ;    
    """


    st.subheader("SNOW Request")
    _request_id = st.text_input('Request Item', value="RITM1743377_TEST1", key="request_id")
    _request_desc = st.text_input('Request Description', value="Please provide me with contact events for CID 1457411230 from 1-1-2022 -  3-31-2022 Thanks!", key="request_desc")
    _request_type, _poids, _date_range = tlf.parse_description(_request_desc)
    if _request_type != "ContactEvent":
        st.error("Not a Contact Event request")
        return

    date_ranges = tlf.split_date_ranges(_date_range, days_to_split=365)
    st.info(f"Request Type: {_request_type}")
    st.info(f"POID: {_poids}")
    st.info(f"Date Range: {_date_range}")
    # st.info(f"Split Date Ranges: {date_ranges}")

    poid_clause = str(_poids).replace("[", "(").replace("]", ")").replace("'", "")

    # Execute SQL
    if st.button('Execute Query'):
        _clear_cache(query_engine)        
        sql_stmt = f"""
        insert into gwgwork.snow_requests(request_item_id, request_type, ts, status, description)
        values('{_request_id.strip()}', '{_request_type}',  LOCALTIMESTAMP, 'New', '{_request_desc.strip()}');
        """
        # st.info(sql_stmt)
        try:
            sql_queries = _reformat_sql(sql_stmt, query_engine)
            _execute_athena(sql_queries[0])
        except Exception as e:
            st.error(str(e))
            return

        for (_start_dt, _end_dt) in date_ranges:
            sql_stmt = sql_ce.format(poid_clause=poid_clause, 
                start_dt=_add_hyphen_date(_start_dt), 
                end_dt=_add_hyphen_date(_end_dt))
            sql_queries = _reformat_sql(sql_stmt, query_engine)
            st.info(f"Split Date Range: {_start_dt} - {_end_dt}")
            # st.code(sql_queries[0])
            _execute_athena(sql_queries[0])

        sql_stmt = f"""
        insert into gwgwork.snow_requests(request_item_id, request_type, ts, status, description)
        values('{_request_id.strip()}', '{_request_type}',  LOCALTIMESTAMP, 'QueryCompleted', '');
        """
        # st.info(sql_stmt)
        sql_queries = _reformat_sql(sql_stmt, query_engine)
        _execute_athena(sql_queries[0])


    st.subheader("Query Results:")
    _merge_request_result(query_engine, file_csv=f"{_request_id}-{_date_range[0]}-{_date_range[1]}.csv")

    # _display_cache_all(query_engine)
              



# place this after fn defined
st_handler_map = {
    "CE": {"fn": do_query_athena, "icon": "file-earmark-spreadsheet"}, 
    "About": {"fn": do_welcome, "icon": "house"},
}

def do_login():

    ## handle Login
    with st.sidebar.form(key='login_form'):
        username = st.text_input('Username', value=_CURRENT_USER, key="username").casefold()
        password = st.text_input('Password', type="password", key="password")
        col1,col2 = st.columns(2)
        with col1:
            if st.form_submit_button('Login'):
                if _is_valid_cred(username, password):
                    # update keyring
                    keyring.set_password("identity", username, password)
                    # use keyring to store sailpoint login session
                    keyring.set_password(_APPNAME, username, "OK")
                else:
                    st.sidebar.warning("Invalid cred")
                    # remove sailpoint login session
                    try:
                        keyring.delete_password(_APPNAME, username)
                    except:
                        pass
        with col2:
            logout = st.form_submit_button('Logout', on_click=_clear_login_form)

## Menu
def do_sidebar():

    do_login()

    login_result = keyring.get_password(_APPNAME, st.session_state["username"])
    if login_result is not None and login_result == "OK":
        menu_item = st.empty()
        st.sidebar.text(f"Logged in")
        
        menu_options = list(st_handler_map.keys()) 
        icons = [st_handler_map[i]["icon"] for i in menu_options]

        with st.sidebar:
            menu_item = option_menu("Reports", menu_options, 
                icons=icons, menu_icon="layout-text-window-reverse",
                default_index=0, 
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "20px"}, 
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "maroon"},
                },
                key="menu_item")

            if menu_item == "Contact Event":

                with st.expander("Manage Athena Connection"):
                    with st.form(key='conn_athena_form'):
                        col_left, col_right = st.columns(2)
                        with col_left:
                            aws_account = st.text_input("Account:", value='gwg-test', key="aws_account")
                            aws_role = st.text_input("Role:", value='ANALYTICS', key="aws_role")
                        with col_right:
                            aws_region = st.text_input("Region:", value='us-east-1', key="aws_region")
                            data_source = st.text_input("Catalog:", value='PlatformCatalog', key="data_source")
                        athena_work_group = st.text_input("Work Group:", value='gwg_athena_workgroup', key="athena_work_group")
                        s3_loc = f'{aws_account}-{aws_region}-gwganalytics-sandbox/athena-query-results'
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

                    # st.checkbox("Execute all SQLs at once", value=False, key="EXECUTE_ALL_SQLS_ATHENA")

                    btn_clear = st.button("Clear Cache")
                    if btn_clear:
                        _clear_cache(query_engine="athena")

# Body
def do_body():

    login_result = keyring.get_password(_APPNAME, st.session_state["username"])
    if login_result == "OK" and "menu_item" in st.session_state:        
        menu_item = st.session_state["menu_item"]
        if menu_item and "fn" in st_handler_map[menu_item]:
            st_handler = st_handler_map[menu_item]["fn"]
            st_handler()

            # st.image("https://user-images.githubusercontent.com/329928/161578699-c78b5b69-7e23-45b0-9b1d-3f8c2a46bc2d.PNG")
            # with st.expander("View code"):
            #     st.code(inspect.getsource(st_handler))
        else:
            do_query_athena()
    else:
        do_query_athena()

def main():
    do_sidebar()
    do_body()

# Run main()
if __name__ == '__main__':
    main()
