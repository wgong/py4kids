from utils import *

def insert_default_user():
    count = db_get_row_count(table_name="t_user")
    if count < 1:
        curr_ts = get_ts_now()
        insert_user = f""" 
            insert into t_user(
                email, created_by, updated_by, 
                username, password, created_at, updated_at
            ) 
            values(
                '{DEFAULT_USER}', '{DEFAULT_USER}', '{DEFAULT_USER}', 
                '{DEFAULT_USER}', '{DEFAULT_USER}', '{curr_ts}', '{curr_ts}'
            );
        """
        with DBConn() as _conn:
            db_run_sql(insert_user, _conn)        

def create_tables():
    # run a test query
    try:
        db_get_row_count(table_name=CFG["TABLE_CONFIG"])
    except Exception as e:
        ddl_script = open(CFG["META_DB_DDL"]).read()
        logging.error(ddl_script)
        with DBConn() as _conn:
            db_run_sql(ddl_script, _conn)
            
if __name__ == '__main__':
    # create tables if missing
    create_tables()
    insert_default_user()
