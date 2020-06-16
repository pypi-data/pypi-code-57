from orm_collector import NetworkGroup
from sqlalchemy.schema import CreateTable
from orm_collector.db_session import CollectorSession
from orm_collector.scripts.create_db import get_session

sql = CreateTable(NetworkGroup.__table__)
print(sql, type(sql))
session=get_session("collector",True,{})
session.run_sql(sql)

