# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:00:52 2018

@author: blan
required: tushare

"""

import tushare as ts

def getPro ():
    ts.set_token('e5bcd694be0fec88b5036c3af2d3f9b794b318880178f359e2c2ce2a')
    pro = ts.pro_api()
    return pro

