#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 21:57:38 2018

@author: wenshan

modification history
--------------------
23sep18,lan  written
"""

from common import db
from common import ts
from datetime import datetime, timedelta
import  time

from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
AlBase = declarative_base()
engine = db.getDBEnginee()
DBSessionT = sessionmaker(bind=engine)

pro = ts.getPro()

#stock基本信息表
class StockBasic (AlBase):
    # 表的名字:
    __tablename__ = 'pro_stock_basic'
    
    # 表的结构:
    ts_code = Column(String(255), primary_key=True)  # TS_CODE 比如：  000001.SZ
    symbol = Column(String(255))                     # 股票代码， 比如：  000001
    name = Column(String(255))                       # 名字
    fullname = Column(String(255))                   # 股票全称
    enname = Column(String(255))                     # 英文全称
    exchange_id = Column(String(255))                # 交易所代码
    curr_type = Column(String(255))                  # 交易货币                   
    list_status = Column(String(255))                # 上市状态 L上市 D退市 P暂停上市                    
    list_date = Column(String(255))                  #上市日期
    delist_date = Column(String(255))                # 退市日期
    is_hs = Column(String(255))                      # 是否沪深港通标的，N否 H沪股通 S深股通

def createTables ():
    #IndexBasic.__table__.drop (bind = engine)
    AlBase.metadata.create_all(engine)

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
            session = DBSessionT ()
            try:
                session.add (stb)
                session.commit ()
            except Exception as e:
                pass
            finally:
                session.close ()
            

#获得所有股票数据名称 (ts_code)
def getAllStockName ():
    session = DBSessionT ()
    stbs = session.query (StockBasic).all ()
    session.close ()    

    result = []
    for stb in stbs:
        result.append (stb.ts_code)

    return result

#stock 日K数据 
class StockKHis (AlBase):
    # 表的名字:
    __tablename__ = 'pro_stock_k_his_al'
    
    # 表的结构:
    ts_code = Column(String(255), primary_key=True)    # TS_CODE 比如：  000001.SZ    
    trade_date = Column(String(255), primary_key=True)          # 交易日期   
    open = Column(Float)          # 开盘价        
    high = Column(Float)          # 最高价
    low = Column(Float)          # 最低价
    close = Column(Float)        # 收盘价
    pre_close = Column(Float)    # pre_close
    changee = Column(Float)          # 涨跌额
    pct_change = Column(Float)       #  涨跌幅
    vol = Column(Float)       #   成交量 （手）
    amount = Column(Float)       #  成交额 （千元）

#获得最新日期历史数据日期
def getStockLast (tscode):
    session = DBSessionT ()
    recs = session.query (StockKHis).filter_by (ts_code=tscode).order_by(StockKHis.trade_date).all ()
    session.close ()

    if len(recs) != 0:
        return recs[-1].trade_date
    else:
        return None

def insertDataToTable (df):
    for index, row in df.iterrows():
        try:
            session = DBSessionT ()
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

