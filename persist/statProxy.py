# -*- coding: utf-8 -*-
"""
Data Persistence Module @ Helyao
-------------------------------------------------
Interfaces:
    stat: used to get the statistics of proxy-pool
-------------------------------------------------
Change Logs:
    2017-09-26  create
"""
import redis
from config import config

class StatOperation():
    def __init__(self, mode='in'):
        __inusedconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_IN_USED_STAT_DB)
        __invaildconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_IN_VAILD_STAT_DB)
        __outusedconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_OUT_USED_STAT_DB)
        __outvaildconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_OUT_VAILD_STAT_DB)
        self.iurdb = redis.Redis(connection_pool=__inusedconn)
        self.ivrdb = redis.Redis(connection_pool=__invaildconn)
        self.ourdb = redis.Redis(connection_pool=__outusedconn)
        self.ovrdb = redis.Redis(connection_pool=__outvaildconn)
        self.mode = mode

    def vaildStat(self, str):
        if config.REDIS_STAT:
            if self.mode == 'in':
                self.ivrdb.incr(str)
            else:
                self.ovrdb.incr(str)

    def usedStat(self, str):
        if config.REDIS_STAT:
            if self.mode == 'in':
                self.iurdb.incr(str)
            else:
                self.ourdb.incr(str)

__istat = StatOperation(mode='in')
__ostat = StatOperation(mode='out')

stat = {'in': __istat, 'out': __ostat}

if __name__ == '__main__':
    __istat.vaildStat('Hello World')
    stat['in'].vaildStat('Hello World')
    __istat.usedStat('By Helyao')