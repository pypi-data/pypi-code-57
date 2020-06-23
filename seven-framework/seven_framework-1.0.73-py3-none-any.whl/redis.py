# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 14:38:22
@LastEditTime: 2020-05-12 16:17:32
@LastEditors: ChenXiaolei
@Description: redis helper
"""

import redis


class RedisHelper:
    @classmethod
    def redis_init(self, host, port, db, password=None):
        """
        @description: 从redis连接池中创建对象
        @param host:主机地址
        @param port:端口
        @param db:redis_db
        @param password:授权密码
        @return: redis客户端对象
        @last_editors: ChenXiaolei
        """
        pool = redis.ConnectionPool(host=host,
                                    port=port,
                                    db=db,
                                    password=password)
        redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
        return redis_client
