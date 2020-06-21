'''
Documentation: 处理redis的。
引用包名是atBasicLibrary，引用本python文件，请使用Library  atBasicLibrary/redisLib.py。
'''

import redis
import rfApiTestLibrary.log as logger

def at_get_connection(host='127.0.0.1', port=6379,db=0,password=None,charset='utf-8'):
    '''
    Redis 连接。连接实际上是不会真的连redis的，只有在操作时候才真正连接redis.
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN : StrictRedis

   Examples:
       |       关键字       |  参数             |  参数     |  参数 |  参数               |  参数            |
       | at get connection | host='127.0.0.1' | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at get connection | host='127.0.0.1' | port=6379 | db=1  |                    |                 |
    '''
    # 判断port必须为整型
    if type(port) is not type(1):
        raise AssertionError("端口号port必须是整型：" + port)
    r = redis.StrictRedis(host=host, port=port, db=db,password=password,charset=charset,decode_responses=True)
    return r


def at_redis_set(name, value,host='127.0.0.1', port=6379,db=0,password=None,charset='utf-8', ex=None, px=None):
    '''
    插入一对键值对key,value.
   【name】: 就是key,String类型
   【value】: 就是value，类型不定
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
   【ex】： 设置TTL时间,单位是秒，Int类型。
   【px】: 设置TTL时间,单位是毫秒，Int类型。
    RETURN: 返回操作的结果。

    Examples:
       |       关键字   |  参数  |    参数  |  参数             |  参数      |  参数 |  参数               |  参数            |
       | at redis  set |   aa  |    123   |  host='127.0.0.1' | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at redis  set |   vv  |   sasda  |  host='127.0.0.1' | port=6379 | db=1  | ex=3600            |                 |
    '''
    r= at_get_connection(host=host, port=port,db=db,password=password,charset=charset)
    try:
        return r.set(name, value, ex=ex, px=px)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)

def at_redis_get(name,host='127.0.0.1', port=6379,db=0,password=None,charset='utf-8'):
    '''
    通过key获得value/
   【name】: 就是key,String类型
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN: String类型。

    Examples:
       |      关键字   |  参数  |  参数             |  参数     |  参数  |  参数               |  参数            |
       | at redis get |   aa  |  host='127.0.0.1' | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at redis get |   vv  | host='127.0.0.1'  | port=6379 | db=1  | ex=3600            |                 |
    '''
    r = at_get_connection(host=host, port=port, db=db, password=password, charset=charset)
    try:
        return r.get(name)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)

def at_redis_hset(name,key,value,host='127.0.0.1', port=6379,db=0,password=None,charset='utf-8'):
    '''
    插入redis key，内部键值对。
   【name】: key，String类型
   【key】:  内部key.String类型。
   【value】:  value. 不定类型。
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN : 返回操作的结果。

    Examples:
       |      关键字    |  参数  |  参数    |    参数 |  参数           |  参数     |  参数 |  参数               |  参数            |
       | at redis hset |   aa  |  vbb|    |  123   |  host=127.0.0.1 | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at redis hset |   vv  |   sasda  |  cccc  |  host=127.0.0.1 | port=6379 | db=1  | ex=3600            |                 |
    '''
    r = at_get_connection(host=host, port=port, db=db, password=password, charset=charset)
    try:
        return r.hset(name,key,value)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)

def at_redis_hget(name,key,host='127.0.0.1',port=6379,db=0,password=None,charset='utf-8'):
    '''
    通过key和内部key获得值。
   【name】: key，String类型
   【key】:  内部key.String类型。
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN : String类型。

    Examples:
       |      关键字    |  参数  |  参数    |    参数 |  参数             |  参数     |  参数 |  参数               |  参数            |
       | at redis hget |   aa  |  vbba    |  123   |  host='127.0.0.1' | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at redis hget |   vv  |   sasda  |  cccc  |  host='127.0.0.1' | port=6379 | db=1  | ex=3600            |                 |
    '''
    r = at_get_connection(host=host, port=port, db=db, password=password, charset=charset)
    try:
        return r.hget(name, key)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)

def at_redis_hmset(name,dictionary,host='127.0.0.1',port=6379,db=0,password=None,charset='utf-8'):
    '''
    插入redis key，多个内部键值对，也就是字典。
   【name】: key，String类型
   【dictionary】: 被插入的字典，字典类型
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN: 返回操作的结果。

    Examples:
       |    关键字       |  参数  |  参数                      |  参数             |  参数     |  参数 |  参数               |  参数            |
       | at redis hmset |   aa  | {"cc":"1231","dd":True}    |  host='127.0.0.1' | port=6379 | db=1  | password=1234567  | charset='utf-8' |
       | at redis hmset |   vv  | {"cc":"1231","dd":True}    |  host='127.0.0.1' | port=6379 | db=1  | ex=3600           |                 |
    '''
    r = at_get_connection(host=host, port=port, db=db, password=password, charset=charset)
    try:
        return r.hmset(name,dictionary)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)


def at_redis_hmget(name,keys,host='127.0.0.1',port=6379,db=0,password=None,charset='utf-8'):
    '''
    通过redis key，获得redis的值，这里是字典。
   【name】: key，String类型
   【host】: Redis server的IP或者hostname。String类型。默认是127.0.0.1。
   【port】: redis server的端口号。Int类型
   【db】: redis 数据库索引，默认是0。Int类型。
   【password】: redis server的密码。String类型，默认值是None。
   【charset】: 读取数据的encoding，String类型，默认是utf-8
    RETURN: String类型。

    Examples:
       |       关键字    |  参数  |  参数             |  参数     |  参数  |  参数               |  参数            |
       | at redis hmget |   aa  |  host='127.0.0.1' | port=6379 | db=1  | password=1234567   | charset='utf-8' |
       | at redis hmget |   vv  |  host='127.0.0.1' | port=6379 | db=1  | ex=3600            |                 |
    '''
    r = at_get_connection(host=host, port=port, db=db, password=password, charset=charset)
    try:
        return r.hmget(name,keys)
    except redis.ConnectionError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)
    except redis.AuthenticationError as e:
        logger.error(e)
        raise AssertionError('连接redis失败：%s' % e)


