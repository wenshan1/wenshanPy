# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 14:09:48 2018

@author: blan
保存所有股票基本信息和历史信息到mysql数据库中

modification history
--------------------
15sep18,lan  written
"""

from common import db
from common import ts
from datetime import datetime, timedelta
import  time

pro = ts.getPro()
dbcon = db.dbConnect4Ali()  #数据库

#创建stock基本信息表
def createStockBasicTable ():
    cursor = dbcon.cursor()
    createtable =  ("CREATE TABLE IF NOT EXISTS pro_stock_basic" 
                   "("
                   "ts_code VARCHAR(255) primary key,"  # TS_CODE 比如：  000001.SZ
                   "symbol      VARCHAR(255),"          # 股票代码， 比如：  000001
                   "name        VARCHAR(255),"          # 名字
                   "fullname    VARCHAR(255),"          # 股票全称
                   "enname      VARCHAR(255),"          # 英文全称
                   "exchange_id VARCHAR(255),"          # 交易所代码
                   "curr_type   VARCHAR(255),"          # 交易货币
                   "list_status VARCHAR(255),"          # 上市状态 L上市 D退市 P暂停上市
                   "list_date   VARCHAR(255),"          # 上市日期
                   "delist_date VARCHAR(255),"          # 退市日期
                   "is_hs       VARCHAR(255)"           # 是否沪深港通标的，N否 H沪股通 S深股通
                   ")")
    print ("创建stock_pro sql语句:\n" + createtable)
    cursor.execute (createtable)
    dbcon.commit()

#保存股票数据的基本信息
def saveStockBasic () :
    createStockBasicTable ()
    db.truncateTable ('pro_stock_basic', dbcon)
    jys = ('SSE', 'SZSE', 'HKEX')
    
    for exid in jys:
        df = pro.query('stock_basic', exchange_id=exid, is_hs='N', fields='ts_code, symbol, name, fullname, enname, exchange_id, curr_type, list_status, list_date, delist_date, is_hs')
        
        for index, row in df.iterrows ():
            insert_sql = "INSERT INTO pro_stock_basic \
                (ts_code, symbol, name, fullname, enname, exchange_id, curr_type, list_status, list_date, delist_date, is_hs) \
                VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            row_tulpe = (row['ts_code'], row['symbol'], row['name'], row['fullname'], row['enname'], row['exchange_id'], row['curr_type'],
                         row['list_status'], row['list_date'], row['delist_date'], row['is_hs'])
            wsql = insert_sql % row_tulpe
            print (wsql)
            try:
                cursor = dbcon.cursor()
                cursor.execute(wsql)
                dbcon.commit()
            except Exception as e:
                print('Exception:', e)
            finally:
                cursor.close()

def createStockKHisTable ():
    createtable =  ("CREATE TABLE IF NOT EXISTS pro_stock_k_his" 
                   "("
                   "ts_code     VARCHAR(255) NOT NULL,"  # TS_CODE 比如：  000001.SZ
                   "trade_date  VARCHAR(255) NOT NULL,"  # 交易日期
                   "open	    float,"                    # 开盘价
                   "high        float,"                 # 最高价
                   "low         float,"                # 最低价
                   "close       float,"          # 收盘价
                   "pre_close   float,"          # pre_close
                   "changee     float,"          # 涨跌额
                   "pct_change  float,"          # 涨跌幅
                   "vol         float,"          # 成交量 （手）
                   "amount      float,"          #成交额 （千元）
                   "CONSTRAINT pk_his PRIMARY KEY(ts_code, trade_date))")
    print ("创建pro_stock_k_his sql语句:\n" + createtable)
    cursor = dbcon.cursor()
    cursor.execute (createtable)
    dbcon.commit()

def insertDataToTable (df):
    try:
        for index, row in df.iterrows():
            insert_sql = "INSERT INTO pro_stock_k_his \
            (ts_code, trade_date, open, high, low, close, pre_close, changee, pct_change, vol, amount) \
         VALUES ('%s', '%s',       %f,   %f,   %f,  %f,    %f,         %f,      %f,        %f,  %f)"
            row_tulpe = (row['ts_code'], row['trade_date'], row['open'], row['high'], 
                         row['low'], row['close'], row['pre_close'], row['change'],
                         row['pct_change'], row['vol'], row['amount'])
            wsql = insert_sql % row_tulpe
            cursor = dbcon.cursor()
            try:
                cursor.execute(wsql)
                print (wsql)
                dbcon.commit()
            except Exception as e:
                #print (e)
                pass
            finally:
                cursor.close()
    except Exception as e:
        print (e)
    
""" 
获得最新日期历史数据日期
"""
def getStockLast (ts_code):
    with dbcon.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = "SELECT trade_date FROM pro_stock_k_his where ts_code = '%s' order by trade_date desc" % ts_code
        cursor.execute(sql)
        dbcon.commit()

        # 获取查询结果
        result = cursor.fetchone ()

    if result != None:
        return result[0]
    else:
        return None
    
#baocun gupiao lishi shuju
def saveStockKHis (nday):
    now = datetime.now()
    start = now - timedelta(days=nday)
    startstr = start.strftime('%Y%m%d')
    endstr = now.strftime('%Y%m%d')
    names = getAllStockName ()
    for astock in names:
        rs = getStockLast (astock[0])
        if rs is not None:
            startstr = rs
            
        df = pro.daily(ts_code=astock[0], start_date=startstr, end_date=endstr)
        insertDataToTable (df)
        time.sleep (2)
        
#get all stock name
def getAllStockName ():
    with dbcon.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = 'SELECT ts_code FROM pro_stock_basic order by ts_code'
        cursor.execute(sql)
        dbcon.commit()
        # 获取查询结果
        result = cursor.fetchall()

    return result

def updateStockKHis ():
    createStockKHisTable ()
    saveStockKHis (360 * 10)
    
if __name__ == '__main__':
    updateStockKHis ()

