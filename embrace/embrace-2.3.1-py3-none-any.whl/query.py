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

from itertools import chain
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Sequence
from typing import Tuple
import sys

from .parsing import BindParams, compile_bind_parameters
from . import exceptions


known_styles: Dict[type, str] = {}


def get_param_style(conn: Any) -> str:

    conncls = conn.__class__
    try:
        return known_styles[conncls]
    except KeyError:
        modname = conncls.__module__
        while modname:
            try:
                style = sys.modules[modname].paramstyle  # type: ignore
                known_styles[conncls] = style
                return style
            except AttributeError:
                if "." in modname:
                    modname = modname.rsplit(".", 1)[0]
                else:
                    break
    raise TypeError(f"Can't find paramstyle for connection {conn!r}")


class Query:

    name: str
    metadata: Mapping
    sql: str
    source: str

    def __init__(self, name, metadata, statements, source):
        self.name = name
        self.metadata = metadata
        self.statements = statements
        self.source = source
        self._conn = None

    def prepare(self, paramstyle, kw: Mapping) -> List[Tuple[str, BindParams]]:
        return [
            compile_bind_parameters(paramstyle, s, kw) for s in self.statements
        ]

    def bind(self, conn) -> "Query":
        """
        Return a copy of the query bound to a database connection
        """
        cls = self.__class__
        bound = cls.__new__(cls)
        bound.__dict__ = self.__dict__.copy()
        bound._conn = conn
        return bound

    def one(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="one", **kwargs)

    def first(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="first", **kwargs)

    def one_or_none(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="one_or_none", **kwargs)

    def many(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="many", **kwargs)

    def scalar(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="scalar", **kwargs)

    def affected(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="affected", **kwargs)

    def column(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="column", **kwargs)

    def cursor(self, conn=None, *, debug=False, **kwargs):
        return self(conn, debug=debug, _result="cursor", **kwargs)

    def __call__(self, conn=None, *, debug=False, _result=None, **kw):
        if conn is None:
            conn = self._conn
            if conn is None:
                raise TypeError(
                    "Query must be called with a connection argument"
                )
        rt = _result or self.metadata["result"]

        paramstyle = get_param_style(conn)
        cursor = conn.cursor()

        for sqltext, bind_params in self.prepare(paramstyle, kw):
            if debug:
                import textwrap

                print(
                    f"Executing \n{textwrap.indent(sqltext, '    ')} with {bind_params!r}",
                    file=sys.stderr,
                )
            try:
                cursor.execute(sqltext, bind_params)
            except BaseException:
                _handle_exception(conn)

        if rt == "one":
            row = cursor.fetchone()
            if row is None:
                raise exceptions.NoResultFound()
            if cursor.fetchone() is not None:
                raise exceptions.MultipleResultsFound()
            return row

        if rt == "first":
            return cursor.fetchone()

        if rt == "many":
            return iter(cursor.fetchone, None)

        if rt == "one_or_none":
            row = cursor.fetchone()
            if cursor.fetchone() is not None:
                raise exceptions.MultipleResultsFound()
            return row

        if rt == "scalar":
            result = cursor.fetchone()
            if result is None:
                raise exceptions.NoResultFound()
            if isinstance(result, Mapping):
                return next(iter(result.values()))
            elif isinstance(result, Sequence):
                return result[0]
            raise TypeError(
                f"Can't find first column for row of type {type(row)}"
            )

        if rt == "column":
            first = cursor.fetchone()
            if first:
                if isinstance(first, Mapping):
                    key = next(iter(first))
                elif isinstance(first, Sequence):
                    key = 0
                else:
                    raise TypeError(
                        f"Can't find first column for row of type {type(row)}"
                    )

                return (
                    row[key]
                    for row in chain([first], iter(cursor.fetchone, None))
                )
            return iter([])

        if rt == "affected":
            return cursor.rowcount

        if rt == "cursor":
            return cursor

        raise ValueError(f"Unsupported result type: {rt}")


def _handle_exception(conn):
    """
    We have an exception of unknown type, probably raised
    from the dbapi module
    """
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_type and exc_value:
        classes = [exc_type]
        while classes:
            cls = classes.pop()
            clsname = cls.__name__

            if clsname in exceptions.pep_249_exception_names:
                newexc = exceptions.pep_249_exception_names[clsname]()
                newexc.args = getattr(exc_value, "args", tuple())
                raise newexc.with_traceback(exc_tb) from exc_value
            classes.extend(getattr(cls, "__bases__", []))

        raise exc_value.with_traceback(exc_tb)
