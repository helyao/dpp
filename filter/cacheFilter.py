# -*- coding: utf-8 -*-
"""
Proxy Filter Module @ Helyao
-------------------------------------------------
Interfaces:
    CacheFilter: filter from cache to workin db, and
    when cache db is empty, copy seed db to cache.
-------------------------------------------------
Change Logs:
    2017-10-09  create
"""
import os
from filter import vaildProxy
from persist import rdb

class CacheFilter():
    def __init__(self, mode='in'):
        self.db = rdb[mode]
        self.mode = mode

    def _handler(self):
        try:
            proxy = self.db.getCacheProxy()
            print(proxy)
            if proxy:   # get a cache proxy
                bool = vaildProxy(proxy=proxy, mode=self.mode)
                if bool == True:
                    print('CacheFilter() found vaild proxy = {}'.format(proxy))
                    self.db.cache2Workin(proxy)
                else:
                    print('CacheFilter() found invaild proxy = {}'.format(proxy))
                    self.db.delCache(proxy)
            else:       # empty
                print('CacheFilter() warning: cache proxy pool is empty')
                self.db.copySeedToCache()
        except Exception as ex:
            print('Cache Filter error: {}'.format(ex))

    def run(self):
        print('Press Ctrl+{} to exit'.format('Break' if os.name == 'nt' else 'C'))
        while True:
            self._handler()

def run(mode='in'):
    cf = CacheFilter(mode=mode)
    cf.run()

if __name__ == '__main__':
    run()