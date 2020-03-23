# -*- coding: utf-8 -*-
"""
Created on Jul 20 2017
@author: Bin Lan
@email:  jetlan@live.cn

获取数据基本类型
"""

import pymysql.cursors
import tushare as ts

def getPro ():
    ts.set_token('e5bcd694be0fec88b5036c3af2d3f9b794b318880178f359e2c2ce2a')
    pro = ts.pro_api()
    return pro

def dbConnectionStr ():
    str = "mysql://root:root@127.0.0.1/stock?charset=utf8"
    return str

def dbConnect ():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='stock', charset='utf8')
    return conn

def dbDisconnect (conn):
    conn.close ()

def truncateTable (tablename, conn):
    wsql = "truncate table %s" % tablename
    cursor = conn.cursor ()
    cursor.execute(wsql)
    conn.commit()
    cursor.close()
    return

def getAllStock (conn):
    with conn.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = 'SELECT code, name, timeToMarket FROM stockbasics order by code'
        cursor.execute(sql)
        conn.commit()

        # 获取查询结果
        result = cursor.fetchall()

    return result

#获得股票代码最新的日期
def getStockLast (code, conn):
    with conn.cursor() as cursor:
        # 执行sql语句，进行查询
        sql = "SELECT riqi FROM stockdayhist where code = '%s' order by riqi desc" % code
        cursor.execute(sql)
        conn.commit()

        # 获取查询结果
        result = cursor.fetchone ()

    if result != None:
        return result[0]
    else:
        return None

def getTSCons ():
    cons = None;
    for i in range(5):
        try:
            cons = ts.get_apis()
            break;
        except Exception as e:
            print(e)
    return cons


if __name__ == '__main__':
    conn = dbConnect ()
    df = getAllStock(conn )
    dbDisconnect(conn)
    print (df)
