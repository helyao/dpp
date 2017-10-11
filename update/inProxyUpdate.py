# -*- coding: utf-8 -*-
"""
Update Seed Module @ Helyao
-------------------------------------------------
Interfaces:
    InProxy: update seed proxies from in-firewall cache
-------------------------------------------------
Change Logs:
    2017-10-09  create
"""

import os
from bs4 import BeautifulSoup
from persist import rdb

kuai_maxpage = 10
xici_maxpage = 10

class InProxy():
    """
    Update out-firewall proxy from HTML:
    [
        '<Root>/cache/ifirewall/kuai/kuai_inha_{}.html',
        '<Root>/cache/ifirewall/kuai/kuai_intr_{}.html',
        '<Root>/cache/ifirewall/xici/xici_nn_{}.html',
        '<Root>/cache/ifirewall/xici/xici_nt_{}.html',
        '<Root>/cache/ifirewall/xici/xici_wn_{}.html',
        '<Root>/cache/ifirewall/xici/xici_wt_{}.html'
    ]
    """
    def __init__(self):
        cur_path = os.path.dirname(__file__)
        self.pages = {
            'kuai-proxy': {
                'url': os.path.join(cur_path, r'..\cache\ifirewall\kuai\kuai_{}_{}.html'),
                'list': ['inha', 'intr'],
                'maxpage': kuai_maxpage
            },
            'xici-proxy': {
                'url': os.path.join(cur_path, r'..\cache\ifirewall\xici\xici_{}_{}.html'),
                'list': ['nn', 'nt', 'wn', 'wt'],
                'maxpage': xici_maxpage
            }
        }

    def __kuai_update(self, file):
        proxies = []
        with open(file, 'r', encoding='utf-8') as html:
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
            trs = soup.select('tbody tr')
            for tr in trs:
                ip = tr.select('td[data-title=IP]')[0].text
                port = tr.select('td[data-title=PORT]')[0].text
                if ip != '' and port != '':
                    proxy = '{}:{}'.format(ip, port)
                    proxies.append(proxy)
        return proxies

    def __xici_update(self, file):
        proxies = []
        with open(file, 'r', encoding='utf-8') as html:
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
            trs = soup.select('tr')
            for tr in trs:
                num = 0
                ip = ''
                port = ''
                for td in tr.findChildren('td'):
                    num += 1
                    if num == 1:    # country
                        continue
                    elif num == 2:  # ip
                        ip = td.text.strip()
                    elif num == 3:  # port
                        port = td.text.strip()
                    else:           # others
                        break
                if ip != '' and port != '':
                    proxy = '{}:{}'.format(ip, port)
                    proxies.append(proxy)
        return proxies

    def __update(self, file):
        key = file.split('\\')[-1].split('_')[0]
        if key == 'kuai':
            return self.__kuai_update(file)
        elif key == 'xici':
            return self.__xici_update(file)
        else:
            return []

    def update(self):
        for source in self.pages.keys():
            for key in self.pages[source]['list']:
                print('Update in-firewall proxies from {}-{}'.format(source, key))
                for page in range(1, (self.pages[source]['maxpage']+1)):
                    file = self.pages[source]['url'].format(key, page)
                    list = self.__update(file)
                    print(len(list))
                    print(list)
                    for proxy in list:
                        rdb['in'].add2Seed(proxy)

    def updateXici(self):
        source = 'xici-proxy'
        for key in self.pages[source]['list']:
            print('Update in-firewall proxies from {}-{}'.format(source, key))
            for page in range(1, (self.pages[source]['maxpage'] + 1)):
                file = self.pages[source]['url'].format(key, page)
                list = self.__update(file)
                print(len(list))
                print(list)
                for proxy in list:
                    rdb['in'].add2Seed(proxy)

    def updateKuai(self):
        source = 'kuai-proxy'
        for key in self.pages[source]['list']:
            print('Update in-firewall proxies from {}-{}'.format(source, key))
            for page in range(1, (self.pages[source]['maxpage'] + 1)):
                file = self.pages[source]['url'].format(key, page)
                list = self.__update(file)
                print(len(list))
                print(list)
                for proxy in list:
                    rdb['in'].add2Seed(proxy)


    def kuai_test(self):
        list = self.__kuai_update(r'D:/open/dpp/update\..\cache\ifirewall\kuai\kuai_inha_1.html')
        return list

    def xici_test(self):
        list = self.__kuai_update(r'D:/open/dpp/update\..\cache\ifirewall\xici\xici_nn_1.html')
        return list

def test():
    iproxy = InProxy()
    kuai_list = iproxy.kuai_test()
    print('Unit test for kuai proxy, len = {}'.format(len(kuai_list)))
    xici_list = iproxy.xici_test()
    print('Unit test for xici proxy, len = {}'.format(len(xici_list)))

if __name__ == '__main__':
    iproxy = InProxy()
    iproxy.update()

