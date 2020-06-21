# -*- coding: utf-8 -*-
import pymysql
def connect():
    return pymysql.connect(host = 'localhost',
                           user = 'kheyrollah',
                           password = 'kh@123',
                           database = 'telegram_2')



