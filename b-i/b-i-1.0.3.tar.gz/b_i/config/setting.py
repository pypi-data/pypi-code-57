#!/usr/bin/env python3
# coding: utf-8

import os
from configparser import ConfigParser

configPath = "{}/{}".format(os.environ['HOME'], ".b-i")

if os.path.exists(configPath) is True:
    cp = ConfigParser()
    cp.read(configPath, encoding='utf-8')
    HIVE_URI = {
        "HOST": cp.get("hive", "host"),
        "PORT": int(cp.get("hive", "port")),
        "DATABASE": cp.get("hive", "database"),
        "USER": cp.get("hive", "user"),
        "PASSWORD": cp.get("hive", "password"),
        "AUTH": cp.get("hive", "auth")
    }

    MYSQL_URI = {
        "HOST": cp.get("mysql", "host"),
        "PORT": int(cp.get("mysql", "port")),
        "DATABASE": cp.get("mysql", "database"),
        "USER": cp.get("mysql", "user"),
        "PASSWORD": cp.get("mysql", "password")
    }

    LOG_INFO = {
        "LEVEL": cp.get("log", "level"),
        "NAME": cp.get("log", "name"),
        "PATH": cp.get("log", "path"),
        "TIPS": cp.get("log", "tips")
    }

else:
    HIVE_URI = {
        "HOST": "127.0.0.1",
        "PORT": 10000,
        "DATABASE": "default",
        "USER": "b-i",
        "PASSWORD": "123456",
        "AUTH": "LDAP"
    }

    MYSQL_URI = {
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "DATABASE": "default",
        "USER": "b-i",
        "PASSWORD": "123456",
    }

    LOG_INFO = {
        "LEVEL": "INFO",
        "NAME": "b-i",
        "PATH": "/tmp/b-i.log",
        "TIPS": "true"
    }
    cp = ConfigParser()
    cp.add_section("hive")
    cp.set("hive", "host", HIVE_URI["HOST"])
    cp.set("hive", "port", str(HIVE_URI["PORT"]))
    cp.set("hive", "database", HIVE_URI["DATABASE"])
    cp.set("hive", "user", HIVE_URI["USER"])
    cp.set("hive", "password", HIVE_URI["PASSWORD"])
    cp.set("hive", "auth", HIVE_URI["AUTH"])

    cp.add_section("mysql")
    cp.set("mysql", "host", MYSQL_URI["HOST"])
    cp.set("mysql", "port", str(MYSQL_URI["PORT"]))
    cp.set("mysql", "database", MYSQL_URI["DATABASE"])
    cp.set("mysql", "user", MYSQL_URI["USER"])
    cp.set("mysql", "password", MYSQL_URI["PASSWORD"])

    cp.add_section("log")
    cp.set("log", "level", LOG_INFO["LEVEL"])
    cp.set("log", "name", LOG_INFO["NAME"])
    cp.set("log", "path", LOG_INFO["PATH"])
    cp.set("log", "tips", LOG_INFO["TIPS"])
    with open(configPath,"w+") as f:
        cp.write(f)
    print(
        '''
        \033[1;31m
        TIPS!!!
        ---------------------------------------
        You must config your database infomation in: {} for the first time
        \033[0m
        '''.format(configPath)
    )

if LOG_INFO["TIPS"] == "true":
    print(
            '''
            \033[1;31m
            TIPS!!!
            ---------------------------------------
            configuration file path: {}
            log path: {}
            \033[0m
            '''.format(configPath, LOG_INFO["PATH"])
    )