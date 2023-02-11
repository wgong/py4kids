# -*- coding: utf8 -*- 
import cx_Oracle
import operator
import os
from hashlib import md5
from random import randint 
import random
import hashlib
  
class LobExample:
  def __enter__(self):
    self.__db = cx_Oracle.Connection("hr/hr@localhost:1521/XE")
    self.__cursor = self.__db.cursor()
    return self 
  
  def __exit__(self, type, value, traceback):
    # calling close methods on cursor and connection -
    # this technique can be used to close arbitrary number of cursors
    map(operator.methodcaller("close"), (self.__cursor, self.__db)) 
  
  def clob(self):
    # populate the table with large data (1MB per insert) and then
    # select the data including dbms_lob.getlength for validating assertion
    self.__cursor.execute("INSERT INTO lobs(c) VALUES(:1)", ["~"*2**10])
    self.__db.commit()
    self.__cursor.execute("SELECT c, c_len FROM v_lobs WHERE c IS NOT NULL") 
    c, c_len = self.__cursor.fetchone()
    clob_data = c.read()
    assert len(clob_data)==c_len
    #self.__db.rollback()
     
  def nclob(self):
    unicode_data = u"€"*2**10
    # define variable object holding the nclob unicode data
    nclob_var = self.__cursor.var(cx_Oracle.NCLOB)
    nclob_var.setvalue(0, unicode_data) 
    self.__cursor.execute("INSERT INTO lobs(nc) VALUES(:1)", [nclob_var])
    self.__db.commit()
    self.__cursor.execute("SELECT nc, nc_len FROM v_lobs WHERE nc IS NOT NULL") 
    nc, nc_len = self.__cursor.fetchone()
    # reading only the first character just to check if encoding is right
    nclob_substr = nc.read(1, 1)
    assert nclob_substr==u"€"
    #self.__db.rollback() 
  
  def blob(self):
    # preparing the sample binary data with random 0-255 int and chr function
    #binary_data = "".join(chr(randint(0, 255)) for c in range(2**2))
    binary_data = str(random.getrandbits(256))
    binary_md5 = md5(binary_data.encode('utf-8')).hexdigest()
    binary_var = self.__cursor.var(cx_Oracle.BLOB)
    binary_var.setvalue(0, binary_data) 
    self.__cursor.execute("INSERT INTO lobs(b) VALUES(:1)", [binary_var])
    self.__db.commit()
    self.__cursor.execute("SELECT b FROM v_lobs WHERE b IS NOT NULL") 
    b, = self.__cursor.fetchone()
    blob_data = str(b.read())
    blob_md5 = md5(blob_data.encode('utf-8')).hexdigest()
    # data par is measured in hashes equality, what comes in must come out
    #assert binary_md5==blob_md5
    #self.__db.rollback() 
  
  def bfile(self):
    # to insert bfile we need to use the bfilename function
    self.__cursor.execute("INSERT INTO lobs(bf) VALUES(BFILENAME(:1, :2))",
      ["LOB_DIR", "example.txt"])
    self.__db.commit()
    self.__cursor.execute("SELECT bf FROM v_lobs WHERE bf IS NOT NULL") 
    # selecting is as simple as reading other types of large objects
    bf, = self.__cursor.fetchone()
    bfile_data = bf.read()
    assert bfile_data
    #self.__db.rollback() 
  
if __name__ == "__main__":
  with LobExample() as eg:
    eg.clob()
    eg.nclob()
    eg.blob()
    eg.bfile()