# -*- coding: utf-8 -*-
"""
    Python Database Connectivity lib
"""
# import sys
# sys.path.append('/home/apps/xapEtlPython/pydbclib-master/pydbclib')

# import os
# os.chdir('/home/apps/xapEtlPython/pydbclib-master/pydbclib')
# print("__init__.py的当前路径是：",os.getcwd())


from pydbclib.database import Database
from pydbclib.drivers import CommonDriver, SQLAlchemyDriver


__author__ = "liyatao"
__version__ = '2.1.8'

"""
传入：
driver ---如：Engine(mysql+pymysql://root:***@47.92.223.90:3306/song)

返回：
Database(driver_class(*args, **kwargs)) ---<pydbclib.database.Database object at 0x7f99698faeb8>
"""
def connect(*args, **kwargs):
    #这里获取“driver”的参数，如果没有，默认把“driver”置为sqlalchemy
    driver = kwargs.get("driver", "sqlalchemy")
    #Engine(mysql+pymysql://root:***@47.92.223.90:3306/song)
    print("driver......../",driver)
    if isinstance(driver, str):
        print('driver.lower()............../',driver.lower())
        print('SQLAlchemyDriver............../',SQLAlchemyDriver)
        print('CommonDriver............../',CommonDriver)
        print('1111')
        #<class 'pydbclib.drivers.SQLAlchemyDriver'>
        driver_class = {"sqlalchemy": SQLAlchemyDriver}.get(driver.lower(), CommonDriver)
        print('driver_class。。。。。。。',driver_class)
    elif hasattr(driver, "cursor"):
        print('222')
        driver_class = CommonDriver
    else:
        #访问mysql，会进入这里；
        print('333')
        driver_class = SQLAlchemyDriver
    print('Database(driver_class(*args, **kwargs)),......',Database(driver_class(*args, **kwargs)))
    #返回的是<pydbclib.database.Database object at 0x7f99698faeb8>
    #Database 是继承了抽象基类BaseDatabase的子类；
    return Database(driver_class(*args, **kwargs))
