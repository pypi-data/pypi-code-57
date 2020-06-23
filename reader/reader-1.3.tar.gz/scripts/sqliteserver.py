"""
In which we use multiprocessing managers and proxies
to run queries on multiple remote SQLite connections
to the same or different databases.

The additions to 07-manager-db-more-magic.py come from multiple iterations,
but since the file was getting big I merged them in a single version.

* connect() allows connecting to more than one database per server.
* Remote calls when iterating over a cursor are batched (see BatchNextMixin).
* executemany() works with generators (see BatchExecuteManyMixin).
* There are some benchmarks.


Some notes on how the multiprocessing manager works
---------------------------------------------------

The manager has 2 modes of operation, server and client.

For server, it needs to be used within .start()/.shutdown() calls,
or as a context manager, or by calling .serve_forever() (blocking).

For client, .connect() must be called first, which just pings the server
once to see if it's alive, with no connection maintained after that.

Each new proxy object creates a new separate connection; because of this,
there can't be a client-side disconnect()/shotdown() manager method.

The connection closes itself when the proxy gets garbage collected,
which in turn deletes the shared object on the server;
https://docs.python.org/3/library/multiprocessing.html#cleanup

It may be possible to close the proxy's connection explicitly by calling
proxy._close(), but it is undocumented/private;
https://github.com/python/cpython/blob/3.8/Lib/multiprocessing/managers.py#L871

This may be needed if the garbage collection delay is not acceptable
(on PyPy objects are not freed instantly when they are no longer reachable).

Unrelated note: The proxy connections are created lazily on the first
method call, one per thread. Each connection has a corresponding
worker thread in the server.

"""
import os
import sys
import time
from multiprocessing.managers import BaseManager, MakeProxyType
from threading import Thread
import threading
import sqlite3
import collections
import itertools


def log(*args):
    # join before printing to avoid overlapping lines
    print(' '.join(map(str, args)) + '\n', end='')


ADDR = ('127.0.0.1', 5000)
PATH = '/tmp/s3c.sqlite'


_ConnectionProxyBase = MakeProxyType(
    '_ConnectionProxyBase',
    (
        'close',
        'commit',
        'create_function',
        # TODO: cursor(factory=...) may not work
        'cursor',
        'execute',
        'executemany',
        'rollback',
    )
)

class ConnectionProxyBase(_ConnectionProxyBase):

    # allows us to not implement getter and setter methods on the Connection object
    _exposed_ = _ConnectionProxyBase._exposed_ + ('__getattribute__', '__setattr__')

    # NOTE: methods that take callables only work with picklable callables

    _method_to_typeid_ = {
        'cursor': 'Cursor',
        'execute': 'Cursor',
        'executemany': 'Cursor',
    }

    def __enter__(self):
        # __enter__ is a noop in the original implementation
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # can't _callmethod('__exit__') because exc_tb is not picklable
        if exc_val:
            self.rollback()
        else:
            self.commit()

    @property
    def in_transaction(self):
        return self._callmethod('__getattribute__', ('in_transaction',))

    @property
    def isolation_level(self):
        return self._callmethod('__getattribute__', ('isolation_level',))

    @isolation_level.setter
    def isolation_level(self, value):
        return self._callmethod('__setattr__', ('isolation_level', value))


_CursorProxyBase = MakeProxyType(
    '_CursorProxyBase',
    (
        '__next__',
        'close',
        'execute',
        'executemany',
        'fetchall',
        'fetchmany',
        'fetchone',
    )
)

class CursorProxyBase(_CursorProxyBase):

    _exposed_ = _CursorProxyBase._exposed_ + ('__getattribute__',)

    _method_to_typeid_ = {
        'execute': 'Cursor',
        'executemany': 'Cursor',
    }

    def __iter__(self):
        return self

    # If we don't override execute(many), they will return a new proxy
    # to the same cursor instead of the same proxy. The new proxy
    # may create an additional connection, but that doesn't seem to show up
    # in the simple timemarks we run on localhost.
    #
    # The new proxy may be an issue if the cursor proxy has client-side state
    # (see RowCountMixin).

    def execute(self, *args, **kwargs):
        super().execute(*args, **kwargs)
        return self

    def executemany(self, *args, **kwargs):
        super().executemany(*args, **kwargs)
        return self

    @property
    def rowcount(self):
        return self._callmethod('__getattribute__', ('rowcount',))


