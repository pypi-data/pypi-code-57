import pickle
from typing import Any, Dict, List

from datatosk.sources.source import Source, SourceParam, SourceRead


# pylint: disable = abstract-method
class PickleRead(SourceRead):
    """Interface element for retrieving data from pickle files.

    Attributes:
        filepath: pickle file path
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

        with open(self.filepath, "rb") as file:
            self.obj = pickle.load(file)

    def __call__(self) -> object:
        """Default PickleSource().read() implementation."""
        return self.obj

    def to_dict(self) -> Dict[Any, Any]:
        if isinstance(self.obj, dict):
            return self.obj
        try:
            return dict(self.obj)
        except (ValueError, TypeError):
            raise ValueError("This object cannot be changed to dict.")


class PickleSource(Source):
    """Pickle files interface, it enables retrieving data from it.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `PICKLE_FILEPATH_[SOURCE_NAME]`
        filepath: pickle file path

    Examples:
        >>> import datatosk
        >>> source = datatosk.pickle(filepath="cool_file.pickle")
        >>> source.read()
        <cool object>

        >>> import datatosk
        >>> source = datatosk.pickle(filepath="cool_file.pickle")
        >>> source.read.to_dict()
        {"pickle": "tasty"}
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)

        self.filepath = self.init_params["PICKLE_FILEPATH"]

    @property
    def params(self) -> List[SourceParam]:
        return [SourceParam(env_name="PICKLE_FILEPATH")]

    @property
    def read(self) -> PickleRead:
        """Interface element for retrieving data from pickle file.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return PickleRead(self.filepath)

    def write(self) -> None:
        """Not implemented yet"""
        raise NotImplementedError
