def dataframe_insert_to_database(dataframe, connection, table):
    """
    将dataframe写入数据库对应表中
    适用于大量数据导入
    :param connection: 由sqlalchemy.create_engine得到
    """
    dataframe.to_sql(name=table, con=connection, if_exists="append", index=False)
    connection.dispose()


def dataframe_update_to_database(dataframe, connection, table):
    """
    增量数据插入数据库，对于存在的主键进行值的更新
    适用于少量数据
    大量的数据用该方法速度较慢
    """
    query = "REPLACE INTO {table} ({fields}) VALUES ({values});".format(table=table,
                                                                        fields=",".join(dataframe.columns),
                                                                        values=",".join(["%s"]*len(dataframe.columns)))
    for i, row in dataframe.iterrows():
        connection.execute(query, row.values.tolist())
    connection.dispose()