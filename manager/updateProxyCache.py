# -*- coding: utf-8 -*-
"""
Update All Proxy Cache @ Helyao
-------------------------------------------------
Change Logs:
    2017-10-11  create
"""

from cache import updateAllCache, updateInCache, updateOutCache
from update import updateRedisSeed

def updateAll():
    updateAllCache()
    updateRedisSeed(mode='in')
    updateRedisSeed(mode='out')

def updateIn():
    updateInCache()
    updateRedisSeed(mode='in')

def updateOut():
    updateOutCache()
    updateRedisSeed(mode='out')

if __name__ == '__main__':
    updateAll()