# -*- coding: utf-8 -*-


# get a Stock highest

import common as comm
import pandas as pd
import time
import numpy as np

df = pd.DataFrame ()
conn = comm.dbConnect ()
 
def getAStockHighest (stock):
    sql = "select code, riqi, open, high, close, low, volume, amount\
    from stockdayhist where code = '%s' order by  close limit 1"
    
    with conn.cursor() as cursor:
        # 执行sql语句，进行查询
        wsql = sql % (stock[0])
        cursor.execute(wsql)
        conn.commit()

        # 获取查询结果
        result = cursor.fetchone ()
        
        if (result != None):
            dt = result[1]
            if dt.year == 2017:
                s = np.Series (result)
                df.append (s)

    

if __name__ =='__main__':
    stocks = comm.getAllStock (conn)
    for stock in stocks:
        getAStockHighest (stock)
        
    comm.dbDisconnect (conn)
    print (df)
    df.to_excel ("df.xlsx")
    
    


