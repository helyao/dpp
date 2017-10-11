# -*- coding: utf-8 -*-
"""
Proxy Filter Module @ Helyao
-------------------------------------------------
Interfaces:

-------------------------------------------------
Change Logs:
    2017-10-09  create
"""
import requests
from random import choice
from util import getAgentRandom

IN_LIST = ['https://www.baidu.com/', 'https://www.jd.com/', 'https://www.taobao.com/']
OUT_LIST = ['https://www.google.com/', 'http://www.facebook.com/']

def vaildProxy(proxy, timeout=10, num_retries=2, mode='in'):
    if mode == 'in':
        url = choice(IN_LIST)
    elif mode == 'out':
        url = choice(OUT_LIST)
    else:
        print("Warning: proxy mode should be 'in' or 'out'")
        return False
    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    headers = {'User-agent': getAgentRandom()}
    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)
        code = response.status_code
        if (num_retries > 0):
            if (500 <= code < 600):
                return vaildProxy(proxy=proxy, timeout=timeout, num_retries=(num_retries-1), mode=mode)
        else:
            return False
        return True
    except requests.ReadTimeout as ex:
        print('Filter Timeout: {ex}'.format(ex=ex))
        return vaildProxy(proxy=proxy, timeout=timeout, num_retries=(num_retries - 1), mode=mode)
    except Exception as ex:
        print('Filter error: {ex}'.format(ex=ex))
        return False

if __name__ == '__main__':
    vaildProxy('1.194.148.7:25797')