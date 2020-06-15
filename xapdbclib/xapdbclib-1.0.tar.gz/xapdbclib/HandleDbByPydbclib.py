# -*- coding: utf-8 -*-

#这个地方修改系统路径后是可以找到不同路径下的pydbclib的；但是牵一发而动全身；pydbclib包中的系统路径也变了；都要改
# import sys
# sys.path.append('/home/apps/xapEtlPython/pydbclib-master')
# import os
# print("readMysql的路径：",os.getcwd())
# print("readMysql的路径：",os.path.abspath('.'))

import pydbclib
from sqlalchemy import create_engine
###################################################################获取数据库连接信息getDbConfig
"""
传入：
dbEngineUrl ---数据库连接url；
    Mysql --- "mysql+pymysql://root:root@47.92.223.90:3306/song"
    Oracle ---
    Hive --- "hive://47.92.223.90:10000/default"

readSql ---读取数据库的sql语句；
"""
class HandleDbByPydbclib():
    def __init__(self,dbEngineUrl,readSql):
        self.dbEngineUrl = dbEngineUrl
        self.readSql = readSql

    """
    read ---读数据库(Mysql/Oracle/Hive)
    返回：
        RecordsResult ---读出的数据库结果，是个list列表；
        [{'user_model_id': 1, 'model_name': '关键字模型1'},{...}...]      
    """
    def read(self):
        print('进入HandleDbByPydbclib的read方法')
        ###############################使用pydbclib读取各种数据库,这个先不用；
        engine = create_engine(self.dbEngineUrl)
        #建立数据库的链接；
        pydbclibConnect = pydbclib.connect(driver=engine)

        #get_all()获取全部；  .get_one()获取一条；
        RecordsResult = pydbclibConnect.read(self.readSql).get_all()
        return RecordsResult
        ###############################使用Presto读取各种数据库；

###################################################################################################pydbclib读取各种数据库测试
#---pydbclib读取Mysql数据库示例
# dbEngineUrl = "mysql+pymysql://root:root@47.92.223.90:3306/song"
# readSql = "select * from T_BUILD_MODEL"
# #实例化类HandleDbByPydbclib的对象；
# handleDbByPydbclib = HandleDbByPydbclib(dbEngineUrl,readSql)
#
# #读取Mysql数据库；
# mysqlResult = handleDbByPydbclib.read()
# print('mysqlResult..........', type(mysqlResult))
# print('mysqlResult..........', mysqlResult)

#---pydbclib读取Oracle数据库示例
# """
# Oracle数据库需要在集群的每一台服务器上都安装oracle的64位客户端；
# """
# dbEngineUrl = "oracle://bigdata:bigdata@47.92.223.90:3306/helowin"
# print('21111')
# readSql = "select * from T_BUILD_MODEL"
# #实例化类HandleDbByPydbclib的对象；
# handleDbByPydbclib = HandleDbByPydbclib(dbEngineUrl,readSql)
#
# #读取Oracle数据库；
# mysqlResult = handleDbByPydbclib.read()
# print('mysqlResult..........', type(mysqlResult))
# print('mysqlResult..........', mysqlResult)

#---pydbclib读取Hive数据库示例
# """
# 这里有一点注意：
# 47.92.223.90 上开通/配置了10000端口；才可以访问；
# 39.98.49.13 上没有开通/配置10000端口；不能访问；
# """
# dbEngineUrl = "hive://47.92.223.90:10000/default"
# # dbEngineUrl = "hive://39.98.49.13:10000/default"
# readSql = "show tables"
# #实例化类HandleDbByPydbclib的对象；
# handleDbByPydbclib = HandleDbByPydbclib(dbEngineUrl,readSql)
#
# #读取Hive数据库；
# mysqlResult = handleDbByPydbclib.read()
# print('mysqlResult..........', type(mysqlResult))
# print('mysqlResult..........', mysqlResult)

