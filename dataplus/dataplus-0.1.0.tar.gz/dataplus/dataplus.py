#!/usr/bin/python
# coding: utf-8

import cx_Oracle
import os,sys
import pymysql
import petl as etl
import time,datetime
from tqdm import tqdm
from configparser import ConfigParser
# import warnings
# warnings.filterwarnings("ignore")

import platform
system=platform.system()

os.environ['NLS_DATE_FORMAT'] = 'yyyy-mm-dd hh24:mi:ss'
os.environ['NLS_TIMESTAMP_FORMAT'] = 'yyyy-mm-dd hh24:mi:ss.ff6'
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'
if system == 'Windows':
    os.environ['ORACLE_HOME'] = 'C:\Oracle'
elif system == 'Linux':
    os.environ['ORACLE_HOME'] = '/opt/oracle/product/11.2.4/dbhome_1'
os.environ['PATH'] += ';'+os.environ['ORACLE_HOME']

def singleton (cls, *args, **kwargs):
    instances = {}
    def get_instance(*args, **kwargs):
        if args not in instances:
            instances[args] = cls(*args, **kwargs)
        return instances[args]
    return get_instance

@singleton
class CursorProxy(object):
    def __init__(self, cursor):
        self._cursor = cursor
    def executemany(self, statement, parameters, **kwargs):
        if "mysql" in str(type(self._cursor)):
            statement = statement.replace("INSERT", "REPLACE")
        return self._cursor.executemany(statement, parameters, **kwargs)
    def fetchone(self):
        row = self._cursor.fetchone()
        if row is not None:
            row = [str(x.read()) if isinstance(x, cx_Oracle.LOB) else x for x in row]
        return row
    def __getattr__(self, item):
        return getattr(self._cursor, item)
    def __iter__(self):
        return iter(self.fetchone, None)

@singleton
class DbTable:
    dbo = ''
    schema = ''
    tablename = ''
    timestampField = ''
    primaryKeys = ''
    columns = ()
    rowCount = 0
    def __init__(self, dbo, schema, tablename, timestampField):
        self.dbo = dbo
        self.schema = schema
        self.tablename = tablename
        self.timestampField = timestampField
        self.lastUpdatetime = self.getLastUpdatetime()
        self.rowCount = self.getCount()
        # self.columns = self.getColumns()
    def __repr__(self):
        return ("%s.%s" % (self.schema, self.tablename))
    def getLastUpdatetime(self):
        sql = "select max({timestamp}) from {schema}.{tablename}".format(timestamp=self.timestampField, schema=self.schema, tablename=self.tablename)
        self.dbo.execute(sql)
        rs = self.dbo.fetchone()
        updatetime = rs[0]
        self.lastUpdatetime = updatetime.strftime('%Y-%m-%d %H:%M:%S.%f') if updatetime is not None else '1970-01-01 08:00:01.000000'
        return self.lastUpdatetime
    def getCount(self):
        sql = "select count(1) from {schema}.{tablename}".format(schema=self.schema, tablename=self.tablename)
        self.dbo.execute(sql)
        rs = self.dbo.fetchone()
        count = rs[0]
        self.rowCount = count if count is not None else 0
        return self.rowCount
    def getColumns(self):
        table = etl.fromdb(self.dbo.connection, 'SELECT * FROM {tablename} WHERE 1=0'.format(tablename=self.tablename))
        self.columns = etl.header(table)
        return self.columns

