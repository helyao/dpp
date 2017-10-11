# -*- coding: utf-8 -*-
"""
Main For Proxy Pool @ Helyao
-------------------------------------------------
Change Logs:
    2017-10-11  create
"""
from multiprocessing import Process

from filter.cacheFilter import run as CacheFilterRun
from filter.workinFilter import run as WorkinFilterRun

"""
Unit Test
"""
def modeA(mode='in'):
    proList = list()
    pro1 = Process(target=CacheFilterRun, args=(mode,), name='CacheFilter_1')
    proList.append(pro1)
    pro2 = Process(target=CacheFilterRun, args=(mode,), name='CacheFilter_2')
    proList.append(pro2)
    pro3 = Process(target=WorkinFilterRun, args=(mode,), name='WorkinFilter')
    proList.append(pro3)
    for pro in proList:
        pro.start()
    for pro in proList:
        pro.join()

if __name__ == '__main__':
    modeA(mode='out')