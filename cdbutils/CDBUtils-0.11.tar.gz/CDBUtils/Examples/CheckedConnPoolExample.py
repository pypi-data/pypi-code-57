from CDBUtils.ValidatedPooledDB import PooledDB
import cx_Oracle


# TNS = cx_Oracle.makedsn("127.0.0.1", '1521',"orcl")
# TNS = 127.0.0.1:1521/orcl
TNS = "LOCALORCL"


pool = PooledDB(cx_Oracle,
                user="zhangzx",
                password="Pwdasc123",
                dsn=TNS,
                mincached=3,
                maxcached=20,
                blocking=True,
                test_on_borrow=True,
                test_idle = True,
                maxconnections=50,
                max_wait_time=10
                )


def test_fun(sql, params=[]):
    try:
        conn = pool.connection()
        cus = conn.cursor()
        print("test-sql"+sql)
        print("test-params" + str(params), "现在的连接数", pool._connections)
        result_db = cus.execute(sql, params)
        result = result_db.fetchall()
        return_result = list()
        if len(result) > 0:
            key_list = [key[0] for key in result_db.description]
            for value in result:
                return_result.append(dict(zip(key_list, value)))
        return return_result
    except Exception as e:
        raise e
    finally:
        cus.close()


if __name__ == '__main__':
    sql = """select username,count(username) as u_size from v$session where 
    PROGRAM='python.exe' and username is not null  group by username"""
    params = []
    for i in range(10):
        print("test_resut=%s" % test_fun(sql, params))
