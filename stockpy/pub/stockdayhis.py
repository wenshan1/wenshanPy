'''
Created on Jul 20 2017
@author: Bin Lan
@email:  jetlan@live.cn

股票日k线数据,前复权
'''

# modification history
# --------------------
# 05nov17,lan  修改数据采集接口
# 20jul17,lan  written

import common as comm
from datetime import datetime, timedelta
import  time
import tushare as ts

cons = comm.getTSCons ()

def updateAStockData(code, start, end, conn):
    startstr = start.strftime('%Y-%m-%d')
    endstr = end.strftime('%Y-%m-%d')
    try:
        #df = ts.get_h_data(code, start=startstr, end=endstr)
        df = ts.bar(code, conn=cons, freq='D', start_date=startstr, end_date=endstr)
        for index, row in df.iterrows():
            insert_sql = "INSERT INTO stockdayhist \
                          (code, riqi, open, high, close, low, volume, amount) \
                          VALUES ('%s', '%s', %f, %f, %f, %f, %f, %f)"
            row_tulpe = (code, index, row['open'], row['high'], row['close'], row['low'], row['vol'],
                         row['amount'])
            wsql = insert_sql % row_tulpe
            cursor = conn.cursor()
            try:
                cursor.execute(wsql)
                conn.commit()
            except Exception as e:
                #print (e)
                pass
            finally:
                cursor.close()
    except Exception as e:
        print (e)
    return

#更新最近股票的数据
def updateDayHis (allCodes, conn):
    now = datetime.now()
    for codeTu in allCodes:
        code = codeTu[0]
        start = now - timedelta(days=365)
        end = now
        result = comm.getStockLast (code, conn)
        if result != None:
            start = result + timedelta (days=1)

        updateAStockData(code, start, end, conn)
        time.sleep(1)
    return

if __name__ == '__main__':
    conn = comm.dbConnect ()
    updateDayHis (comm.getAllStock (conn), conn)
    comm.dbDisconnect (conn)