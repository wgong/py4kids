# presto-test.py
# simple python script to run a query on a presto cluster and display the result set 
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
engine = create_engine("presto://localhost:8080/ahana_hive", connect_args={'protocol': 'http'})
 
with engine.connect() as con:
    rs = con.execute('SELECT now()')
    for row in rs:
        print(row)