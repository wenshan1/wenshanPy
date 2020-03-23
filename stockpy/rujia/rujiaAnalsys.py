#!/usr/bin/env python3
"""
Created on Sun Aug 19 19:38:13 2018

@author: wenshan
"""

from common import db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
matplotlib 解决中文显示问题
"""
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

engine = db.getDBEnginee()
    
def rujiaAnalsys ():
    sql = 'select count(*) from rujia where gender="F"'
    df = pd.read_sql_query (sql, engine)
    
    fcount = df.iat[0,0]
    print ("女性数量： %s" % (fcount))
    
    sql = 'select count(*) from rujia where gender="M"'
    df = pd.read_sql_query (sql, engine)
    
    fcount = df.iat[0,0]
    print ("男性数量： %s" % (fcount))
    
    sql = 'select ctfid, count(*) as sum  from rujia group by ctfid order by sum desc limit 10'
    df = pd.read_sql_query (sql, engine)
    print ('前10名爱住如家酒店人员')
    print (df)
    
def rujiaBar ():
    sql = 'select count(*) from rujia where gender="F"'
    df = pd.read_sql_query (sql, engine)
    
    women = df.iat[0,0]
    print ("女性数量： %s" % (women))
    
    sql = 'select count(*) from rujia where gender="M"'
    df = pd.read_sql_query (sql, engine)
    
    men = df.iat[0,0]
    print ("男性数量： %s" % (men))

    men_means = (men, 3000000)

    women_means = (women, 2000000)

    ind = np.arange (len (men_means))  # the x locations for the groups
    width = 0.35                     # the width of the bars

    fig, ax = plt.subplots()

    rects1 = ax.bar(ind - width/2, men_means, width,
                color='SkyBlue', label='Men')
    rects2 = ax.bar(ind + width/2, women_means, width,
                color='IndianRed', label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('人数')
    ax.set_title('如家男女比例')
    ax.set_xticks(ind)
    ax.set_xticklabels(('G1','G2'))
    ax.legend()
    