# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 17:28:01 2017

@author: blan
采用 tushare 模块来采集指数和股票K线数据
"""

# modification history
# --------------------
# 06nov17,lan  直接保存数据到数据库中
# 20jul17,lan  written

import tushare as ts
import pymysql.cursors
from datetime import datetime, timedelta
from urllib import request
import json
import requests
import common as comm

data = []
data_frame = None

def updateDataBase (conn, bInit):
    nCount = 0
    cursor = None
    insert_sql = "INSERT INTO stockindex (name, riqi, volume, openprice, closeprice, highprice, lowprice, adjcloseprice) VALUES ('%s', '%s', %s, %s, %s, %s, %s, %s);"
    for index, row in data_frame.iterrows():
        # 这里修改为组装SQL并执行的语句
        print(row['code'], row['date'], row['volume'])
        if nCount == 0:
            cursor = conn.cursor()

        row_tulpe = (row['code'], row['date'], row['volume'], row['open'], row['close'], row['high'], row['low'], '0.0')

        wsql = insert_sql % row_tulpe
        nCount = nCount + 1

        try:
            cursor.execute(wsql)
            if not bInit:
                conn.commit()
                cursor.close()
                nCount = 0
            elif nCount >= 500:
                conn.commit()
                cursor.close()
                nCount = 0
        except Exception as e:
            pass

    if nCount> 0 and nCount < 500:
        conn.commit()
        cursor.close()        
'''
def postStock(url):
    global data

    postCount = 0
    for index, row in data_frame.iterrows():
        data.append({'pk':{'name': row["code"], 'riqi': row["date"]},
                           'openprice': row["open"],
                     'highprice': row["high"], 'lowprice': row["low"], 'closeprice': row["close"],
                     'volume': row["volume"], 'adjcloseprice': 0})
        postCount = postCount + 1
        if postCount > 200:
            stocks = {'token': '698544885afeeggafdfadafafdiekee',
                      'data': data}
            r = requests.post(url, json=stocks)
            print(r.status_code)
            print(r.text)
            data = []
            postCount = 0

    if postCount > 0:
        stocks = {'token': '698544885afeeggafdfadafafdiekee',
                  'data': data}
        r = requests.post(url, json=stocks)
        print(r.status_code)
        print(r.text)
'''

#得到一个stock的数据
def GetIndexData (conn, posturl, stockName, bInit = False):
    global data_frame
    if (bInit):
        data_frame = ts.get_k_data(stockName, start='2004-01-01',  index = True)        
    else:
         now = datetime.now()
         start = now - timedelta(days=60)
         startStr = start.strftime ('%Y-%m-%d')
         data_frame = ts.get_k_data(stockName, start=startStr,  index = True)

    updateDataBase (conn, bInit)


#初始化指数数据

def GetAllIndexData (conn, posurl, bInit = False):
    stockindexs = ('000001', '399001', '000300', '000905', '399006', '399005', '000010', '000016')
    for stock in stockindexs:
        GetIndexData (conn, posurl, stock, bInit)

if __name__ == '__main__':
    conn = comm.dbConnect()
    GetAllIndexData (conn, "http://localhost/post/stockindex", False)
    comm.dbDisconnect(conn)
