# -*- coding: utf-8 -*-
"""
Proxy Filter Module @ Helyao
-------------------------------------------------
Interfaces:
    WorkinFilter: filter from workin to cache db, and
    when workin db is empty, wait the vaild db, and
    reduce the interval time.
-------------------------------------------------
Change Logs:
    2017-10-09  create
"""
import os
import time
from filter import vaildProxy
from persist import rdb

min_interval = 5

class WorkinFilter():
    def __init__(self, mode='in'):
        self.db = rdb[mode]
        self.mode = mode
        self.interval = min_interval

    def _handler(self):
        try:
            proxy = self.db.getProxy()
            print(proxy)
            if proxy:  # get a workin proxy
                self.interval = min_interval
                bool = vaildProxy(proxy=proxy, mode=self.mode)
                if bool == True:
                    print('WorkinFilter() found vaild proxy = {}'.format(proxy))
                else:
                    print('WorkinFilter() found invaild proxy = {}'.format(proxy))
                    self.db.workin2Cache(proxy)
            else:  # empty
                print('WorkinFilter() warning: workin proxy pool is empty')
                self.interval += 1
                print('WorkinFilter.interval = {}'.format(self.interval))
        except Exception as ex:
            print('Workin Filter error: {}'.format(ex))

    def run(self):
        print('Press Ctrl+{} to exit'.format('Break' if os.name == 'nt' else 'C'))
        while True:
            self._handler()
            time.sleep(self.interval)

def run(mode='in'):
    wf = WorkinFilter(mode=mode)
    wf.run()

if __name__ == '__main__':
    run()