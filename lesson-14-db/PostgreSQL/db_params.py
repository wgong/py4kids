#!/usr/bin/env python
# coding: utf-8

from  os.path import expanduser
from json import loads
with open(expanduser("~/.secrets/db_params.json")) as f:
    db_params = loads(f.read())

def get_db_params(db_name, db_type="postgresql"):
    """Given db_name, db_type
    return a dictionary of (host,port,user,password,database)
    """
    kwargs = {"database": db_name}
    kwargs.update(db_params[db_type][db_name])
    return kwargs