class BatchNextMixin:

    """__next__() cursor proxy implementation that retrieves rows in batches.

    The using class must have a _batch_size defined.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._array = None
        self._index = None

    def __next__(self):
        # makes things 3-4 times faster for 100 noop rows,
        # 33 times faster for 10000 noop rows
        if self._array is None:
            self._array = self.fetchmany(self._batch_size)
            self._index = 0

        if not self._index < len(self._array):
            if len(self._array) < self._batch_size:
                raise StopIteration
            self._array = self.fetchmany(self._batch_size)
            self._index = 0

        if not self._array:
            raise StopIteration

        rv = self._array[self._index]
        self._index += 1
        return rv


class BatchExecuteManyMixin:

    """executemany() implementation that supports generators.

    The using class must have a _batch_size defined.

    Compatible with both ConnectionProxy and CursorProxy.
    Requires a CursorProxy that has a _rowcount attribute (see RowCountMixin).

    """

    def executemany(self, operation, param_sets):
        # only pay the chunking price for iterables of unkwown length
        # (otherwise for a 10k element param_sets list it takes 3-4x as much time)
        if isinstance(param_sets, collections.abc.Sequence):
            all_chunks = [param_sets]
        else:
            all_chunks = chunks(self._batch_size, param_sets)

        try:
            cursor = self
            for i, chunk in enumerate(all_chunks):
                chunk = list(chunk)
                cursor = super(BatchExecuteManyMixin, cursor).executemany(operation, chunk)

                # only pay for the extra rowcount call if we have more than one chunk;
                # a custom Connection could send both the cursor and the rowcount in a single roundrip, but this is simpler
                if i != 0 or len(chunk) >= self._batch_size:
                    last_rowcount = super(RowCountMixin, cursor).rowcount
                    cursor._rowcount = (cursor._rowcount or 0) + last_rowcount

        except Exception:
            if hasattr(cursor, '_rowcount'):
                cursor._rowcount = -1
            raise

        return cursor


def chunks(n, iterable):
    """chunks(2, 'ABCDE') --> AB CD E"""
    # based on https://stackoverflow.com/a/8991553
    # copy-pasted from reader._utils
    it = iter(iterable)
    while True:
        chunk = itertools.islice(it, n)
        try:
            first = next(chunk)
        except StopIteration:
            break
        yield itertools.chain([first], chunk)


class RowCountMixin:

    """Allow overriding .rowcount on a CursorProxy."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rowcount = None

    @property
    def rowcount(self):
        if self._rowcount is not None:
            return self._rowcount
        return super().rowcount

    def execute(self, *args, **kwargs):
        self._rowcount = None
        return super().execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        self._rowcount = None
        return super().executemany(*args, **kwargs)


class ConnectionProxy(BatchExecuteManyMixin, ConnectionProxyBase):

    _batch_size = 256


class CursorProxy(RowCountMixin, BatchExecuteManyMixin, BatchNextMixin, CursorProxyBase):

    connection_cls = ConnectionProxy

    @property
    def _batch_size(self):
        return self.connection_cls._batch_size


def make_manager_cls(bases=(BaseManager,)):

    def make_connection(*args, **kwargs):
        return sqlite3.connect(*args, check_same_thread=False, **kwargs)

    Manager = type('Manager', bases, {})
    Manager.register('Connection', make_connection, proxytype=ConnectionProxy)
    Manager.register('Cursor', proxytype=CursorProxy, create_method=False)
    return Manager


def connect(address, authkey, *args, manager_bases=(BaseManager,), **kwargs):
    manager = make_manager_cls(bases=manager_bases)(address, authkey)
    manager.connect()
    return manager.Connection(*args, **kwargs)


def client_one(connect, *args):
    log(f"client one: pid {os.getpid()}, ident {threading.get_ident()}")

    db = connect(*args)

    db.execute("create table if not exists t(a)")
    log("client one: created table")

    time.sleep(1)

    cursor = db.execute("select * from t")
    log(f"client one: cursor.rowcount, list(cursor): {cursor.rowcount}, {list(cursor)}")

    db.create_function('pymax', 2, max)
    log(f"client one: pymax: {list(db.execute('select pymax(1, 2)'))}")

    db.close()
    try:
        db.execute("select 1")
        assert False, "expected exception"
    except Exception as e:
        log(f"client one: select 1: error: {type(e).__name__}: {e}")


