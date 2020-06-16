#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/25 17:05
# @Author : yangpingyan@gmail.com

import os, json, inspect, sys
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import inspect
from sqlalchemy import MetaData, Table
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Sequence,
    Float
)


def sql_connect(sql_file, ssh_pkey=None):
    '''连接数据库'''
    with open(sql_file, encoding='utf-8') as f:
        sql_info = json.load(f)
        ssh_host = sql_info['ssh_host']
        ssh_user = sql_info['ssh_user']
        sql_address = sql_info['sql_address']
        sql_user = sql_info['sql_user']
        sql_password = sql_info['sql_password']
        database = sql_info['database']

        if ssh_pkey is not None:
            server = SSHTunnelForwarder((ssh_host, 22), ssh_username=ssh_user, ssh_pkey=fr"{ssh_pkey}",
                                        remote_bind_address=(sql_address, 3306))
            server.start()
            host="127.0.0.1"
            port = server.local_bind_port
        else:
            host = sql_address
            port = 3306

        sql_engine = create_engine(f'mysql+mysqldb://{sql_user}:{sql_password}@{host}:{port}/{database}?charset=utf8')

    return sql_engine

# sql_engine = create_engine('sqlite:///:memory:')  # sqlite database in memory






if __name__ == '__main__':


    # db_uri = URL(**db_uri_qizu)
    db_uri = 'sqlite:///db.sqlite'
    # engine = create_engine(db_uri)


    class Engine():
        def __init__(self, conn=db_uri):
            self.engine = create_engine(conn, encoding='utf8')  # 这engine直到第一次被使用才真实创建

        def execute(self, sql, **kwargs):
            """含commit操作，返回<class 'sqlalchemy.engine.result.ResultProxy'>"""
            return self.engine.execute(sql, **kwargs)

        def fetchall(self, sql):
            return self.execute(sql).fetchall()  # 能解释CLOB

        def fetchone(self, sql, n=999999):
            result = self.execute(sql)
            for _ in range(min(n, result.rowcount)):
                yield result.fetchone()  # <class 'sqlalchemy.engine.result.RowProxy'>

        def fetchone_dt(self, sql, n=999999):
            result = self.execute(sql)
            columns = result.keys()
            length = len(columns)
            for _ in range(n):
                one = result.fetchone()
                if one:
                    yield {columns[i]: one[i] for i in range(length)}

        def get_table_info(self):
            # Get table information
            inspector = inspect(self.engine)
            return inspector.get_table_names()

        def get_columns_info(self, table_name):
            # Get column information
            inspector = inspect(self.engine)
            return inspector.get_columns(table_name)




    class ORM(Engine):
        """对象关系映射（Object Relational Mapping）"""
        def __init__(self, *args):
            super().__init__(*args)
            _Session = sessionmaker(bind=self.engine)  # 创建ORM基类
            self.session = _Session()  # 创建ORM对象

        def __del__(self):
            self.session.close()

        def add(self, tb_obj):
            self.session.add(tb_obj)  # 添加到ORM对象
            self.session.commit()  # 提交

    # Create table with same columns
    Base = declarative_base()
    class TemplateTable(object):
        id   = Column(Integer, primary_key=True)
        create_time = Column(DateTime)
        update_time  = Column(DateTime)
        deleted  = Column(Integer)
        version  = Column(Integer)

    class Goods(TemplateTable, Base):
        __tablename__ = "goods"

    class GoodsInfo(TemplateTable, Base):
        __tablename__ = "goods_info"
        goods_id  = Column(Integer, ForeignKey('goods.id'))
        code  = Column(String(50))
        subtitle  = Column(String(255))
        goods_intro  = Column(String)
        goods_image_json  = Column(String)
        sell_id  = Column(String(100))
        sell_name  = Column(String(100))
        goods_detail_json  = Column(String)
        user_coupon_id  = Column(Integer)


    class GoodsCategory(TemplateTable, Base):
        __tablename__ = "goods_category"

    Base.metadata.create_all(bind=engine)

    # check table exists
    inspect(engine).get_table_names()


    orm = ORM(db_uri)
    orm.execute('create table if not EXISTS t1(sid int PRIMARY KEY ,name char(32));')  # 建表
    orm.execute('insert into t1 values(%(sid)s,%(name)s);', name='egon2', sid=1)  # 插入
    orm.execute('insert into t1(sid, name) values(%s,%s);', ['egon7',2])  # 插入
    for dt in orm.fetchone_dt('select * from t1;'):
        print(dt)
    orm.execute('drop table t1;')  # 删表
    orm.get_table_info()

    for dt in orm.fetchone('select * from goods ;'):
        print(dt)


if __name__ == '__main__':
    print("Mission start!")
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
    exec_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if 'ypyapi' not in exec_path:
        exec_path = os.path.join(exec_path, 'ypyapi')

    sql_engine = sql_connect( os.path.join(exec_path, 'bi_db.json'))

    # 创建对象的基类:
    Base = declarative_base()

    # 定义User对象:
    class User(Base):
        # 表的名字:
        __tablename__ = 'user'

        # 表的结构:
        id = Column(String(20), primary_key=True)
        name = Column(String(20))

        # 初始化数据库连接:
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=sql_engine)

    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = User(id='5', name='Bob')
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter(User.id=='5').one()
    # 打印类型和对象的name属性:
    print('type:', type(user))
    print('name:', user.name)
    # 关闭Session:
    session.close()



    print("Mission complete!")



    from sqlalchemy import (create_engine, Table, Column, Integer,
    String, MetaData)
    meta = MetaData()
    cars = Table('bus', meta,
         Column('Id', Integer, primary_key=True),
         Column('Name', String),
         Column('Price', Integer)
    )

    meta = MetaData()
    meta.reflect(bind=sql_engine)

    for table in meta.tables:
        print(table)