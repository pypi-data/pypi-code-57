from typing import List

import pandas as pd  # type: ignore
import sqlalchemy

from datatosk import types
from datatosk.sources.source import Source, SourceParam, SourceRead


class MySQLRead(SourceRead):
    """Interface element for retrieving data from MySQL database.

        Attributes:
            engine: SQLAlchemy engine
        """

    def __init__(self, engine: sqlalchemy.engine.Engine) -> None:
        self.engine = engine

    def __call__(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> pd.DataFrame:
        """Default MySQLSource().read() implementation."""
        return self.to_pandas(query=query, params=params, **kwargs)

    def to_pandas(
        self,
        query: str = "",
        params: types.ParamsType = None,
        **kwargs: types.KwargsType,
    ) -> pd.DataFrame:
        return pd.read_sql(query, con=self.engine, params=params, **kwargs)

    def to_list(
        self, query: str = "", params: types.ParamsType = None
    ) -> types.ListOutputType:

        with self.engine.connect() as connection:

            if params is None:
                result = connection.execute(query)
            else:
                result = connection.execute(query, params)

            return [
                item[0] if len(item) == 1 else list(item) for item in result.fetchall()
            ]

    def to_dict(
        self, query: str = "", params: types.ParamsType = None,
    ) -> types.DictOutputType:
        with self.engine.connect() as connection:

            if params is None:
                result = connection.execute(query)
            else:
                result = connection.execute(query, params)

            columns = [column[0] for column in result.keys()]

            return [dict(zip(columns, row)) for row in result.fetchall()]


class MySQLSource(Source):
    """MySQL database interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `MYSQL_USER_[SOURCE_NAME]`
            - `MYSQL_PASS_[SOURCE_NAME]`
            - `MYSQL_HOST_[SOURCE_NAME]`
            - `MYSQL_PORT_[SOURCE_NAME]`
            - `MYSQL_DB_[SOURCE_NAME]`
        engine: SQLAlchemy engine


    Examples:
        >>> import datatosk
        >>> source = datatosk.mysql(source_name="dope_db")
        >>> source.read("SELECT * FROM dope_table")
           dope_column  other_dope_column
        0            1                  3
        1            2                  4

        >>> import datatosk
        >>> source = datatosk.mysql(source_name="dope_db")
        >>> source.read.to_list("SELECT SUM(*) FROM dope_table")
        [3, 7]

        >>> import datatosk
        >>> source = datatosk.mysql(source_name="dope_db")
        >>> source.read.to_dict("SELECT * FROM dope_table")
        [{dope_column: 1, other_dope_column:3}]
        [{dope_column: 2, other_dope_column:4}]
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)

        self.engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{self.init_params['MYSQL_USER']}:"
            f"{self.init_params['MYSQL_PASS']}@"
            f"{self.init_params['MYSQL_HOST']}:"
            f"{self.init_params['MYSQL_PORT']}/"
            f"{self.init_params['MYSQL_DB']}"
            "?charset=utf8mb4",
            pool_recycle=3600,
        )

    @property
    def params(self) -> List[SourceParam]:
        return [
            SourceParam(env_name="MYSQL_USER"),
            SourceParam(env_name="MYSQL_DB"),
            SourceParam(env_name="MYSQL_PASS", is_required=False, default="",),
            SourceParam(env_name="MYSQL_HOST", is_required=False, default="localhost",),
            SourceParam(env_name="MYSQL_PORT", is_required=False, default="3306",),
        ]

    @property
    def read(self) -> MySQLRead:
        """Interface element for retrieving data from MySQL database.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return MySQLRead(self.engine)

    def write(self) -> None:
        """Not implemented yet"""
        raise NotImplementedError
