# -*- coding: utf-8 -*-
"""
Update Seed Module @ Helyao
-------------------------------------------------
Interfaces:
    OutProxy: update seed proxies from out-firewall cache
-------------------------------------------------
Change Logs:
    2017-09-27  create
"""
import os
from bs4 import BeautifulSoup
from persist import rdb


class OutProxy():
    """
    Update out-firewall proxy from HTML:
    [
        '<Root>/cache/ofirewall/us-proxy.html',
        '<Root>/cache/ofirewall/ssl-proxy.html',
        '<Root>/cache/ofirewall/socks-proxy.html'
    ]
    """
    def __init__(self):
        cur_path = os.path.dirname(__file__)
        self.pages = {
            'us-proxy': os.path.join(cur_path, r'..\cache\ofirewall\us-proxy.html'),
            'ssl-proxy': os.path.join(cur_path, r'..\cache\ofirewall\ssl-proxy.html'),
            'socks-proxy': os.path.join(cur_path, r'..\cache\ofirewall\socks-proxy.html')
        }

    def __update(self, file):
        proxies = []
        with open(file, 'r', encoding='utf-8') as html:
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
            trs = soup.select('#proxylisttable tr')
            for tr in trs:
                num = 0
                ip = ''
                port = ''
                for td in tr.findChildren('td'):
                    num += 1
                    if num == 1:
                        ip = td.text.strip()
                    elif num == 2:
                        port = td.text.strip()
                    else:
                        break
                if ip != '' and port != '':
                    proxy = '{}:{}'.format(ip, port)
                    proxies.append(proxy)
        return proxies

    def update(self):
        for key in self.pages.keys():
            print('Update out-firewall proxies from {}.html'.format(key))
            list = self.__update(self.pages[key])
            for proxy in list:
                rdb['out'].add2Seed(proxy)

if __name__ == '__main__':
    oproxy = OutProxy()
    oproxy.update()
