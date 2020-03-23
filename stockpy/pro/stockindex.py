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

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
AlBase = declarative_base()
engine = db.getDBEnginee()
DBSessionT = sessionmaker(bind=engine)

pro = ts.getPro()

class IndexBasic (AlBase):
    # 表的名字:
    __tablename__ = 'pro_stock_index_basic'
    
    # 表的结构:
    ts_code = Column(String(255), primary_key=True)  #TS代码
    name = Column(String(255))                      #简称
    fullname = Column(String(255))                 #指数全称
    market = Column(String(255))                    #市场
    publisher = Column(String(255))                 #发布方
    index_type = Column(String(255))                 #指数风格
    category = Column(String(255))                #指数类别
    base_date = Column(String(255))      #基期
    base_point = Column(String(255))         #基点
    list_date = Column(String(255))           #发布日期
    weight_rule = Column(String(255))     #加权方式
    desc = Column(String(255))              #描述
    exp_date = Column(String(255))         #终止日期

def createIndexBasicTable ():
    #IndexBasic.__table__.drop (bind = engine)
    AlBase.metadata.create_all(engine)
    
def saveIndexBasic ():
    for ex_market in ('SSE', 'SZSE', 'CSI'):
        df = pro.index_basic(market=ex_market)
        for index, row in df.iterrows ():
            ind = IndexBasic (ts_code = row['ts_code'], 
                              name = row['name'],
                              market = row['market'],
                              publisher = row['publisher'],
                              category = row['category'],
                              base_date = row['base_date'],
                              base_point = row['base_point'],
                              list_date = row['list_date'])
            session = DBSessionT ()
            try:
                session.add (ind)
                session.commit ()
            except Exception as e:
                pass
            finally:
                session.close ()

#显示前10上海交易所指数
def showTop10SSh ():
    session = DBSessionT ()
    query = session.query(IndexBasic)
    recs = query.filter ().all()
    for rec in recs:
        print (rec.name) 
    session.close()

if __name__ == '__main__':
    saveIndexBasic ()