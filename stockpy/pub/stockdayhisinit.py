'''

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

def getAStockData (code, start, end, conn):
    startstr = start.strftime ('%Y-%m-%d')
    endstr = end.strftime ('%Y-%m-%d')

    try:
        #df = ts.get_h_data (code, start= startstr, end= endstr)
        df = ts.bar(code, conn=cons, freq='D', start_date=startstr, end_date=endstr)
    except Exception as e:
        print (e)
        return

    cursor = conn.cursor()

    for index, row in df.iterrows ():
        insert_sql = "INSERT INTO stockdayhist \
                    (code, riqi, open, high, close, low, volume, amount) \
                    VALUES ('%s', '%s', %f, %f, %f, %f, %f, %f)"
        row_tulpe = (code, index, row['open'], row['high'], row['close'], row['low'], row['vol'],
                     row['amount'])
        wsql = insert_sql % row_tulpe
        cursor.execute(wsql)

    conn.commit()
    cursor.close()
    return


#初始化所有的股票日线数据
def initDayHis (allCodes, conn):
    now = datetime.now()
    for codeTu in allCodes:
        code = codeTu[0]
        start = codeTu[2]
        result = comm.getStockLast (code, conn)
        if result != None:
            start = result + timedelta (days=1)
        print (code, codeTu[1], start)

        nCount = 0
        while start <= now:
            end = start + timedelta(days=365)
            if end > now:
                end = now
            getAStockData (code, start, end, conn)
            start = end + timedelta(days=1)
            #if nCount > 0:
                #time.sleep (nCount)
            nCount += 1
            if nCount > 3:
                nCount = 0
    return

if __name__ == '__main__':
    conn = comm.dbConnect ()
    initDayHis (comm.getAllStock (conn), conn)
    comm.dbDisconnect (conn)