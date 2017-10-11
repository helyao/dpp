# -*- coding: utf-8 -*-
"""
Data Persistence Module @ Helyao
-------------------------------------------------
Interfaces:
    rdb: the handler of rdb with 'Singleton Pattern'
-------------------------------------------------
Change Logs:
    2017-09-04  create
    2017-09-26  update: add stat module
    2017-10-09  update: add getCacheProxy() method
"""

import os
import redis
from config import config
from persist.statProxy import stat

class PersistOperation:
    """
    There are three table:
    1. seed table: store all proxy-string from multi-source
    2. cache table: store proxies need to be detected
    3. workin table: store vaild proxy-string
    Relationships between tables:
    1. insert all proxies crawled to seed table
    2. when cache table null, copy all from seed
    3. when a proxy vaild in cache, switch it to workin table
    4. when a proxy invaild in workin, switch it to cache table
    """
    def __init__(self, mode='in'):
        # redis connection
        __inconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_IN_FIREWALL_DB)
        __inrdb = redis.Redis(connection_pool=__inconn)
        __outconn = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_OUT_FIREWALL_DB)
        __outrdb = redis.Redis(connection_pool=__outconn)
        self.rdb = {'in': __inrdb, 'out': __outrdb}
        self.mode = mode

    # clear seed table
    def emptySeed(self):
        self.rdb[self.mode].delete(config.REDIS_DB_SEED)

    # add a proxy string to seed
    def add2Seed(self, str):
        self.rdb[self.mode].sadd(config.REDIS_DB_SEED, str)

    # copy all from seed to cache
    def copySeedToCache(self):
        for str in self.rdb[self.mode].smembers(config.REDIS_DB_SEED):
            self.rdb[self.mode].sadd(config.REDIS_DB_CACHE, str.decode('utf-8'))

    # add a proxy string to cache
    def add2Cache(self, str):
        self.rdb[self.mode].sadd(config.REDIS_DB_CACHE, str)

    # delete a proxy string from cache
    def delCache(self, str):
        self.rdb[self.mode].srem(config.REDIS_DB_CACHE, str)

    # add a proxy string to workin
    def add2Workin(self, str):
        self.rdb[self.mode].sadd(config.REDIS_DB_WORKIN, str)

    # delete a proxy string from workin
    def delWorkin(self, str):
        self.rdb[self.mode].srem(config.REDIS_DB_WORKIN, str)

    # move a proxy string from workin to cache
    def workin2Cache(self, str):
        self.rdb[self.mode].smove(config.REDIS_DB_WORKIN, config.REDIS_DB_CACHE, str)

    # move a proxy string from cache to workin
    def cache2Workin(self, str):
        self.rdb[self.mode].smove(config.REDIS_DB_CACHE, config.REDIS_DB_WORKIN, str)
        stat[self.mode].vaildStat(str)

    # get a proxy
    def getProxy(self):
        if self.rdb[self.mode].scard(config.REDIS_DB_WORKIN) > 0:
            proxy = self.rdb[self.mode].srandmember(config.REDIS_DB_WORKIN, 1)[0].decode('utf-8')
            stat[self.mode].usedStat(proxy)
            return proxy
        else:
            return

    # get a cache proxy
    def getCacheProxy(self):
        if self.rdb[self.mode].scard(config.REDIS_DB_CACHE) > 0:
            proxy = self.rdb[self.mode].srandmember(config.REDIS_DB_CACHE, 1)[0].decode('utf-8')
            return proxy
        else:
            return

__irdb = PersistOperation(mode='in')
__ordb = PersistOperation(mode='out')

rdb = {'in': __irdb, 'out': __ordb}

if __name__ == '__main__':
    __irdb.copySeedToCache()
    __ordb.copySeedToCache()
    # __irdb.add2Seed('Hello World')
    # __ordb.add2Cache('By Helyao')
