#!/usr/bin/env python3
# coding: utf-8

import datetime
import inspect
import sqlparse

from pyhive import hive
from contextlib import closing
from b_i.config.setting import HIVE_URI
from b_i.utils.log_handle import logHandle

class hiveClient(object):

    '''
    PASV CONNECT HIVE
    HIVE SQL FOR JOBS, ENJOY IT!
    "LDAP" AUTH , PLAIN
    todo: [no be completed]no testing , auto reconnect when the tcp connect disconnected.
    todo: [bug wait to be fixed] rowcount is not support by PyHive 2019-08, also hiveserver version is old not support "cursor.fetch_logs ()"
    '''

    def __init__(self):
        '''
        echo: Secondary confirm
        '''
        self.conn = None
        self.hive_uri = HIVE_URI
        self.logger = logHandle()

        self._affirm = False

    def __del__(self):
        if self.conn:
            self.conn.close()

    def config(self, hive_uri, password=None):
        '''

        :param hive_uri: one, for hive config; two, for hive multi account username.
        :param password:
        :return:
        '''
        if isinstance(hive_uri, dict) and password is None:
            self.hive_uri = self.lower_to_capital(hive_uri)
        elif isinstance(hive_uri, str) and isinstance(password, str):
            self.hive_uri = self.lower_to_capital(
                {
                    "USER": hive_uri,
                    "PASSWORD": password
                }
            )
        else:
            raise Exception('error parameters for config function')

        self.validate_settings(self.hive_uri)
        if self.conn:
            self.conn.close()
            self.conn = None

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise Exception('%s is not defined in parameters' % setting_key)

        required_settings = {'USER', 'PASSWORD'}

        for required_setting in required_settings:
            validate_setting(required_setting)

        if "DATABASE" not in settings:
            settings["DATABASE"] = HIVE_URI.get("DATABASE")
        if "HOST" not in settings:
            settings["HOST"] = HIVE_URI.get("HOST")
        if "PORT" not in settings:
            settings["PORT"] = HIVE_URI.get("PORT")
        if "AUTH" not in settings:
            settings["AUTH"] = "LDAP"

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
                    self.conn = hive.connect(
                        host=self.hive_uri.get('HOST'),
                        port=self.hive_uri.get('PORT'),
                        username=self.hive_uri.get('USER'),
                        database=self.hive_uri.get('DATABASE'),
                        auth=self.hive_uri.get('AUTH'),
                        password=self.hive_uri.get('PASSWORD'),
                    )
                except Exception as e:
                    self.logger.error(
                        "HIVE SQL Connect Exception: %s" % str(e)
                    )
            else:
                pass

            # noinspection PyCallingNonCallable
            return func(self, *args, **kwargs)
        return wrapper

    def lower_to_capital(self, dict_info):
        new_dict = {}
        for i, j in dict_info.items():
            new_dict[i.upper()] = j
        return new_dict

    @property
    @connect
    def get_cursor(self):
        return self.conn.cursor()

    @connect
    @confirm
    def exec_sql(self, sql, args=None):
        '''
        run HIVE SQL command on MySQLDB
        :param sql: hive sql, you know!
        :param args: paramters for sql format.
        :return:
        '''

        with closing(self.conn.cursor()) as cur:
            try:
                sql = sql.strip()
                sql = sql[:-1] if ";" in sql and sql[-1] == ";" else sql

                pre = datetime.datetime.now()
                if isinstance(args, (tuple, list)) and len(args) > 0 and isinstance(args[0], tuple):
                    for i in args:
                        cur.execute(sql, parameters=i)
                        self.conn.commit()
                else:
                    cur.execute(sql, parameters=args)
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
                        "not support hive_exec_sql",
                        "->".join(filestack),
                        sql,
                        self.escape_parameter(args)
                    )
                )

            except Exception as e:
                self.logger.error(
                    "HIVE SQL Rollback: %s" % str(e)
                )
                self.conn.rollback()

    @connect
    @confirm
    def read_sql(self, sql, args=None, rvt=tuple):
        '''
        return query result list from HIVE SQL
        :param sql: hive sql, you konw!
        :param rvt: returnValueType:set, list, str, dict. default type=set.
        :return:
        '''

        with closing(self.conn.cursor()) as cur:
            try:
                sql = sql.strip()
                sql = sql[:-1] if ";" in sql and sql[-1] == ";" else sql

                pre = datetime.datetime.now()
                cur.execute(sql, parameters=args)
                next = datetime.datetime.now()

                if rvt is dict:
                    colnames = [desc[0] for desc in cur.description]
                    sqlResultSet = list()
                    for tup in cur.fetchall():
                        sqlResultSet.append(dict(zip(colnames, tup)))
                else:
                    sqlResultSet = cur.fetchall()

                filestack = []
                for i in inspect.stack():
                    if "egg" not in i[1]:
                        if i.filename not in filestack:
                            filestack.append(i.filename)
                self.logger.info(
                    "Times: {}, Fetched: {}, Filename: {}, SQL: {}".format(
                        next - pre,
                        len(sqlResultSet),
                        "->".join(filestack),
                        sql
                    )
                )

                if rvt is tuple:
                    return tuple(sqlResultSet)
                elif rvt is list:
                    return list(sqlResultSet)
                elif rvt is str:
                    return str(sqlResultSet)
                elif rvt is dict:
                    return sqlResultSet
                else:
                    raise Exception("No support type for return value")
            except Exception as e:
                self.logger.error(
                    "HIVE SQL Query Failed: %s" % str(e)
                )

    def file_sql(self, path=None, args=None, query=False):
        '''
        read HIVE SQL from filepath.  format var . then execute

        :param path: the HIVE SQL file path.
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
                    "Format HIVE SQL file, failed! %s" % str(e)
                )

    def escape_parameter(self, parameter):
        '''
        safe esacpe
        :param parameter:
        :return:
        '''
        if None is parameter:
            return "None"
        elif isinstance(parameter, bytes):
            parameter = parameter.decode('utf-8')
        try:
            parameter = str(parameter)
        except Exception as e:
            parameter = "not support type for SQL PARAMETER TO LOG: %s" % str(e)

        return "'{}'".format(
            parameter
                .replace('\\', '\\\\')
                .replace("'", "\\'")
                .replace('\r', '\\r')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
        )

if __name__ == "__main__":
    pass