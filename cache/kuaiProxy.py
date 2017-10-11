# -*- coding: utf-8 -*-
"""
Update KuaiDaili Cache Module @ Helyao
-------------------------------------------------
Interfaces:
    ProxyCache: caching the list of HTML files
-------------------------------------------------
Note:
    Get caching without proxy temporarily because
accessing needs cookie(with same proxy and agent).
-------------------------------------------------
Change Logs:
    2017-09-27  create
"""
import os
import re
import time
import random
import execjs
import requests
from bs4 import BeautifulSoup
from util import getAgentRandom, cacheHTMLSeries

maxpage = 10
timedeta = 10

"""
inha: High hiding
intr: Normal
"""
list = ['inha', 'intr']


class ProxyCache():
    def __init__(self):
        """
        Domain:
            http://www.kuaidaili.com
        Download:
            http://www.kuaidaili.com/free/inha/1/
            http://www.kuaidaili.com/free/intr/1/
        """
        cur_path = os.path.dirname(__file__)
        self.cache_path = os.path.join(cur_path, 'ifirewall/kuai')
        self.domain = 'http://www.kuaidaili.com'
        self.agent = getAgentRandom()
        self.cookie = self.__cookie()  # need execute after domain & headers

    def __cookie(self):
        headers = {'User-agent': self.agent}
        retries_num = 3
        bool = True
        while bool:
            if retries_num <= 0:
                bool = False
            retries_num -= 1
            try:
                response = requests.get(self.domain, timeout=20, headers=headers)
            except Exception as ex:
                print(ex)
                continue
            code = response.status_code
            if code == 521:  # Get the cookie from javascript
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                script = soup.select_one('script')
                jscript = script.text.strip().replace("""eval("qo=eval;qo(po);")""", 'return po').replace(
                    '''window.onload=setTimeout("''', '').replace('''", 200)''', '')
                item = jscript.split(';')
                js = execjs.compile(jscript.replace(item[0] + ';', '').strip())
                paras = re.findall(r'(\w+)\((\d+)\)', item[0])[0]
                res = js.call(paras[0], paras[1])
                cookies = {}
                str_cookies = res.split('\'')[1]
                res = re.findall(r'([A-Za-z0-9_]*)=([A-Za-z0-9_ -:/,]*)', str_cookies)
                for item in res:
                    cookies[item[0]] = item[1]
                return cookies
            else:
                continue

    def __cache(self, url):
        item = url.split('/')
        file = 'kuai_{}_{}.html'.format(item[-3], item[-2])
        print(file)
        with open(os.path.join(self.cache_path, file), 'w', encoding='utf-8') as html:
            content = cacheHTMLSeries(url, cookies=self.cookie, agent=self.agent)
            if content:
                html.write(content)
            else:
                return False
        return True

    def cache(self):
        for key in list:
            for page in range(1, (maxpage + 1)):
                url = '{}/free/{}/{}/'.format(self.domain, key, page)
                while not self.__cache(url):
                    print('[kuai-{}-proxy]Failed url: {}'.format(key, url))
                    time.sleep(timedeta + random.random() * timedeta)
                time.sleep(timedeta + random.random() * timedeta)
            print('[kuai-{}-proxy]Finish caching proxy HTMLs'.format(key))


if __name__ == '__main__':
    pc = ProxyCache()
    print(pc.cookie)
    print(pc.cache())

