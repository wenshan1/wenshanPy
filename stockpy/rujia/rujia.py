"""
解析如家文件到数据库中保存，
并且分析
required package: pymysql
作者：兰斌

创建数据库是用utf8： create database rujia  charset utf8;
"""

import pymysql.cursors

def createTable (conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS rujia"
                   "("
                   "id int auto_increment primary key,"  # ID
                   "name        VARCHAR(255),"               # 名字
                   "cardno      VARCHAR(255),"               # CardNo 
                   "descriot    VARCHAR(255),"               # Descriot  
                   "ctftp       VARCHAR(255),"               # CtfTp
                   "ctfid       VARCHAR(255),"               # CtfId
                   "gender      VARCHAR(255),"               # 性别
                   "birthday    VARCHAR(255),"               # 生日 
                   "address     VARCHAR(255),"               # 地址 
                   "zip         VARCHAR(255),"               # zip 
                   "mobile      VARCHAR(255),"               # 手机 
                   "tel         VARCHAR(255),"               # 电话 
                   "fax         VARCHAR(255),"               # 传真  
                   "email       VARCHAR(255),"               # email
                   "version     VARCHAR(255),"               # Version
                   "rujiaid     int"                         # 如家ID
                   ")"
                   )
    conn.commit()

def dbConnect ():
    conn = pymysql.connect(host='localhost', port=3306, user='root', 
                           passwd='root', db='stock', charset='utf8')
    return conn

def dbDisconnect (conn):
    conn.close ()

# 解析文件并且保存到数据库中。
def analysisFile (fileName):
    conn = dbConnect()
    createTable (conn)
    ncount = 0

    with open(fileName, 'r', encoding='utf-8') as fh:
        for ln in fh:
            ln = fh.readline()
            ln = ln.strip('\n')

            rec = ln.split('|')
            #print (rec)

            insert_sql = "INSERT INTO rujia \
                        (name, cardno, descriot, ctftp, ctfid, gender, birthday, address, zip, mobile, tel, fax, email, version, rujiaid) \
                VALUES  ('%s', '%s',   '%s',      '%s', '%s',  '%s',    '%s',     '%s',  '%s', '%s',  '%s', '%s', '%s', '%s',     %s)"
            if len(rec) < 2:
                continue
            try:
                row_tulpe = (
                         rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[19], rec[20], rec[21], rec[22], rec[-2], rec[-1])
                wsql = insert_sql % row_tulpe
                ncount += 1
            except Exception as e:
                pass

            try:
                if ncount == 1:
                    conn.begin()
                    cursor = conn.cursor()

                print (wsql)
                cursor.execute(wsql)

                if ncount > 1000:
                    conn.commit()
                    cursor.close()
                    ncount = 0

            except Exception as e:
                # print (e)
                pass
            finally:
                pass

    dbDisconnect(conn)


if __name__ == '__main__':
    analysisFile('D:/qqtongbu/tongbu/python/rujia/hotel.txt')



