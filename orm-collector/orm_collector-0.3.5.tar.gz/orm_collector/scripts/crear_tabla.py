from orm_collector import NetworkGroup
from sqlalchemy.schema import CreateTable
from orm_collector.db_session import CollectorSession
from orm_collector.scripts.create_db import get_session

sql = CreateTable(NetworkGroup.__table__)
print(sql, type(sql))
schema = "COLLECTOR"
dbparams =  dict(dbuser='%s_DBUSER' %schema,
                dbpass='%s_DBPASS' %schema,
                dbname='%s_DBNAME' %schema,
                dbhost='%s_DBHOST' %schema,
                dbport='%s_DBPORT' %schema)    

session=get_session("collector",True,{}, dbparams)
session.run_sql(sql)

