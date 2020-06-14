from .versioner import Versioner


class MemoryVersioner(Versioner):
    def __init__(self, version: str = '') -> None:
        self.version = version

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._version = value
