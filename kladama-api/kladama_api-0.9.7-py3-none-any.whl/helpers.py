import abc
from abc import ABC


class HelperBase(ABC):

    def __init__(self, url_base: str):
        self._url_base = url_base

    @property
    def url_path(self) -> str:
        return self._url_base

    @property
    @abc.abstractmethod
    def obj(self):
        pass


class CheckAoiHelper(HelperBase):

    def __init__(self, aoi_obj):
        HelperBase.__init__(self, '/do/check/aoi')
        self._aoi_obj = aoi_obj

    @property
    def aoi_obj(self):
        return self._aoi_obj

    @property
    def obj(self):
        return self.aoi_obj
