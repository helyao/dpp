# -*- coding: utf-8 -*-
"""
Update Seed Module @ Helyao
-------------------------------------------------
Interfaces:
    updateRedisSeed: update seed proxies from html cached
-------------------------------------------------
Change Logs:
    2017-09-27  create
    2017-10-09  update: add mode=in updateRedisSeed()
"""
from persist import rdb
from update.outProxyUpdate import OutProxy
from update.inProxyUpdate import InProxy

def updateRedisSeed(mode='in'):
    if mode in ['in', 'out']:
        rdb[mode].emptySeed()
        if mode == 'in':
            iproxy = InProxy()
            iproxy.update()
        else:
            oproxy = OutProxy()
            oproxy.update()
    else:
        raise ValueError("Error: argument of updateRedisSeed should be 'in' or 'out'")


if __name__ == '__main__':
    try:
        updateRedisSeed(mode='out')
    except Exception as ex:
        print(ex)




