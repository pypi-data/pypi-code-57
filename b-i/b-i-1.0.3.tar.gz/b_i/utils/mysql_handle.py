#!/usr/bin/env python3
# coding: utf-8

import pymysql
import inspect
import datetime
import sqlparse

from contextlib import closing
from b_i.config.setting import MYSQL_URI
from b_i.utils.log_handle import logHandle

class mysqlClient(object):

    '''
    PASV CONNECT MySQLDB
    Import packages without using them, not connect
    Auto to reconnect when connect downtimed.
    Long connect: when SQL timeout , try connect again
    self.logger: mysqlClient Class built-in loging
    '''

    def __init__(self):
        '''
        _affirm: Secondary confirm
        '''
        self.conn = None
        self.mysql_uri = MYSQL_URI
        self.logger = logHandle()

        self._affirm = False

    def __del__(self):
        if self.conn:
            self.conn.close()

    def config(self, mysql_uri):
        '''
        Display configuration database information
        Default: config.setting.MYSQL_URI
        :param mysql_uri: MySQL DB Information, Type: dict
        :return:
        '''
        self.mysql_uri = self.lower_to_capital(mysql_uri)
        self.validate_settings(self.mysql_uri)
        if self.conn:
            self.conn.close()
            self.conn = None

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise Exception('%s is not defined in parameters' % setting_key)

        required_settings = {'DATABASE', 'HOST', 'USER', 'PASSWORD', 'PORT'}

        for required_setting in required_settings:
            validate_setting(required_setting)

    @property
    def echo(self):
        '''
        Secondary confirmation, execute sql command
        :return:
        '''
        self._affirm = True if self._affirm is False else False

    def confirm(func):
        def wrapper(self, *args, **kwargs):
            if self._affirm is False:
                return func(self, *args, **kwargs)
            else:
                print(sqlparse.format(str.format(*args, **kwargs), reindent=True, keyword_case='upper'))
                isOK = input("DBLIB TIPS, this sql is corrent?: (yes/no)")
                if isOK in ["YES", "yes", "y", "Y"]:
                    return func(self, *args, **kwargs)
                else:
                    return 0
        return wrapper

    def connect(func):
        def wrapper(self, *args, **kwargs):
            if self.conn is None:
                try:
                    self.conn = pymysql.connect(
                        db=self.mysql_uri.get('DATABASE'),
                        host=self.mysql_uri.get('HOST'),
                        user=self.mysql_uri.get('USER'),
                        passwd=self.mysql_uri.get('PASSWORD'),
                        port=self.mysql_uri.get('PORT'),
                        charset='utf8'
                    )
                except Exception as e:
                    self.logger.error(
                        "MySQLDB Connect Exception: %s" % str(e)
                    )
            else:
                try:
                    self.conn.ping(reconnect=True)
                except Exception as e:
                    self.logger.error(
                        "MySQLDB Try ReConnect failed: %s" %str(e)
                    )

            # noinspection PyCallingNonCallable
            return func(self, *args, **kwargs)
        return wrapper

    def lower_to_capital(self, dict_info):
        new_dict = {}
        for i, j in dict_info.items():
            new_dict[i.upper()] = j
        return new_dict

    # noinspection PyArgumentList
    @property
    @connect
    def get_cursor(self):
        return self.conn.cursor()

    # noinspection PyArgumentList
    @connect
    @confirm
    def exec_sql(self, sql, args=None):
        '''
        run sql command on MySQLDB
        :param sql: exec sql
        :param args: (tuple, list or dict) – parameters used with query. (optional)
        :return:
        '''

        with closing(self.conn.cursor()) as cur:
            try:
                pre = datetime.datetime.now()
                if isinstance(args, (tuple, list)) and len(args) > 0 and isinstance(args[0], tuple):
                    cur.executemany(sql, args)
                else:
                    cur.execute(sql, args)
                self.conn.commit()
                next = datetime.datetime.now()

                filestack = []
                for i in inspect.stack():
                    if "egg" not in i[1]:
                        if i.filename not in filestack:
                            filestack.append(i.filename)
                self.logger.info(
                    "Times: {}, Fetched: {}, Filename: {}, SQL: {}, Para: {}".format(
                        next - pre,
                        cur.rowcount,
                        "->".join(filestack),
                        sql,
                        self.escape_parameter(args)
                    )
                )

            except Exception as e:
                self.conn.rollback()
                self.logger.error(
                    "MySQLDB Rollback: %s" % str(e)
                )

    # noinspection PyArgumentList
    @connect
    @confirm
    def read_sql(self, sql, args=None, rvt=tuple):
        '''
        return query result list from SQL
        :param sql: query sql
        :param args: (tuple, list or dict) – parameters used with query. (optional)
        :param rvt: returnValueType:tuple, list, str, dict. default type=tuple.
        :return:
        '''
        with closing(self.conn.cursor(cursor=pymysql.cursors.DictCursor if rvt is dict else None)) as cur:
            try:
                pre = datetime.datetime.now()
                cur.execute(sql, args)
                next = datetime.datetime.now()

                filestack = []
                for i in inspect.stack():
                    if "egg" not in i[1]:
                        if i.filename not in filestack:
                            filestack.append(i.filename)
                self.logger.info(
                    "Times: {}, Fetched: {}, Filename: {}, SQL: {}".format(
                        next-pre,
                        cur.rowcount,
                        "->".join(filestack),
                        sql
                    )
                )
                if rvt is tuple:
                    return tuple(cur.fetchall())
                elif rvt is list:
                    return list(cur.fetchall())
                elif rvt is str:
                    return str(cur.fetchall())
                elif rvt is dict:
                    return cur.fetchall()
                else:
                    raise Exception("No support type for return value")
            except Exception as e:
                self.logger.error(
                    "MySQLDB Query Failed: %s" % str(e)
                )

    def file_sql(self, path=None, args=None, query=False):
        '''
        read sql from filepath.  format var . then execute

        :param path: the sql file path.
        :param args: string, tuple, list, set,  dict for $.key
        :param query: False=exec_sql, True=read_sql, default:False
        :return: return read_sql result or exec_sql
        '''

        def replace_str_by_sequence(sql_str, args):
            '''
            if args is set, list or tuple, Replace strings by sequence
            '''
            new_str = ""
            temp_str = ""
            index = 0
            for i in sql_str:
                if i == " ":
                    if temp_str != "":
                        if '$.' in temp_str:
                            new_str = new_str + args[index] + i
                            index += 1
                        else:
                            new_str = new_str + temp_str + i
                        temp_str = ""
                else:
                    temp_str += i
            if temp_str != "":
                if '$.' in temp_str:
                    new_str = new_str + args[index]
                    index += 1
                else:
                    new_str = new_str + temp_str
            return new_str

        with open(path, "r") as f:
            sql_str = "".join([line for line in f.readlines()])
            sql_str = sql_str.strip()
            sql_str = sql_str[:-1] if ";" in sql_str and sql_str[-1] == ";" else sql_str

            try:
                if '%' in sql_str:
                    sql_str = sql_str % args
                elif '{' in sql_str and '}' in sql_str:
                    sql_str = sql_str.format(*args)
                elif '$.' in sql_str:
                    if isinstance(args, dict):
                        for k, v in args.items():
                            sql_str = sql_str.replace('$.{}'.format(k), v)
                    else:
                        sql_str = replace_str_by_sequence(sql_str, args)
                if query is False:
                    self.exec_sql(sql_str)
                else:
                    return self.read_sql(sql_str)
            except Exception as e:
                self.logger.error(
                    "Format MySQL file, failed! %s" % str(e)
                )

    def escape_parameter(self, parameter):
        '''
        safe esacpe
        :param parameter:
        :return:
        '''
        if None is parameter:
            return "None"
        elif isinstance(parameter, str):
            return pymysql.escape_string(parameter)
        elif isinstance(parameter, dict):
            return pymysql.escape_dict(parameter, charset="utf8")
        elif isinstance(parameter, (list, tuple, set)):
            return pymysql.escape_sequence(parameter, charset="utf-8")
        else:
            self.logger.warning(
                "No support type for MySQL ESCAPE!"
            )
            return parameter

if __name__ == '__main__':
    pass