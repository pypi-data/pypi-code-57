# coding:utf-8
import threading
import sys
import time
from CDBUtils.ValidatedPooledDB import PooledDB
# from DBUtils.PooledDB import PooledDB
from threading import Thread, Timer
import cx_Oracle


# TNS = cx_Oracle.makedsn("127.0.0.1", '1521',"orcl")
# TNS = 127.0.0.1:1521/orcl
TNS = "RC_50.67ORCL"

pool = PooledDB(cx_Oracle,
                user="e_channel",
                password="gN6Qrmjf7#R9G",
                dsn=TNS,
                mincached=5,
                maxcached=20,
                blocking=True,
                test_idle=True,
                maxconnections=50,
                idle_check_time=30
                )


def test_fun(conn, sql, params=[]):
    try:
        cus = conn.cursor()
        # print("testTimeout-sql"+sql)
        print("testTimeout222-params=%s,现在的连接数=%s" % (str(params), pool._connections))
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


sql = "select username,count(username) as u_size from v$session where PROGRAM='python.exe' and username is not null  group by username"
params = []


def run_with_timeout(time_out=1, connection=None):
    c = Dispacher(test_fun, conn=connection, sql=sql, params=params)
    c.join(time_out)
    if c.isAlive():
        c.stop()
        print("testTimeout-%s 现在的连接数%s" % (threading.currentThread().getName(),  pool._connections))
        connection.cancel()
        time.sleep(1)
        return "TimeOutError"
    elif c.error:
        return c.error[1]
    t = c.result
    return t


def start_check():
    connection = pool.connection()
    fun = run_with_timeout(1, connection)
    c_size = pool._connections
    idle_size = len(pool._idle_cache)
    print("testTimeout-返回结果%s" % str(fun))
    r = test_fun(conn=connection, sql=sql, params=params)
    connection.close()
    print("testTimeout-%s-返回%s现在的连接数%s缓存连接%s" %
          (threading.currentThread().getName(), r,c_size , idle_size))


def start_thread():
    for i in range(60):
        Thread(target=start_check).start()
    time.sleep(20)
    print("testTimeout-%s现在的连接数%s_现在缓存的连接数%s" %
          (threading.currentThread().getName(), pool._connections, len(pool._idle_cache)))
    # 20分钟后再次执行
    Timer(20, start_thread).start()


class Dispacher(threading.Thread):
    def __init__(self, fun, *args, **kwargs):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.result = None
        self.error = None
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

        self.start()

    def stop(self):
        try:
            print("testTimeout-into stop")
            self._stop()
        except Exception as e:
            print(e)

    def run(self):
        try:
            self.result = self.fun(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            self.error = sys.exc_info()


if __name__ == '__main__':
    time.sleep(35)
    for i in range(3):
        threading.Thread(target=start_thread).start()
        time.sleep(30)