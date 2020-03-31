#!/usr/bin/env python

from weblog.database import db
from stock import stockal

if __name__ == '__main__':
    stockal.createTables ()
    db.create_all()
    stockal.saveStockBasic ()
