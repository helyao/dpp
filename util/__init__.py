# -*- coding: utf-8 -*-
"""
Common Functions Module @ Helyao
-------------------------------------------------
Interfaces:
    user_agent_list: common used agents
    getAgentRandom: get random agent string
    cacheHTML: cache html to string
-------------------------------------------------
Change Logs:
    2017-09-26  create
    2017-09-27  update: add cacheHTMLSeries()
"""
import time
import random
import requests
from persist import rdb

user_agent_list = [
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
    "MQQBrowser/25 (Linux; U; 2.3.3; zh-cn; HTC Desire S Build/GRI40;480*800)",
    "Mozilla/5.0 (Linux; U; Android 2.3.3; zh-cn; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (SymbianOS/9.3; U; Series60/3.2 NokiaE75-1 /110.48.125 Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/413 (KHTML, like Gecko) Safari/413",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8J2",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A5313e Safari/7534.48.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; SAMSUNG; OMNIA7)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; XBLWP7; ZuneWP7)",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    "Mozilla/4.0 (compatible; MSIE 60; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)"
]

def getAgentRandom():
    global user_agent_list
    return user_agent_list[random.randint(0, (len(user_agent_list) - 1))]

def cacheHTMLSeries(url, agent=None, cookies=None, timeout=10, num_retries=2):
    """
    Cache HTML to String, accessing with same session and without proxy
    :param url: HTML url for caching
    :param agent: User-agent
    :param cookies: Request cookies
    :param timeout:  Request timeout
    :param num_retries: Number of retries
    :return: HTML content
    """
    if agent == None:
        agent = getAgentRandom()
    headers = {'User-agent': agent}
    try:
        response = requests.get(url, headers=headers, timeout=timeout, cookies=cookies)
        code = response.status_code
        if (num_retries > 0):
            if (500 <= code < 600):
                time.sleep(5 + random.random() * 5)  # sleep 5 ~ 10s
                return cacheHTMLSeries(url, agent=agent, cookies=cookies, timeout=timeout, num_retries=(num_retries - 1))
        else:
            return None
        html = response.text
        return html
    except requests.ReadTimeout as ex:
        print('Cache Timeout: {ex}'.format(ex=ex))
        time.sleep(5 + random.random() * 5)  # sleep 5 ~ 10s
        return cacheHTMLSeries(url, agent=agent, cookies=cookies, timeout=timeout, num_retries=(num_retries - 1))
    except Exception as ex:
        print('Cache error: {ex}'.format(ex=ex))
        return


def cacheHTML(url, proxy=True, firewall=False, timeout=10, num_retries=2, mode='in'):
    """
    Cache HTML to String
    :param url: HTML url for caching
    :param proxy: Use proxy or not
    :param firewall: Use in-firewall or out-firewall proxy
    :param timeout: Request timeout
    :param num_retries: Number of retries
    :return: HTML content
    """
    print('Cache the HTML: {url}'.format(url=url))
    user_agent = getAgentRandom()
    headers = {'User-agent': user_agent}
    if proxy == False:
        # Without proxy, need random waiting time between retries
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            code = response.status_code
            if (num_retries > 0):
                if (500 <= code < 600):
                    time.sleep(5 + random.random() * 5) # sleep 5 ~ 10s
                    return cacheHTML(url, proxy=proxy, firewall=firewall, timeout=timeout, num_retries=(num_retries-1), mode=mode)
            else:
                return None
            html = response.text
            return html
        except requests.ReadTimeout as ex:
            print('Cache Timeout: {ex}'.format(ex=ex))
            time.sleep(5 + random.random() * 5)  # sleep 5 ~ 10s
            return cacheHTML(url, proxy=proxy, firewall=firewall, timeout=timeout, num_retries=(num_retries-1), mode=mode)
        except Exception as ex:
            print('Cache error: {ex}'.format(ex=ex))
            return
    else:
        # With proxy
        if mode not in ['in', 'out']:
            print("Warning: proxy mode should be 'in' or 'out', change to without proxy mode")
            return cacheHTML(url, proxy=False, firewall=firewall, timeout=timeout, num_retries=num_retries, mode=mode)
        proxy = rdb[mode].getProxy()
        if proxy is None:
            # If proxy poll is empty, change mode to without proxy caching
            print('Warning: proxy-pool is empty, change to without proxy mode')
            return cacheHTML(url, proxy=False, firewall=firewall, timeout=timeout, num_retries=num_retries, mode=mode)
        proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
            code = response.status_code
            if (num_retries > 0):
                if (500 <= code < 600):
                    return cacheHTML(url, proxy=proxy, firewall=firewall, timeout=timeout, num_retries=(num_retries-1), mode=mode)
            else:
                return None
            html = response.text
            return html
        except requests.ReadTimeout as ex:
            print('Cache Timeout: {ex}'.format(ex=ex))
            return cacheHTML(url, proxy=proxy, firewall=firewall, timeout=timeout, num_retries=(num_retries-1), mode=mode)
        except Exception as ex:
            print('Cache error: {ex}'.format(ex=ex))
            return

if __name__ == '__main__':
    # html = cacheHTML('http://www.baidu.com', proxy=True)
    # print(html)
    agent = getAgentRandom()
    html = cacheHTMLSeries('http://www.baidu.com', agent=agent)
    print(html)