def client_two(connect, *args):
    log(f"client two: pid {os.getpid()}, ident {threading.get_ident()}")

    db = connect(*args)

    time.sleep(.1)
    with db as db_enter:
        log(f"client two: db is db.__enter__(): {db is db_enter}")
        cursor = db.cursor()
        execute_cursor = cursor.execute("insert into t values (0), (1), (2)")
        log(f"client two: db.cursor() is cursor.execute(): {cursor is execute_cursor}")
        log(f"client two: db.cursor().rowcount, cursor.execute().rowcount: {cursor.rowcount}, {execute_cursor.rowcount}")

    with db:
        cursor = db.executemany("insert into t values (?)", [(3,)])
        log(f"client two: db.executemany().rowcount #1 {cursor.rowcount}")
        cursor = db.executemany("insert into t values (?)", ((i,) for i in (4, 5, 6)))
        log(f"client two: db.executemany().rowcount #2 {cursor.rowcount}")

        cursor = db.cursor()
        cursor.executemany("insert into t values (?)", [(7,), (8,), (9,)])
        log(f"client two: db.cursor().executemany().rowcount #1 {cursor.rowcount}")
        cursor.executemany("insert into t values (?)", ((i,) for i in (10, 11, 12, 13)))
        log(f"client two: db.cursor().executemany().rowcount #2 {cursor.rowcount}")
        list(cursor.execute("select 1;"))
        log(f"client two: db.cursor().execute().rowcount for select {cursor.rowcount}")

    try:
        with db:
            cursor = db.cursor()
            cursor.executemany(
                "insert into t values (?)",
                [(i,) for i in range(300)]
            )
            rowcount = cursor.rowcount
            cursor.executemany(
                "insert into t values (?)",
                map(lambda i: (1/i,), range(300, -1, -1))
            )
    except ZeroDivisionError:
            pass
    log(f"client two: executemany().rowcount exception: {rowcount}, {cursor.rowcount}")

    log(f"client two: db.isolation_level: {db.isolation_level}")
    db.isolation_level = 'IMMEDIATE'
    log(f"client two: db.isolation_level: {db.isolation_level}")
    db.isolation_level = ''
    log(f"client two: db.isolation_level: {db.isolation_level}")

    try:
        log(f"client two: db.in_transaction before with: {db.in_transaction}")
        with db:
            db.execute("insert into t values (3), (4)")
            log(f"client two: db.in_transaction inside with: {db.in_transaction}")
            1/0
    except ZeroDivisionError:
        pass


def clean_up_db():
    try:
        os.remove(PATH)
    except FileNotFoundError:
        pass


# --- basic test

def main_test():
    ConnectionProxy._batch_size = 2

    clean_up_db()
    manager = make_manager_cls()(ADDR, b'')
    with manager:
        one = Thread(target=client_one, args=(connect, ADDR, b'', PATH))
        two = Thread(target=client_two, args=(connect, ADDR, b'', PATH))
        one.start()
        two.start()
        one.join()
        two.join()
        log()

    clean_up_db()
    one = Thread(target=client_one, args=(sqlite3.connect, PATH))
    two = Thread(target=client_two, args=(sqlite3.connect, PATH))
    one.start()
    two.start()
    one.join()
    two.join()
    log()


# --- benchmark

import timeit
from multiprocessing.managers import SyncManager

