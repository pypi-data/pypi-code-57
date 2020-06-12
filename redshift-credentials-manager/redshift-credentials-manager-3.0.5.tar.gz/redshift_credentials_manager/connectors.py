def connect_sql_alchemy(search_path=None, **options):
    if not options:
        return lambda **opts: connect_sql_alchemy(search_path, **opts)
    database = options.pop("dbname")
    username = options.pop("user")
    import sqlalchemy as db
    from sqlalchemy.engine.url import URL
    url = URL(drivername="postgresql", database=database,
              username=username, **options)
    # ssl is required for connecting to redshift
    connect_args = {'options': f"-c search_path={','.join(search_path)}",
                    'sslmode': "require"}
    return db.create_engine(url, connect_args=connect_args)
