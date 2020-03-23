# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:30:46 2017

@author: blan
"""

import tushare as ts
import common as comm
import matplotlib.pyplot as plt

df = ts.get_money_supply()

fig  = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlabel("month")      
ax.set_ylabel("m2")

ax.plot(df['month'][:100].tolist (), df['m2'][:100].tolist ())
plt.show ()