# label, bases, stmt, direct_setup, remote_setup
TIME_DATA = [
    (
        "len(l)",
        (SyncManager,),
        "len(l)",
        "l = list()",
        "manager = make_manager_cls(bases)(ADDR, b'')\n"
        "manager.connect()\n"
        "l = manager.list()\n",
    ),
    (
        "select literal",
        (BaseManager,),
        "list(db.execute('select 1, 2'))",
        "db = sqlite3.connect(PATH)",
        "db = connect(ADDR, b'', PATH)",
    ),
    (
        "select literal reuse cursor",
        (BaseManager,),
        "list(cursor.execute('select 1, 2'))",
        "db = sqlite3.connect(PATH)\ncursor = db.cursor()",
        "db = connect(ADDR, b'', PATH)\ncursor = db.cursor()",
    ),
    (
        "select 1M blob",
        (BaseManager,),
        "list(db.execute('select randomblob(1024*1024)'))",
        "db = sqlite3.connect(PATH)",
        "db = connect(ADDR, b'', PATH)",
    ),
    (
        "select from 10k row table",
        (BaseManager,),
        "list(db.execute('select * from t where a >= 80 and b < 190'))",
        "db = sqlite3.connect(PATH)\n"
        "db.execute('create table t(a, b)')\n"
        "with db:\n"
        "    db.executemany('insert into t values (?, ?)', [(i, i*2) for i in range(10000)])\n",
        "db = connect(ADDR, b'', PATH)\n"
        "db.execute('create table t(a, b)')\n"
        "with db:\n"
        "    db.executemany('insert into t values (?, ?)', [(i, i*2) for i in range(10000)])\n",
    ),
    (
        "select 100 rows",
        (BaseManager,),
        """list(db.execute('''
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt
                LIMIT 100
            )
            SELECT x FROM cnt;
        '''))""",
        "db = sqlite3.connect(PATH)",
        "db = connect(ADDR, b'', PATH)",
    ),
    (
        "select 10000 rows",
        (BaseManager,),
        """list(db.execute('''
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt
                LIMIT 10000
            )
            SELECT x FROM cnt;
        '''))""",
        "db = sqlite3.connect(PATH)",
        "db = connect(ADDR, b'', PATH)",
    ),
    (
        "select 100 custom func rows",
        (BaseManager,),
        """list(db.execute('''
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt
                LIMIT 100
            )
            SELECT pow(x, 2) FROM cnt;
        '''))""",
        "db = sqlite3.connect(PATH)\n"
        "db.create_function('pow', 2, pow)\n",
        "db = connect(ADDR, b'', PATH)\n"
        "db.create_function('pow', 2, pow)\n",
    ),
    (
        "simple insert",
        (BaseManager,),
        "with db:\n"
        "    db.execute('insert into t values (1, 2)')\n",
        "db = sqlite3.connect(PATH)\n"
        "db.execute('create table t(a, b)')\n",
        "db = connect(ADDR, b'', PATH)\n"
        "db.execute('create table t(a, b)')\n",
    ),
    (
        "insert 100 rows",
        (BaseManager,),
        "with db:\n"
        "    db.executemany('insert into t values (?, ?)', [(i, i*2) for i in range(100)])\n",
        "db = sqlite3.connect(PATH)\n"
        "db.execute('create table t(a, b)')\n",
        "db = connect(ADDR, b'', PATH)\n"
        "db.execute('create table t(a, b)')\n",
    ),
    (
        "insert 10000 rows",
        (BaseManager,),
        "with db:\n"
        "    db.executemany('insert into t values (?, ?)', [(i, i*2) for i in range(10000)])\n",
        "db = sqlite3.connect(PATH)\n"
        "db.execute('create table t(a, b)')\n",
        "db = connect(ADDR, b'', PATH)\n"
        "db.execute('create table t(a, b)')\n",
    ),
]

TIME_ADDRESSES = {
    # AF_UNIX seems 50% faster than AF_INET, depending on the query
    'AF_UNIX': 'unix-socket-i-guess',
    'AF_INET': ('127.0.0.1', 5000),
}

def main_time():
    # "Python 3.8 changes the default mode of multiprocessing on MacOS to spawn instead of fork", from
    # https://github.com/huge-success/sanic/issues/1774#issuecomment-579182577
    # 
    # TODO: To get this to work with any context other than fork,
    # Manager should be importable.
    import multiprocessing
    fork_context = multiprocessing.get_context('fork')

    for family, ADDR in TIME_ADDRESSES.items():

        for label, bases, stmt, direct_setup, remote_setup in TIME_DATA:
            clean_up_db()
            direct = timeit.timeit(stmt, direct_setup, globals=globals(), number=100)

            clean_up_db()
            with make_manager_cls(bases=bases)(ADDR, b'', ctx=fork_context):
                vars = dict(globals())
                vars.update(locals())
                remote = timeit.timeit(stmt, remote_setup, globals=vars, number=100)

            log(f"{family:<7} {label:<39} {remote/direct:>9.2f}")


# --- main

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        main_test()
    if sys.argv[1] == 'time':
        main_time()
