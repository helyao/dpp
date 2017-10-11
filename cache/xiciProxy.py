# -*- coding: utf-8 -*-
"""
Update XiciDaili Cache Module @ Helyao
-------------------------------------------------
Interfaces:
    ProxyCache: caching the list of HTML files
-------------------------------------------------
Note:
    Xici url often change by official, need to change
    ProxyCache.cache() url string.
        http://www.xicidaili.com/nn/1
        http://www.xicidaili.com/free/nn/1
-------------------------------------------------
Change Logs:
    2017-09-28  create
"""
import os
import time
import random
from util import cacheHTML

maxpage = 10
timedeta = 10

"""
nn: High hiding
nt: Normal
wn: HTTPs
wt: HTTP
"""
list = ['nn', 'nt', 'wn', 'wt']


class ProxyCache():
    def __init__(self):
        """
        Domain:
            http://www.xicidaili.com
        Download:
            http://www.xicidaili.com/nn/1
            http://www.xicidaili.com/nt/1
            http://www.xicidaili.com/wn/1
            http://www.xicidaili.com/wt/1
        """
        cur_path = os.path.dirname(__file__)
        self.cache_path = os.path.join(cur_path, 'ifirewall/xici')
        self.domain = 'http://www.xicidaili.com'

    def __cache(self, url):
        item = url.split('/')
        file = 'xici_{}_{}.html'.format(item[-2], item[-1])
        print(file)
        with open(os.path.join(self.cache_path, file), 'w', encoding='utf-8') as html:
            content = cacheHTML(url)
            if content:
                html.write(content)
            else:
                return False
        return True

    def cache(self):
        for key in list:
            for page in range(1, (maxpage + 1)):
                url = '{}/{}/{}'.format(self.domain, key, page)
                while not self.__cache(url):
                    print('[xici-{}-proxy]Failed url: {}'.format(key, url))
                    time.sleep(timedeta + random.random() * timedeta)
                time.sleep(timedeta + random.random() * timedeta)
            print('[xici-{}-proxy]Finish caching proxy HTMLs'.format(key))


if __name__ == '__main__':
    pc = ProxyCache()
    pc.cache()