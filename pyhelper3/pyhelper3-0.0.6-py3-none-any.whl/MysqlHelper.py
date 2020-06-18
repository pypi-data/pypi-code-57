# -*- coding: utf-8 -*-
import pymysql,datetime
from queue import Queue
class MysqlHelper:
    def __init__(self,db_host,db_port,username,password,db_name,charset=None,maxconn = 5):
        self.maxconn = maxconn
        self.pool = Queue(maxconn)
        for i in range(maxconn):
            try:
                conn = pymysql.connect(host=db_host,port=db_port,user=username,
                                                  password=password,db=db_name)
                
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)


    def close(self):
        for i in range(self.maxconn):
            self.pool.get().close()
    def insert_many(self,sql,data=None):
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        with cursor:
            try:
                cursor.executemany(sql,data)
                conn.commit()
            except Exception as e:
                conn.rollback()
        self.pool.put(conn)
    def insert(self,sql,params=None):
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        with cursor:
            try:
                cursor.execute(sql,params)
                conn.commit()
            except Exception as e:
                conn.rollback()
        self.pool.put(conn)
    def update(self,sql,params=None):
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        with cursor:
                try:
                    cursor.execute(sql,params)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
        self.pool.put(conn)
    def query(self,sql):
        conn = self.pool.get()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        json_data = []
        with cursor:
                try:
                    count = cursor.execute(sql)
                    keys = []
                    json_data = cursor.fetchall()
                    conn.commit()
                except Exception as e:
                    print("数据库查询出错:{0},sql:{1}".format(str(e),sql))
                    conn.rollback()
        self.pool.put(conn)
        return json_data
'''
if row[q].year >= 1900:
str_time = row[q].strftime('%Y-%m-%d %H:%M:%S')
else:
str_time = '{0.year:4d}-{0.month:0>2d}-{0.day:0>2d} {0.hour:0>2d}:{0.minute:0>2d}:{0.second:0>2d}'.format(
row[q])'''