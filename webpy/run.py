#!/usr/bin/env python
#coding=utf8

from weblog import app
from stock import stockal

if __name__ == '__main__':
    stockal.saveStockKHis (360 * 10)
    app.run(host='0.0.0.0', port=8888, debug=True)
