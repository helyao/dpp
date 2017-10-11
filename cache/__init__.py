# -*- coding: utf-8 -*-
"""
Update Cache Module @ Helyao
-------------------------------------------------
Interfaces:
    Single Caching:
        updateUsProxyCache: update us-proxy html caching
        updateKuaiProxyCache: update kuai-proxy html caching
        updateXiciProxyCache: update xici-proxy html caching
    Mode Caching:
        updateInCache:  update in-firewall html caching
        updateOutCache: update out-firewall html caching
    All Caching:
        updateAllCache: update all html caching
-------------------------------------------------
Change Logs:
    2017-09-27  create
    2017-10-09  update, add xici proxy source
"""
from cache.usProxy import ProxyCache as UsProxyCache
from cache.kuaiProxy import ProxyCache as KuaiProxyCache
from cache.xiciProxy import ProxyCache as XiciProxyCache

# cache.usProxy.ProxyCache
def updateUsProxyCache():
    pc = UsProxyCache()
    pc.cache()

# cache.kuaiProxy.ProxyCache
def updateKuaiProxyCache():
    pc = KuaiProxyCache()
    pc.cache()

# cache.xiciProxy.ProxyCache
def updateXiciProxyCache():
    pc = XiciProxyCache()
    pc.cache()

# Update in-firewall proxy HTML caching
def updateInCache():
    updateKuaiProxyCache()
    updateXiciProxyCache()

# Update out-firewall proxy HTML caching
def updateOutCache():
    updateUsProxyCache()

# Update both in-firewall and out-firewall
def updateAllCache():
    updateInCache()
    updateOutCache()

if __name__ == '__main__':
    updateOutCache()


