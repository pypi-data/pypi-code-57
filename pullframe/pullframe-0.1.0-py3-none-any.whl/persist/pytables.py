from collections import defaultdict
from contextlib import closing
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from tables import Filters  # type: ignore
from tables import open_file

from pullframe import api
from pullframe.types import CacheFormat


class PyTables(api.Persist):
    def __init__(
        self, directory: Path, complib: str = "blosc", complevel: int = 9
    ):
        super().__init__(directory)
        self.complib = complib
        self.complevel = complevel

    @classmethod
    def on(cls, directory: Path) -> "PyTables":
        return cls(directory)

    def load(
        self,
        name: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        include_start: bool = True,
    ) -> pd.DataFrame:
        with self.__reading_name(name) as h5:
            return _read_from_f(h5, start, end, include_start)

    def save(self, name: str, df: pd.DataFrame) -> None:
        if not self.exists(name):
            return self.write(name, df)

        prev = self.load(name)

        new = prev.reindex(
            index=prev.index.union(df.index),
            columns=prev.columns.union(df.columns),
        )
        new.loc[df.index, df.columns] = df.values
        self.write(name, new)

    def exists(self, name: str) -> bool:
        return self.path(name).exists()

    def last_index(self, name: str) -> datetime:
        with self.__reading_name(name) as h5:
            return _load_index(h5)[-1]

    def update(self, name: str, path: Path) -> None:
        with self.__reading_file(path) as h5:
            append = _read_from_f(h5)

        self.save(name, append)

    @classmethod
    def format(cls):
        return CacheFormat.PYTABLES

    @staticmethod
    def suffix():
        return "h5"

    def write(self, name: str, df: pd.DataFrame) -> None:
        self.dump(self.path(name), df)

    def dump(self, path: Path, df: pd.DataFrame) -> None:
        with self.__writing_file(path) as h5:
            _write_to_f(h5, df)

    def __reading_name(self, name: str):
        return self.__reading_file(self.path(name))

    def __reading_file(self, path: Path):
        return closing(open_file(path, mode="r"))

    def __writing_file(self, path: Path):
        filters = Filters(complib=self.complib, complevel=self.complevel)
        return closing(open_file(path, mode="w", filters=filters))


Index = int


def _read_from_f(
    h5,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    include_start=True,
) -> pd.DataFrame:
    index = _load_index(h5)

    if start is None:
        start_idx: int = 0
    else:
        start_idx = np.searchsorted(index, start)
        if not include_start:
            start_idx = max(0, start_idx + 1)

    if end is None:
        end_idx: int = len(index)  # type: ignore
    else:
        end_idx = np.searchsorted(index, end, side="right")

    all_columns = h5.get_node(h5.root, "all_columns").read()
    dtypes = h5.get_node(h5.root, "dtypes").read()

    df_list = []
    for dtyp in dtypes:
        node = f"/data/{dtyp.decode()}"
        values = h5.get_node(node, "data")[start_idx:end_idx]
        columns = h5.get_node(node, "columns").read()

        if dtyp == b"str":
            values = values.astype("str")
        elif dtyp == b"datetime":
            values = np.vstack(
                [pd.to_datetime(values[:, i]) for i in range(values.shape[1])]
            ).T

        df = pd.DataFrame(
            index=index[start_idx:end_idx], columns=columns, data=values
        )
        df_list.append(df)

    df = pd.concat(df_list, axis=1)[all_columns]

    if df.columns.dtype == "object":
        df.columns = [i.decode() for i in df.columns]
    return df


def _load_index(h5):
    index = h5.get_node(h5.root, "index").read()
    return pd.to_datetime(index)


def _write_to_f(h5, df: pd.DataFrame) -> None:
    dtype_to_col_indexes = _dtype_to_col_indexes(df.dtypes)

    h5.create_array(
        h5.root, "index", df.index.values.astype(np.float64), "index"
    )

    h5.create_array(h5.root, "all_columns", df.columns.tolist(), "all_columns")

    data_grp = h5.create_group(h5.root, "data", "data group")

    h5.create_array(
        h5.root,
        "dtypes",
        [_name(i) for i in dtype_to_col_indexes.keys()],
        "dtypes",
    )

    for dtype, indexes in dtype_to_col_indexes.items():
        data = df.iloc[:, indexes]

        dtype_name = _name(dtype)

        group = h5.create_group(data_grp, dtype_name, f"{dtype_name} group")

        if dtype_name == "str":
            arr = data.values
            arr = arr.astype("U")
        elif dtype_name == "datetime":
            arr = data.values.astype(np.float64)
        else:
            arr = data.values

        h5.create_carray(
            where=group, name="data", obj=arr, title=f"{dtype_name} data"
        )

        h5.create_array(
            group, "columns", data.columns.tolist(), f"{dtype_name} columns"
        )


def _dtype_to_col_indexes(dtypes) -> Dict[np.dtype, List[Index]]:
    result = defaultdict(list)

    for i, dtype in enumerate(dtypes):
        result[dtype].append(i)

    return result


def _name(dtype):
    if dtype.name == "object":
        return "str"
    elif dtype.name == "datetime64[ns]":
        return "datetime"
    else:
        return dtype.name
