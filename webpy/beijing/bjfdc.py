"""
北京房地产数据采集和保存

modification history
--------------------
23dec19,lan  written
"""

from weblog.database import db
import requests
from bs4 import BeautifulSoup

'''
riqi 日期时间
cunliangfang_zong 存量房总签约套数
cunliangfang_zhuzai  存量房住宅签约套数
xianfang_zong      现房总签约套数
xianfang_zhuzhai   现房住宅签约套数
qifang_zong      期房总签约套数
qifang_zhuzhai      期房住宅签约套数    
'''

class BjfdcData (db.Model):
      # 表的名字:
    __tablename__ = 'bjfdc'
       # 表的结构:
    riqi = db.Column(db.Date, primary_key=True)
    cunliangfang_zong = db.Column(db.Integer)
    cunliangfang_zhuzai = db.Column(db.Integer)
    xianfang_zong = db.Column(db.Integer)
    xianfang_zhuzhai = db.Column(db.Integer)
    qifang_zong = db.Column(db.Integer)
    qifang_zhuzhai = db.Column(db.Integer)

def bjfdcCreateDB ():
    pass

class FetchBjfdc:
    def __init__(self):
        pass

    def downloadPage (self):
        '''用于下载页面'''
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
        url = "http://bjjs.zjw.beijing.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml"
        r = requests.get(url, headers=headers)
        r.encoding = 'gb2312'
        return r.text

    def fetch (self):
        html = self.downloadPage ()   # 下载界面
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.body
        tbls = body.find_all ("table")
        tbl = tbls[10]
        print (tbl)

if __name__ == '__main__':
    bjfdc = FetchBjfdc ()
    bjfdc.fetch()