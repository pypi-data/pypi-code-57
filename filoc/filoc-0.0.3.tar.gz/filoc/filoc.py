import itertools
import os
import re
from typing import List, Set, Dict, Tuple

import fsspec
import parse
from fsspec import AbstractFileSystem


def add_filename_suffix(path, suffix):
    root, ext = os.path.splitext(path)
    fname = os.path.basename(root)
    candidate = "{}_{}{}".format(fname, suffix, ext)
    return candidate


def find_first_free_backup_path(fs : AbstractFileSystem, path):
    dirname = os.path.dirname(path)
    ls  = set(fs.listdir(dirname))
    for i in itertools.count(1):
        candidate = add_filename_suffix(path, i)
        if candidate in ls:
            return candidate


def sort_natural(li: List[str]) -> List[str]:
    # todo: improve
    return sorted(li, key=lambda s: [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", s)])


class Filoc:
    def __init__(self, path_fmt : str) -> None:
        super().__init__()
        opened_file          = fsspec.open(path_fmt)
        self.fs              = opened_file.fs           # type: AbstractFileSystem
        self.path_fmt        = path_fmt                 # type: str
        self.path_parser     = parse.compile(path_fmt)  # type: parse.Parser
        # noinspection PyProtectedMember
        self.path_properties = set(self.path_parser._named_fields)  # type: Set[str]

    def build_path(self, **properties) -> str:
        undefined_keys = self.path_properties - set(properties)
        if len(undefined_keys) > 0:
            raise ValueError('Undefined properties: {}'.format(undefined_keys))
        return self.path_fmt.format(**properties)

    def build_glob_path(self, **properties) -> str:
        provided_keys  = set(properties)
        undefined_keys = self.path_properties - provided_keys
        defined_keys   = self.path_properties - undefined_keys

        path_values = {}
        path_values.update({ (k, properties[k]) for k in defined_keys })

        glob_path = self.path_fmt
        for undefined_key in undefined_keys:
            glob_path = re.sub(r'{' + undefined_key + r'(?::[^}]*)}', '*', glob_path)

        # finally format
        glob_path = glob_path.format(**path_values)
        return glob_path

    def extract_properties(self, path : str) -> Dict[str, object]:
        return self.path_parser.parse(path).named

    def find_paths(self, **properties) -> List[str]:
        paths = self.fs.glob(self.build_glob_path(**properties))
        return sort_natural(paths)

    def find_paths_and_properties(self, **properties) -> List[Tuple[str, List[str]]]:
        paths = self.find_paths(**properties)
        return [ (p, self.extract_properties(p)) for p in paths ]
