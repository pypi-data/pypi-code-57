from typing import List

import pandas as pd  # type: ignore
import pandas_gbq  # type: ignore

from datatosk import types
from datatosk.sources.source import Source, SourceParam, SourceRead


# pylint: disable = abstract-method
class GBQRead(SourceRead):
    """Interface element for retrieving data from GBQ dataset.

    Attributes:
        project_id: GoogleBigQuery project_id
    """

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def __call__(self, query: str = "", **kwargs: types.KwargsType,) -> pd.DataFrame:
        """Default GBQSource().read() implementation."""
        return self.to_pandas(query=query, **kwargs)

    def to_pandas(self, query: str = "", **kwargs: types.KwargsType) -> pd.DataFrame:
        return pandas_gbq.read_gbq(query=query, project_id=self.project_id, **kwargs)


class GBQSource(Source):
    """GBQ database interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `GBQ_PROJECT_ID_[SOURCE_NAME]`
        project_id: GoogleBigQuery project_id

    Examples:
        >>> import datatosk
        >>> source = datatosk.gbq(source_name="epic_source")
        >>> source.read("SELECT * FROM epic_table")
            superheros        real_name
        0    "Ironman"     "Tony Stark"
        1     "Batman"    "Bruce Wayne"
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)
        self.project_id = self.init_params["GBQ_PROJECT_ID"]

    @property
    def params(self) -> List[SourceParam]:
        return [SourceParam(env_name="GBQ_PROJECT_ID")]

    @property
    def read(self) -> GBQRead:
        """Interface element for retrieving data from GBQ dataset.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return GBQRead(self.project_id)

    def write(self) -> None:
        """Not implemented yet"""
        raise NotImplementedError
