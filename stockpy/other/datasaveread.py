# -*- coding: utf-8 -*-
# author: Bin Lan
# email:  jetlan@live.cn

import sqlite3
import os
import tushare as ts
import pandas as pd

'''
save data to sqllite3
'''

def test_sql_write (df, dbPath):
    if os.path.exists (dbPath):
        os.remove (dbPath)
    sql_db = sqlite3.connect (dbPath)
    df.to_sql (name = 'test_table', con = sql_db)
    sql_db.close ()

def test_sql_read (dbPath):
    sql_db = sqlite3.connect (dbPath)
    df = pd.read_sql_query ("select * from test_table", sql_db)
    sql_db.close ()
    return df
    

if __name__ == '__main__':
    df = ts.profit_data(top=60)  
    test_sql_write (df, "/home/lanbin/test.db")
    dr = test_sql_read ("/home/lanbin/test.db")
    print (dr)

