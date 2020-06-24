from typing import List, Optional, Mapping, Any, Iterable
from stringanalysis.stringanalysis import stringanalysisdict as rawstringanalysisdict  # type: ignore


class StringAnalysisDict:
    def get_fuzzy_vectorized(self, keys: List[Optional[str]], distance: int):
        pass

    def insert_keys_and_values(self, keys: List[str], values: List[Any]):
        pass

    def insert(self, key: str, value: Any):
        pass

    def keys(self) -> List[str]:
        pass

    def get(self, key: str) -> Any:
        pass

    def finalize(self):
        pass

    def get_by_any_prefix_vectorized(self, prefix: List[List[Optional[str]]], length_diff: int, min_length: int = 0):
        pass

    def get_by_any_superstring_vectorized(self, superstring: List[List[Optional[str]]], min_length: int = 0):
        pass


def stringanalysisdict(**kwargs: Any) -> StringAnalysisDict:
    d = rawstringanalysisdict()
    for k, v in kwargs.items():
        d.insert(k, v)
    return d


class StringAnalysisDefaultDict:
    def __init__(self, default, **kwargs):
        self.dict = stringanalysisdict(**kwargs)
        self.default = default

    def get(self, k):
        out = self.dict.get(k)
        if out is None:
            out = self.default()
            self.dict.insert(k, out)
        return out

    def get_by_prefix(self, key, length_diff):
        return self.dict.get_by_prefix(key, length_diff)

    def get_by_superstring(self, key):
        return self.dict.get_by_superstring(key)

    def insert(self, k, v):
        self.dict.insert(k, v)

    def keys(self):
        return self.dict.keys()


def stringanalysisdefaultdict(default, **kwargs):
    return StringAnalysisDefaultDict(default, **kwargs)
