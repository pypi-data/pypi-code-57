import importlib
import os
from typing import Tuple
from .releases import Types, Commands, Utilities

class _Versioning:
    __slots__ = ('types', 'commands', 'utilities')

    @staticmethod
    def discover(release_: int, build_: int) -> Tuple[int, int]:
        import archicad.releases as RELS
        all_releases = sorted((int(dir_entry.name.lstrip('ac')) for dir_entry in os.scandir(RELS.__path__[0])
            if dir_entry.is_dir() and dir_entry.name.startswith('ac')), reverse=True)
        release = next(x for x in all_releases if x <= release_)

        BUILDS = importlib.import_module(f'archicad.releases.ac{release}')
        all_builds = sorted({int(dir_entry.name.strip('btypescomanduil.')) for dir_entry in os.scandir(BUILDS.__path__[0])
            if dir_entry.is_file() and dir_entry.name.startswith('b')}, reverse=True)
        build = next(x for x in all_builds if x <= build_)
        return release, build

    def __init__(self, release: int, build: int, request):
        assert release >= 24
        self.types = Types
        self.commands = Commands
        self.utilities = Utilities
        self.load(*_Versioning.discover(release, build), request)
    
    def load(self, release: int, build: int, request):
        self.types = importlib.import_module(f'archicad.releases.ac{release}.b{build}types').Types()
        self.commands = importlib.import_module(f'archicad.releases.ac{release}.b{build}commands').Commands(request)
        self.utilities = importlib.import_module(f'archicad.releases.ac{release}.b{build}utilities').Utilities(self.types, self.commands)