@singleton
class sync:
    sourceDb = None
    targetDb = None
    sourceCursor = None
    targetCursor = None
    sourceTable = ''
    targetTable = ''
    targetSchema = ''
    tablelist = []
    sourceTimestampField = ''
    targetTimestampField = ''
    def __init__(self, configfile): #sourceDb, targetDb, sourceCursor, targetCursor, sourceTable, targetTable
        config = ConfigParser()
        config.read(configfile)
        self.sourceDb = cx_Oracle.Connection("%s/%s@%s:%s/%s" % (config.get("sourcedb", "user"), config.get("sourcedb", "password"), config.get("sourcedb", "host"), config.get("sourcedb", "port"), config.get("sourcedb", "database")))
        self.targetDb = pymysql.connect(host=config.get("targetdb", "host"), port=int(config.get("targetdb", "port")), user=config.get("targetdb", "user"), password=config.get("targetdb", "password"), database=config.get("targetdb", "database"), charset=config.get("targetdb", "charset"))#, cursorclass = pymysql.cursors.SSCursor)
        self.sourceCursor = self.sourceDb.cursor()
        self.targetCursor = self.targetDb.cursor()
        if "oracle" in str(type(self.sourceCursor)).lower():
            self.sourceSchema = config.get("sourcedb", "user")
        if "mysql" in str(type(self.sourceCursor)).lower():
            self.sourceSchema = config.get("sourcedb", "database")
        if "mysql" in str(type(self.targetCursor)).lower():
            self.targetCursor.execute("SET @@SQL_MODE='ANSI_QUOTES'")
            self.targetCursor.execute("set autocommit=0")
            self.targetSchema = config.get("targetdb", "database")
        # if not os.access("o2m.list", os.R_OK):
        #     print("No tables list found.")
        #     exit()
        # with open("o2m.list") as f:
        #     tablelist = f.readlines()
        self.tablelist = config.get("targetdb", "tablelist").split("\n")
        self.sourceTimestampField = config.get("sourcedb", "timestamp")
        self.targetTimestampField = config.get("targetdb", "timestamp")

    def synctable(self, sourceDb, targetDb, sourceTable, targetTable):
        sourceCursor = sourceDb.cursor()
        targetCursor = targetDb.cursor()
        affected_total = 0
        init_rowCount = targetTable.rowCount if targetTable.rowCount < sourceTable.rowCount else sourceTable.rowCount
        pbar = tqdm(total = sourceTable.rowCount, unit = 'records')
        pbar.update(init_rowCount)
        while sourceTable.lastUpdatetime > targetTable.lastUpdatetime:
            affected_rows = 0
            batchSize = 100000
            sql = "SELECT * FROM (SELECT * FROM {schema}.{tablename} WHERE {timestamp}>=to_timestamp('{last_updatetime}','yyyy-mm-dd hh24:mi:ss.ff6') ORDER BY {timestamp}) WHERE ROWNUM<={batch_size}".format(timestamp=sourceTable.timestampField, schema=sourceTable.schema, tablename=sourceTable.tablename, last_updatetime=targetTable.lastUpdatetime, batch_size=batchSize)
            table = etl.fromdb(lambda: CursorProxy(sourceDb.cursor()), sql)
            table2 = etl.fromdb(lambda: CursorProxy(targetDb.cursor()), "SELECT * FROM {schema}.{tablename} WHERE 1=0".format(schema=targetTable.schema, tablename=targetTable.tablename))
            sourceTable.columns = etl.header(table)
            targetTable.columns = etl.header(table2)
            for column in list(set(sourceTable.columns) - set(targetTable.columns)):
                table = etl.cutout(table, column)
            max_updatetime = table.cut(sourceTable.timestampField).skip(1).max()[0]
            table = table.sort(sourceTable.timestampField)
            etl.appenddb(table, CursorProxy(targetCursor), targetTable.tablename, schema=targetTable.schema, commit=True)
            affected_rows += targetCursor.rowcount
            targetTable.lastUpdatetime = max_updatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
            targetTable.rowCount += affected_rows
            pbar.update(affected_rows if init_rowCount+affected_total+affected_rows < sourceTable.rowCount else sourceTable.rowCount - init_rowCount - affected_total)
            affected_total += affected_rows
            pbar.set_description("%s %d records updated." % (targetTable.tablename, affected_total))
        pbar.close()

    def start(self):
        for tablename in list(reversed(self.tablelist)):
            tablename = tablename.strip()
            self.sourceTable = DbTable(self.sourceCursor, self.sourceSchema, tablename, self.sourceTimestampField)
            self.targetTable = DbTable(self.targetCursor, self.targetSchema, tablename, self.targetTimestampField)
            self.synctable(self.sourceDb, self.targetDb, self.sourceTable, self.targetTable)

if __name__ == '__main__':
    app = sync("sync.ini")
    app.start()
