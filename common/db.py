# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:00:17 2018

@author: blan
required package: pymysql
数据库操作

modification history
--------------------
23sep18,lan  add sqlalchemy engine
17sep18,lan  written

"""

import pymysql.cursors
from sqlalchemy import create_engine

"""
def getDBEnginee4ali ():
    engine = create_engine('mysql+pymysql://stock:stock.8810@47.93.11.229:3306/stock')
    return engine
"""

dbHost = '128.224.158.223'
dbUser = 'blan'
dbPwd = 'blan'
dbDataBase = 'blan'

def getDBEnginee ():
    #'mysql+pymysql://stock:stock.8810@47.93.11.229:3306/stock'
    dbstr = 'mysql+pymysql://%s:%s@%s:3306/%s' % (dbUser, dbPwd, dbHost, dbDataBase)
    engine = create_engine(dbstr, encoding= 'utf-8', echo = True)
    return engine

def dbConnect ():
    conn = pymysql.connect(host= dbHost, port=3306, user= dbUser, 
                           passwd = dbPwd, db= dbDataBase, charset='utf8')
    return conn

def dbDisconnect (conn):
    conn.close ()
        
def truncateTable (tablename, conn):
    wsql = "truncate table %s" % tablename
    cursor = conn.cursor ()
    cursor.execute(wsql)
    conn.commit()
    cursor.close()
    return