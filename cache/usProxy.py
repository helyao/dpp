# -*- coding: utf-8 -*-
"""
Update Cache Module @ Helyao
-------------------------------------------------
Interfaces:
    ProxyCache: caching the list of HTML files
-------------------------------------------------
Change Logs:
    2017-09-27  create
"""
import os
import time
import random
from util import cacheHTML

timedeta = 10

list = {
    'us-proxy': 'https://www.us-proxy.org/',
    'socks-proxy': 'https://www.socks-proxy.net/',
    'ssl-proxy': 'https://www.sslproxies.org/'
}

class ProxyCache():
    def __init__(self):
        cur_path = os.path.dirname(__file__)
        self.cache_path = os.path.join(cur_path, 'ofirewall')

    def __cache(self, list):
        failed = {}
        for key in list.keys():
            file = '{}.html'.format(key)
            with open(os.path.join(self.cache_path, file), 'w', encoding='utf-8') as html:
                content = cacheHTML(list[key])
                if content:
                    html.write(content)
                else:
                    failed[key] = list[key]
            time.sleep(timedeta + random.random() * timedeta)
        return  failed

    def cache(self):
        bool = True
        failed = self.__cache(list)
        while bool:
            if len(failed.keys()) > 0:
                print('[us-proxy]Failed List: {}'.format(len(failed.keys())))
                print(failed.keys())
                failed = self.__cache(failed)
            else:
                bool = False
        print('[us-proxy]Finish caching proxy HTMLs')


if __name__ == '__main__':
    pc = ProxyCache()
    pc.cache()