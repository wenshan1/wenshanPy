# -*- coding: utf-8 -*-
"""
Created on Jul 18 17:28:01 2017
@author: blan

表stockbasics:

code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数
"""

import tushare as ts
import pymysql.cursors
import common as  cmn

def createTable (conn):
    cursor = conn.cursor()
    cursor.execute( "CREATE TABLE IF NOT EXISTS xiaoqu"
                    "("
                    "name VARCHAR(255) NOT NULL,"                #小区名字
                    "regionb VARCHAR(255) ,"               #小区名字
                    "regions  VARCHAR(255),"
                    "style VARCHAR(255),"
                    "year VARCHAR(255),"
                    "PRIMARY KEY (name))")
    conn.commit()
    print (cursor.rowcount)
    if cursor.rowcount == 1:
        print ("create table success.")
    cursor.close ()

# 判断代码是否存在
def isCodeExit (code, conn):
    select_sql = "select * from stockbasics where code ='%s'"
    wsql = select_sql % code

    cursor = conn.cursor ()
    cursor.execute(wsql)
    conn.commit()
    ncount = cursor.rowcount
    cursor.close()

    return ncount != 0

# 保存data_frame数据到数据库中
def saveDB (conn):
    df = ts.get_stock_basics()
    print (df.columns)
    cmn.truncateTable("stockbasics", conn)
    for index, row in df.iterrows ():
        insert_sql = "INSERT INTO stockbasics \
            (code, name, industry, area, pe, outstanding, totals, totalAssets, liquidAssets, fixedAssets, \
            reserved, reservedPerShare, esp, bsps, pb, timeToMarket, undp, rev, profit, gpr, npr, holders) \
            VALUES ('%s', '%s', '%s', '%s', %f, %f, %f, %f, %f,  %f, %f, %f, %f, %f, %f, '%s', %f, %f, %f, %f, %f, %ld)"
        row_tulpe = (index, row['name'], row['industry'], row['area'], row['pe'], row['outstanding'],
                         row['totals'], row['totalAssets'], row['liquidAssets'], row['fixedAssets'],
                         row['reserved'], row['reservedPerShare'], row['esp'], row['bvps'], row['pb'],
                         row['timeToMarket'], row['undp'], row['rev'], row['profit'], row['gpr'], row ['npr'],
                         row['holders'])
        wsql = insert_sql % row_tulpe
        print (wsql)
        try:
            cursor = conn.cursor()
            cursor.execute(wsql)
            conn.commit()
        except Exception as e:
            print('Exception:', e)
        finally:
            cursor.close()

if __name__ == '__main__':
    conn = cmn.dbConnect ()
    try:
        #createTable (conn)
        saveDB (conn)
    finally:
        cmn.dbDisconnect (conn)


