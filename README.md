# 动态代理池

1. 使用公开免费代理搭建自己的动态代理池
2. 本代理池分为mode='in'的国内代理池，和mode='out'的国外代理池
3. 可以在Linux和Windows正常运行
4. 需要借助Redis做数据持久化

## 数据库
使用Redis做代理池数据持久化
> DB-1: Redis的默认登入db，为了防止意外操作导致数据丢失，不使用<br>
> DB-2: 正式运行的国内代理池<br>
> DB-3: 正式运行的国外代理池<br>
> DB-4: 调试运行的国内代理池<br>
> DB-5: 调试运行的国外代理池<br>
> DB-6: 国内代理池使用统计<br>
> DB-7: 国外代理池使用统计<br>
> DB-8: 国内代理池质量统计<br>
> DB-9: 国外代理池质量统计<br>
> DB-x: 保留，暂不使用

## 安装说明
1. 安装Python3
2. 安装Python Packages
> pip install -r requirements.txt

3. 安装Redis数据库

## 使用说明
1. 运行manager.updateProxyCache.py文件，用于更新proxy缓存文件
2. 运行manager.runProxyPool.py文件，可以启动动态代理池
3. 使用有效代理，提供三种方式：
    - 直接从Redis数据库相应库中取值
    - 使用python
    > from persist import rdb
    > rdb['in'].getProxy()
    > or
    > rdb['out'].getProxy()

    - 通过api接口调用
    > http://localhost:16666
    > or
    > http://localhost:16666/out

## 文件结构
1. /cache: 用于缓存代理源html文件
2. /filter: 用于验证过滤proxy_cache和proxy_proxy中代理
3. /persist: 结合Redis用于数据持久化操作
4. /update: 将/cache中的代理池cache文件更新到proxy_seed中
5. /util: 提供基本资源和方法
6. /web: 借助Flask提供代理池数据可视化
7. config.py: 配置项
8. /manager: 启动入口

## 代理源
#### 国内代理

#### 国外代理
https://www.us-proxy.org/
https://www.socks-proxy.net/
https://www.sslproxies.org/

## 注意事项
1. 在使用过程中，可以灵活改变proxy_cache和proxy_workin的filter数量以调整代理制资源占用和代理池质量
2. 当发现Redis的proxy_workin代理不足时，如果proxy_cache遍历速度过慢，可以增加proxy_cache的filter数量以在同时间获取更多可用代理
3. 当上一条中，增加了proxy_cache的filter数量后依然代理不足，需要更新一下代理池cache文件，保证cache的时效性


## 其他
1. [Redis客户端](https://redisdesktop.com/)

#### 如果对你有帮助，可否打赏一杯咖啡提神

