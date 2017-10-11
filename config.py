# -*- coding: utf-8 -*-
"""
Redis Database:
DB-1: Default DB number, with error prone operation
DB-2: Product in-firewall proxy-poll
DB-3: Product out-firewall proxy-poll
DB-4: Debug in-firewall proxy-poll
DB-5: Debug out-firewall proxy-poll
DB-6: Statistics of the times of getProxy() when mode = in
DB-7: Statistics of the times of cache2Workin() when mode = in
DB-8: Statistics of the times of getProxy() when mode = out
DB-9: Statistics of the times of cache2Workin() when mode = out
DB-x: Reserved
"""
class Config:
    REDIS_PORT = 6379
    REDIS_DB_SEED = 'proxy_seed'
    REDIS_DB_CACHE = 'proxy_cache'
    REDIS_DB_WORKIN = 'proxy_workin'
    REDIS_STAT = False
    REDIS_IN_USED_STAT_DB = 6
    REDIS_IN_VAILD_STAT_DB = 7
    REDIS_OUT_USED_STAT_DB = 8
    REDIS_OUT_VAILD_STAT_DB = 9
    API_PORT = 16666

class DebugLocalConfig(Config):
    REDIS_HOST = 'localhost'
    REDIS_IN_FIREWALL_DB = 4
    REDIS_OUT_FIREWALL_DB = 5
    REDIS_STAT = True

class ReleaseLocalConfig(Config):
    REDIS_HOST = 'localhost'
    REDIS_IN_FIREWALL_DB = 2
    REDIS_OUT_FIREWALL_DB = 3

class DebugServerConfig(Config):
    REDIS_HOST = '192.168.1.10'
    REDIS_IN_FIREWALL_DB = 4
    REDIS_OUT_FIREWALL_DB = 5

class ReleaseServerConfig(Config):
    REDIS_HOST = '192.168.1.10'
    REDIS_IN_FIREWALL_DB = 2
    REDIS_OUT_FIREWALL_DB = 3

config_list = {
    'debug_local': DebugLocalConfig,
    'release_local': ReleaseLocalConfig,
    'debug_server': DebugServerConfig,
    'release_server': ReleaseServerConfig
}

config = config_list['debug_local']



