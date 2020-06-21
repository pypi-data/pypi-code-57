'''
Documentation: 查询操作mysql数据库的。
引用包名是rfApiTestLibrary，引用本python文件，请使用Library  rfApiTestLibrary/mysqlLib.py。
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   rfApiTestLibrary/keywords/[ ../keywords/sc/mysql.html | mysql.robot ],
文档在[ ../keywords/mysql.doc.html | 这里 ]。
'''

import pymysql
import rfApiTestLibrary.log as logger

def _at_get_mysql_connection_with_config(config):
    '''
    通过标准配置连接数据库。底层方法。
   【config】: 字典类型，含有host,port,user,password,db等信息的配置.方法加了默认配置是charset=utf8
    RETURN: Connection类型

    Examples:
        |   方法                              |          参数                                                                                            |
        | at get mysql connection with config | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |                                    |
    '''
    try:
        logger.info("数据库连接" + str(config))
        if config.get("charset") is None:
            config['charset']='utf8'
        connection = pymysql.connect(**config)
        return connection
    except pymysql.OperationalError as e:
        logger.error('连接数据库失败，原因：%s' % e)
        raise AssertionError(e)
    except pymysql.MySQLError as e:
        logger.error('连接数据库失败，原因：%s' % e)
        raise AssertionError('连接数据库失败，原因：%s' % e)

def _at_execute_sql(conn,sql):
    '''
    操作数据库数据。
   【conn】:Connection类型，数据库连接,
   【sql】: String类型，执行的sql,
    RETURN: Int类型，影响数据库数据行数.

    Examples:
        | 方法            |      参数      |  参数 |
        | at execute sql |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        logger.info("被影响的行数: "+ str(count), html=True, also_console=True)
        conn.commit()  # 提交事务
        return count
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: "+e)
        raise AssertionError("数据库错误: "+e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def _at_query(conn,sql):
    '''
    查询所有数据。返回嵌套字典的列表。
   【conn】:Connection类型，数据库连接
   【sql】: String类型，执行的sql
    RETURN: 列表，列表里嵌套字典

    Examples:
        |    方法     |      参数     |  参数  |
        | at query   |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        # 取出所有行
        result = cursor.fetchall()
        fields_list=[]
        for field in cursor.description:
            #field[0]是field名字，如果使用别名，就是别名
            fields_list.append(field[0])
        conn.commit()  # 提交事务
        if result is None or len(result) == 0:
            logger.info("数据库返回结果: None", html=True, also_console=True)
            return None
        result_list=[]
        for i in range(len(result)):
            row_dict={}
            row=result[i]
            for j in range(len(row)):
                row_dict[fields_list[j]]=row[j]
            result_list.append(row_dict)
        logger.info("数据库返回结果: " + str(result_list), html=True, also_console=True)
        return result_list
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def _at_query_one(conn,sql):
    '''
    查询一条数据。返回字典。
   【conn】:Connection类型，数据库连接
   【sql】: String类型，执行的sql
    RETURN: 字典类型

    Examples:
        |       方法     |      参数     |  参数  |
        | at query one  |  <Connection> | <sql> |
    '''
    cursor = conn.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql, html=True, also_console=True)
        count = cursor.execute(sql)
        # 取出所有行
        result = cursor.fetchone()
        fields_list=[]
        for field in cursor.description:
            #field[0]是field名字，如果使用别名，就是别名
            fields_list.append(field[0])
        conn.commit()  # 提交事务
        result_dict={}
        if result is None or len(result)==0:
            logger.info("数据库返回结果: None", html=True, also_console=True)
            return None
        for index in range(len(result)):
            result_dict[fields_list[index]]=result[index]
        logger.info("数据库返回结果: " + str(result_dict), html=True, also_console=True)
        return result_dict
    except pymysql.MySQLError as e:
        conn.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cursor.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            conn.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def at_execute_sql_with_config(sql,config):
    '''
    通过配置configure，获得数据库连接。然后根据sql操作数据库，返回数据是影响的行数int。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host,port,user,password,db等信息的配置
    RETURN: Int类型，影响的行数。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Execute%20database%20mysql%20data | Execute database mysql data],
    [../keywords/mysql.doc.html#操作数据库mysql数据 | 操作数据库mysql数据],


    Examples:
        |       关键字                | 参数   |  参数                                                                                                     |
        | at execute sql with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_execute_sql(conn, sql)


def at_query_mysql_with_config(sql,config):
    '''
    通过配置configure，获得数据库连接。然后根据sql查询所有数据。返回结果是嵌套字典的列表。
   【sql】: String类型,查询的sql
   【config】: 字典类型,含有host,port,user,password,db等信息的配置
    RETURN: 列表，嵌套字典。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Query%20database%20mysql%20data | Query database mysql data],
    [../keywords/mysql.doc.html#查询数据库mysql数据 | 查询数据库mysql数据],

    Examples:
        |       关键字                | 参数   |  参数                                                                                                     |
        | at query mysql with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_query(conn,sql)

def at_query_one_with_config(sql,config):
    '''
    通过configure配置，获得数据库连接。然后根据sql查询1条数据。返回结果是字典。
   【sql】: String类型,查询的sql。
   【config】: 字典类型,含有host,port,user,password,db等信息的配置。
    RETURN: 字典类型数据。

    目前使用该方法的关键字是:
    [../keywords/mysql.doc.html#Query%20database%20Only%20One%20mysql%20data | Query database only one mysql data],
    [../keywords/mysql.doc.html#查询数据库mysql一条数据 | 查询数据库mysql一条数据],

    Examples:
        |       关键字              | 参数   |  参数                                                                                                     |
        | at query one with config | <sql>  | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |
    '''
    conn = _at_get_mysql_connection_with_config(config)
    return _at_query_one(conn,sql)


def at_call_function(function,config,arguments=None):
    '''
    通过配置configure，获得数据库连接。然后根据function和arguments调用存储过程或者函数
    :param function: 存储过程或者函数名，String类型
    :param arguments: 列表，参数
    :param config: 数据库配置
    :return:
    '''
    conn = _at_get_mysql_connection_with_config(config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if arguments is None:
        return cursor.callproc(function)
    else:
        cursor.callproc(function,tuple(arguments))
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result
