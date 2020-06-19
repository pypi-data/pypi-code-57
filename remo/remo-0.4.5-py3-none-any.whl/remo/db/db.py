from remo_app.remo.db import is_sqlite_db, get_db_name

conn = None

if is_sqlite_db():
    db_name = get_db_name()
    if db_name:
        # from playhouse.apsw_ext import APSWDatabase
        # conn = APSWDatabase(db_name)

        from playhouse.sqlite_ext import SqliteExtDatabase

        conn = SqliteExtDatabase(db_name)
        print('Set peewee connection to SQLite')
