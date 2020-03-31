#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 21:57:38 2018

@author: wenshan

modification history
--------------------
23sep18,lan  written
"""

from datetime import datetime, timedelta
from weblog.database import db
from . import ts


pro = ts.getPro()

#stock基本信息表
class StockBasic (db.Model):
    # 表的名字:
    __tablename__ = 'pro_stock_basic'
    
    # 表的结构:
    ts_code = db.Column(db.String(255), primary_key=True)  # TS_CODE 比如：  000001.SZ
    symbol = db.Column(db.String(255))                     # 股票代码， 比如：  000001
    name = db.Column(db.String(255))                       # 名字
    fullname = db.Column(db.String(255))                   # 股票全称
    enname = db.Column(db.String(255))                     # 英文全称
    exchange_id = db.Column(db.String(255))                # 交易所代码
    curr_type = db.Column(db.String(255))                  # 交易货币                   
    list_status = db.Column(db.String(255))                # 上市状态 L上市 D退市 P暂停上市                    
    list_date = db.Column(db.String(255))                  #上市日期
    delist_date = db.Column(db.String(255))                # 退市日期
    is_hs = db.Column(db.String(255))                      # 是否沪深港通标的，N否 H沪股通 S深股通

def createTables ():
    pass

#保存股票数据的基本信息
def saveStockBasic () :
    jys = ('SSE', 'SZSE', 'HKEX')
    
    for exid in jys:
        df = pro.query('stock_basic', exchange_id=exid, is_hs='N', 
        fields='ts_code, symbol, name, fullname, enname, exchange_id, curr_type, list_status, list_date, delist_date, is_hs')
        
        for index, row in df.iterrows ():    
            stb = StockBasic (ts_code = row['ts_code'], symbol = row['symbol'], name = row['name'], 
                              fullname = row['fullname'], enname = row['enname'], exchange_id = row['exchange_id'], 
                              curr_type = row['curr_type'], list_status = row['list_status'], list_date = row['list_date'], 
                              delist_date = row['delist_date'], is_hs = row['is_hs'] )
            session = db.session ()
            try:
                session.add (stb)
                session.commit ()
            except Exception as e:
                pass
            finally:
                session.close ()
            

#获得所有股票数据名称 (ts_code)
def getAllStockName ():
    session = db.session () 
    stbs = session.query (StockBasic).all ()
    session.close ()    

    result = []
    for stb in stbs:
        result.append (stb.ts_code)

    return result

#stock 日K数据 
class StockKHis (db.Model):
    # 表的名字:
    __tablename__ = 'pro_stock_k_his_al'
    
    # 表的结构:
    ts_code = db.Column(db.String(255), primary_key=True)    # TS_CODE 比如：  000001.SZ    
    trade_date = db.Column(db.String(255), primary_key=True)          # 交易日期   
    open = db.Column(db.Float)          # 开盘价        
    high = db.Column(db.Float)          # 最高价
    low = db.Column(db.Float)          # 最低价
    close = db.Column(db.Float)        # 收盘价
    pre_close = db.Column(db.Float)    # pre_close
    changee = db.Column(db.Float)          # 涨跌额
    pct_change = db.Column(db.Float)       #  涨跌幅
    vol = db.Column(db.Float)       #   成交量 （手）
    amount = db.Column(db.Float)       #  成交额 （千元）

#获得最新日期历史数据日期
def getStockLast (tscode):
    session = db.session ()
    recs = session.query (StockKHis).filter_by (ts_code=tscode).order_by(StockKHis.trade_date).all ()
    session.close ()

    if len(recs) != 0:
        return recs[-1].trade_date
    else:
        return None

def insertDataToTable (df):
    for index, row in df.iterrows():
        try:
            session = db.session ()
            session.add ( StockKHis (ts_code = row['ts_code'], 
                                     trade_date = row['trade_date'], 
                                     open = row['open'], 
                                     high = row['high'], 
                                     low = row['low'], close = row['close'], 
                                     pre_close = row['pre_close'], changee = row['change'],
                                     pct_change = row['pct_change'], 
                                     vol = row['vol'], amount = row['amount']
                                    )
                        )

            session.commit ()
            session.close ()
        except Exception as e:
            print (e)
            
#保存股票历史数据
def saveStockKHis (nday):
    now = datetime.now()
    start = now - timedelta(days=nday)
    startstr = start.strftime('%Y%m%d')
    endstr = now.strftime('%Y%m%d')
    names = getAllStockName ()
    for astock in names:
        rs = getStockLast (astock)
        if rs is not None:
            startstr = rs
            
        df = pro.daily(ts_code=astock, start_date=startstr, end_date=endstr)
        insertDataToTable (df)
        time.sleep (2)

if __name__ == '__main__':
    saveStockKHis (360 * 10)

