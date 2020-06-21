#!/usr/bin/python
# coding: utf-8

import cx_Oracle
import getopt,os,sys
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
class configparse(ConfigParser):
    def get(self, section, option):
        return ConfigParser.get(self = self, section = section, option = option, raw=True) if(self.has_option(section, option)) else None

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
    def __init__(self, configfile):
        config = configparse()
        config.read(configfile)
        self.sourceDb = cx_Oracle.Connection("%s/%s@%s:%s/%s" % (config.get("sourcedb", "user"), config.get("sourcedb", "password"), config.get("sourcedb", "host"), config.get("sourcedb", "port"), config.get("sourcedb", "instance") or config.get("sourcedb", "database")))
        self.targetDb = pymysql.connect(host=config.get("targetdb", "host"), port=int(config.get("targetdb", "port")), user=config.get("targetdb", "user"), password=config.get("targetdb", "password"), database=config.get("targetdb", "database"), charset=config.get("targetdb", "charset"))#, cursorclass = pymysql.cursors.SSCursor)
        self.sourceCursor = self.sourceDb.cursor()
        self.targetCursor = self.targetDb.cursor()
        if "oracle" in str(type(self.sourceCursor)).lower():
            self.sourceSchema = config.get("sourcedb", "schema") or config.get("sourcedb", "user")
        if "mysql" in str(type(self.sourceCursor)).lower():
            self.sourceSchema = config.get("sourcedb", "database")
        if "mysql" in str(type(self.targetCursor)).lower():
            self.targetCursor.execute("SET @@SQL_MODE='ANSI_QUOTES'")
            self.targetCursor.execute("set autocommit=0")
            self.targetSchema = config.get("targetdb", "database")
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
            sourceRecord = etl.fromdb(lambda: CursorProxy(sourceDb.cursor()), sql)
            targetRecord = etl.fromdb(lambda: CursorProxy(targetDb.cursor()), "SELECT * FROM {schema}.{tablename} WHERE 1=0".format(schema=targetTable.schema, tablename=targetTable.tablename))
            sourceTable.columns = etl.header(sourceRecord)
            targetTable.columns = etl.header(targetRecord)
            for column in list(set(sourceTable.columns) - set(targetTable.columns)):
                sourceRecord = etl.cutout(sourceRecord, column)
            max_updatetime = sourceRecord.cut(sourceTable.timestampField).skip(1).max()[0]
            sourceRecord = sourceRecord.sort(sourceTable.timestampField)
            etl.appenddb(sourceRecord, CursorProxy(targetCursor), targetTable.tablename, schema=targetTable.schema, commit=True)
            affected_rows += targetCursor.rowcount
            targetTable.lastUpdatetime = max_updatetime.strftime('%Y-%m-%d %H:%M:%S.%f')
            targetTable.rowCount += affected_rows
            pbar.update(affected_rows if init_rowCount+affected_total+affected_rows < sourceTable.rowCount else sourceTable.rowCount - init_rowCount - affected_total)
            affected_total += affected_rows
            pbar.set_description("%s |%d records updated." % (targetTable.tablename, affected_total))

        if targetTable.lastUpdatetime > sourceTable.lastUpdatetime:
            pbar.set_description("%s |timestamp >, skip." % (targetTable.tablename))
        elif targetTable.lastUpdatetime == sourceTable.lastUpdatetime and targetTable.rowCount == sourceTable.rowCount:
            pbar.set_description("%s |no data change." % (targetTable.tablename))
        elif targetTable.lastUpdatetime == sourceTable.lastUpdatetime and targetTable.rowCount > sourceTable.rowCount:
            pbar.set_description("%s |RowCount > but timestamp ==, skip." % (targetTable.tablename))
        elif targetTable.lastUpdatetime == sourceTable.lastUpdatetime and targetTable.rowCount < sourceTable.rowCount:
            pbar.set_description("%s |RowCount < but timestamp ==, skip." % (targetTable.tablename))
        pbar.close()

    def start(self):
        for tablename in list(reversed(self.tablelist)):
            tablename = tablename.strip()
            tableremap = tablename.split(' ')
            if len(tableremap) == 3:
                self.sourceTimestampField = tableremap[2]
                self.targetTimestampField = tableremap[2]
                sourceTableName = tableremap[0]
                targetTableName = tableremap[1]
            elif len(tableremap) == 2:
                self.sourceTimestampField = tableremap[1]
                self.targetTimestampField = tableremap[1]
                sourceTableName = targetTableName = tableremap[0]
            elif len(tableremap) == 1:
                sourceTableName = targetTableName = tableremap[0]
            else:
                print("tablelist error in the configuration")
                sys.exit()
            self.sourceTable = DbTable(self.sourceCursor, self.sourceSchema, sourceTableName, self.sourceTimestampField)
            self.targetTable = DbTable(self.targetCursor, self.targetSchema, targetTableName, self.targetTimestampField)
            self.synctable(self.sourceDb, self.targetDb, self.sourceTable, self.targetTable)

def usage():
    print(
    """
    Usage: dataplus [option]

    -h or --help: 显示帮助信息
                  Show this help message and exit

    -c or --config: 指定配置文件并执行同步 例如：dataplus -c "config.ini"
                    Specify the configuration file and start data synchronization. For example: dataplus -c "config.ini"

    -v or --version: 显示版本
                     Show version
    """
    )

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:v", ["help", "output="])
        if len(opts) == 0 and len(args) == 1:
            configfile = args[0]
            app = sync(configfile)
            app.start()
        for cmd, arg in opts:
            if cmd in ("-h", "--help"):
                usage()
                sys.exit()
            elif cmd in ("-c", "--config"):
                configfile = arg
                app = sync(configfile)
                app.start()
            elif cmd in ("-v", "--version"):
                print("dataplus version 0.1.2")
    except getopt.GetoptError as err:
        print(err, "argv error, please input")
