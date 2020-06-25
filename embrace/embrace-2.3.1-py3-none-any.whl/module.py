#  Copyright 2020 Oliver Cope
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pathlib
from itertools import chain
from itertools import count
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import wrapt

from .query import Query
from .exceptions import InvalidStatement
from .parsing import DEFAULT_RESULT_TYPE
from .parsing import split_statements

SQL_FILE_GLOB = "**/*.sql"


class Module:

    reloader: Optional[Callable] = None
    _conn = None
    queries: Dict = {}

    def __init__(self):
        self.queries = {}

    def __getattr__(self, name):
        if self.reloader:
            self.reloader()
            try:
                return reloadable_query_proxy(self, name, self.reloader)
            except KeyError:
                raise AttributeError(name)
        try:
            return self.queries[name]
        except KeyError:
            raise AttributeError(name)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def set_reloader(self, fn):
        self.reloader = fn

    def clear(self):
        self.queries.clear()

    def add_query(self, name, query):
        if name in self.queries:
            raise InvalidStatement(
                f"Can't add query {name!r} in {query.source}: "
                f"{self!r} already has an attribute named {name!r} "
                f"(loaded from {getattr(self, name).source})"
            )
        if self._conn:
            query = query.bind(self._conn)
        self.queries[name] = query

    def add_queries(
        self, qs: Union[Iterable[Tuple[str, Query]], Mapping[str, Query]]
    ):
        if isinstance(qs, Mapping):
            qs = qs.items()
        for name, query in qs:
            self.add_query(name, query)

    def load_dir(self, path: Union[str, pathlib.Path]):
        for p in pathlib.Path(path).glob(SQL_FILE_GLOB):
            self.load_file(p)

        return self

    def load_file(self, path: pathlib.Path):
        queries = list(load_queries(path))
        for query in queries:
            self.add_query(query.name, query)

    def execute(self, conn, sql=None, result="many", **kw):
        if sql is None:
            conn, sql = self._conn, conn
        query = Query(
            name=None,
            metadata={"result": result},
            statements=[sql],
            source="<string>",
        )
        return query(conn, **kw)

    def one(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="one", **kwargs)

    def one_or_none(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="one_or_none", **kwargs)

    def many(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="many", **kwargs)

    def scalar(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="scalar", **kwargs)

    def affected(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="affected", **kwargs)

    def column(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="column", **kwargs)

    def cursor(self, conn, sql=None, **kwargs):
        return self.execute(conn, sql, result="cursor", **kwargs)

    def bind(self, conn) -> "Module":
        """
        Return a copy of the module bound to a database connection
        """
        cls = self.__class__
        bound = cls.__new__(cls)
        bound.__dict__ = {
            "_conn": conn,
            "reloader": self.reloader,
            "queries": {
                name: q.bind(conn) for name, q in self.queries.items()
            },
        }
        return bound

    def transaction(self, conn) -> "Transaction":
        return Transaction(self, conn)

    def savepoint(self, conn) -> "Savepoint":
        return Savepoint(self, conn)


class Transaction:
    def __init__(self, module, conn):
        self.conn = conn
        self.module = module.bind(conn)

    def __enter__(self):
        return self.module

    def __exit__(self, type, value, traceback):
        if type:
            self.conn.rollback()
        else:
            self.conn.commit()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


class Savepoint:

    _seq = count()

    def __init__(self, module, conn):
        self.conn = conn
        self.module = module.bind(conn)
        self.savepoint = f"sp_{next(self._seq)}"
        self._cursor = None

    def __enter__(self):
        self._cursor = self.conn.cursor()
        self._cursor.execute(f"SAVEPOINT {self.savepoint}")
        return self.module

    def __exit__(self, type, value, traceback):
        if self._cursor is not None:
            if type:
                self._cursor.execute(f"ROLLBACK TO SAVEPOINT {self.savepoint}")
            else:
                self._cursor.execute(f"RELEASE SAVEPOINT {self.savepoint}")
            self._cursor.close()


def module(path, auto_reload=False):
    path = pathlib.Path(path)
    module = Module()
    module.load_dir(path)
    if auto_reload:

        def get_all_mtimes(path):
            return chain(
                [path.stat().st_mtime],
                (p.stat().st_mtime for p in path.glob(SQL_FILE_GLOB)),
            )

        module_mtime = [max(get_all_mtimes(path))]

        def reload_module():
            if any(m > module_mtime[0] for m in get_all_mtimes(path)):
                module_mtime[:] = [max(get_all_mtimes(path))]
                module.clear()
                module.load_dir(path)
                return True
            return False

        module.set_reloader(reload_module)
    return module


def load_queries(path: pathlib.Path) -> Iterable[Query]:
    with path.open("r", encoding="UTF-8") as f:
        sql = f.read()
        for ix, (metadata, statements) in enumerate(split_statements(sql)):
            metadata.setdefault("result", DEFAULT_RESULT_TYPE)
            if not metadata.get("name"):
                if ix == 0:
                    metadata["name"] = path.stem
                else:
                    raise InvalidStatement(
                        f"{path!s}: no name specified (eg `-- :name my_query_name`)"
                    )
            if "result" not in metadata:
                raise InvalidStatement(
                    f"{path!s}: no result type specified (eg `-- :result :many`)"
                )
            yield Query(
                metadata["name"], metadata, statements, source=str(path)
            )


def reloadable_query_proxy(module, name, reloader):
    def get_query():
        return module.queries[name]

    class ReloadableQueryProxy(wrapt.ObjectProxy):
        def __call__(self, *args, **kwargs):
            reloader()
            self.__wrapped__ = get_query()
            return self.__wrapped__(*args, **kwargs)

        def bind(self, conn):
            return reloadable_query_proxy(module, name, reloader)

    return ReloadableQueryProxy(get_query())
