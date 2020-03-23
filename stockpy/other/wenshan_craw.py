# -*- coding: utf-8 -*-

"""
Created on Nov 13 2018

@author: Bin Lan
@email: jetlan@live.cn

爬取www.wenshan.me， 并保存到SQLit中
"""

import requests
import time

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
AlBase = declarative_base()
engine = create_engine('sqlite:///e:/wenshan.db', echo=True)
DBSessionT = sessionmaker(bind=engine)

class HTML (AlBase):
    # 表的名字:
    __tablename__ = 'wenshan'
    time = Column(String(256), primary_key=True)
    html = Column(String(2048))

def createTables ():
    #IndexBasic.__table__.drop (bind = engine)
    AlBase.metadata.create_all(engine)
    
def download_page(url):
    '''
    用于下载页面
    '''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text

def saveHtml (text):
    try:
        session = DBSessionT ()
        session.add (HTML (time=time.ctime(), html=text))
        session.commit ()
        session.close ()
    except Exception as e:
        print (e)

if __name__ == '__main__':
    html = download_page ('http://www.wenshan.me/?p=534')
    saveHtml (html)
    