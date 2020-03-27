# -*- coding: utf-8 -*-

"""
北京房地产数据采集和保存

modification history
--------------------
23dec19,lan  written
"""

from common import db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date

# 创建对象的基类:
AlBase = declarative_base()
engine = db.getDBEnginee()
DBSessionT = sessionmaker(bind=engine)

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

'''
riqi 日期时间
cunliangfang_zong 存量房总签约套数
cunliangfang_zhuzai  存量房住宅签约套数
xianfang_zong      现房总签约套数
xianfang_zhuzhai   现房住宅签约套数
qifang_zong      期房总签约套数
qifang_zhuzhai      期房住宅签约套数    
'''

class BjfdcData (AlBase):
      # 表的名字:
    __tablename__ = 'bjfdc'
       # 表的结构:
    riqi = Column(Date, primary_key=True)
    cunliangfang_zong = Column(Integer)
    cunliangfang_zhuzai = Column(Integer)
    xianfang_zong = Column(Integer)
    xianfang_zhuzhai = Column(Integer)
    qifang_zong = Column(Integer)
    qifang_zhuzhai = Column(Integer)


def createBjfdcData ():
    #IndexBasic.__table__.drop (bind = engine)
    AlBase.metadata.create_all(engine)
    

def downloadPage ():
    '''用于下载页面'''
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    url = "http://bjjs.zjw.beijing.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml"
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'
    return r.text

''' 存量房网上签约 '''
def cunLiangFangTable ():
    html = downloadPage ()   # 下载界面
    soup = BeautifulSoup(html, 'html5lib')
    body = soup.body
    tbls = body.find_all ("table")
    ''' 存量房网上签约表'''
    tbl = tbls[16]
    return tbl
        
class FetchBjfdc:
    def __init__(self):
        pass
    
    def getCunLiangFang (self, tbl):
        '''所有的tr'''
        trs = tbl.find_all("tr")
        
        '''签约数据日期'''
        tds = trs[0].find_all("td")
        riqiTxt = tds[0].text
        riqiTxt=riqiTxt.strip ('\n')
        riqiTxt=riqiTxt.strip ()

        match=re.compile(u'[\u4e00-\u9fa5]')
        riqiTxt=match.sub('',riqiTxt)
        riqiTxt = riqiTxt.strip ('�')
        
        self.riqi = datetime.strptime(riqiTxt, "%Y/%m/%d")
        print ("riqi:" + str(self.riqi))
        
        '''存量房总签约数据'''
        tds = trs[1].find_all ("td")
        qianyueTxt = tds[1].text
        lst = re.findall('(\w*[0-9]+)\w*', qianyueTxt)
        self.qianyue_zong = 0
        for item in lst:
            self.qianyue_zong = self.qianyue_zong * 10 + int(item)
            
        print ("qianyueshu:" + str(self.qianyue_zong))
        
        '''存量房住宅签约数据'''
        tds = trs[3].find_all ("td")
        qianyueTxt = tds[1].text
        lst = re.findall('(\w*[0-9]+)\w*', qianyueTxt)
        self.qianyue_zhuzai = 0
        for item in lst:
            self.qianyue_zhuzai = self.qianyue_zhuzai * 10 + int(item)
            
        print ("qianyueshu_zhuzai:" + str(self.qianyue_zhuzai))        
        
    def getAndSaveData (self):
        tbl = cunLiangFangTable ()
        self.getCunLiangFang (tbl)
        
        bjfdc = BjfdcData (riqi=self.riqi, cunliangfang_zong=self.qianyue_zong,
                           cunliangfang_zhuzai=self.qianyue_zhuzai)
        
        session = DBSessionT ()
        try:
            session.add (bjfdc)
            session.commit ()
        except Exception as e:
            pass
        finally:
            session.close ()        
        

if __name__ == '__main__':
    bjfdc = FetchBjfdc ()
    bjfdc.getAndSaveData()

