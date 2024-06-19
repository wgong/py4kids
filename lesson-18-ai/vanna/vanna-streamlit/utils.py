import re
from datetime import date, datetime, timedelta
import sqlite3

import jsonlines

import pandas as pd
import streamlit as st

CFG = {
    "FILE_DB": "./db/data_copilot.sqlite3", 
    "DEBUG_SQL": True,
}

class DBConn(object):
    def __init__(self, db_file=CFG["FILE_DB"]):
        self.conn = sqlite3.connect(db_file)

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()


class DBUtils():
    """SQLite database query utility """

    def get_db_connection(self, file_db=CFG["FILE_DB"]):
        if not file_db.exists():
            raise(f"DB file not found: {file_db}")
        return sqlite3.connect(file_db)

    def run_sql(self, sql_stmt, conn=None, DEBUG_SQL=CFG["DEBUG_SQL"]):
        """helper to run SQL statement
        """
        if not sql_stmt:
            return
        
        if conn is None:
            # create new connection
            with DBConn() as _conn:

                if sql_stmt.lower().strip().startswith("select"):
                    return pd.read_sql(sql_stmt, _conn)
                        
                if DEBUG_SQL:  
                    print(f"[DEBUG] {sql_stmt}")
                cur = _conn.cursor()
                cur.executescript(sql_stmt)
                _conn.commit()
                return
            
        else:
            # use existing connection
            _conn = conn
            if sql_stmt.lower().strip().startswith("select"):
                return pd.read_sql(sql_stmt, _conn)
                    
            if DEBUG_SQL:  
                print(f"[DEBUG] {sql_stmt}")
            cur = _conn.cursor()
            cur.executescript(sql_stmt)
            _conn.commit()
            return


def remove_collections(vn, collection_name=None, ACCEPTED_TYPES = ["sql", "ddl", "documentation"]):
    if not collection_name:
        collections = ACCEPTED_TYPES
    elif isinstance(collection_name, str):
        collections = [collection_name]
    elif isinstance(collection_name, list):
        collections = collection_name
    else:
        print(f"\t{collection_name} is unknown: Skipped")
        return

    for c in collections:
        if not c in ACCEPTED_TYPES:
            print(f"\t{c} is unknown: Skipped")
            continue
            
        # print(f"vn.remove_collection('{c}')")
        vn.remove_collection(c)

def strip_brackets(ddl):
    """
    This function removes square brackets from table and column names in a DDL script.
    
    Args:
        ddl (str): The DDL script containing square brackets.
    
    Returns:
        str: The DDL script with square brackets removed.
    """
    # Use regular expressions to match and replace square brackets
    pattern = r"\[([^\]]+)]"  # Match any character except ] within square brackets
    return re.sub(pattern, r"\1", ddl)        

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
