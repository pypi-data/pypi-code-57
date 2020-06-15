import os
import json
import unicodedata
from itertools import chain
from typing import List, Dict
from file_or_name import file_or_name
from unicode_write.data import DATA_DIR


def get_unicode_mapping(start: int = 0, end: int = 0x10FFF + 1) -> Dict[str, str]:
    names = {}
    for c in range(start, end):
        try:
            names[unicodedata.name(chr(c))] = hex(c)[2:]
        except ValueError:
            pass
    return names


@file_or_name
def get_emojis(path: str = os.path.join(DATA_DIR, "emoji.json")) -> Dict[str, str]:
    emojis = json.load(path)
    mapping = {}
    for emoji in emojis:
        mapping[" ".join(chain([emoji["name"]], emoji.get("aliases", [])))] = emoji["codes"]
    return mapping


def merge_mappings(*mappings):
    revs = [{v: k for k, v in mapp.items()} for mapp in mappings]
    merged = {}
    for rev in revs:
        for v, k in rev.items():
            if v not in merged:
                merged[v] = k
    return {k: v for v, k in merged.items()}


class UnicodeWriter:
    def __init__(self, names: Dict[str, str]):
        self.names = names

    def __call__(self, name):
        try:
            return unicodedata.lookup(name)
        except KeyError:
            return to_unicode(self.names.get(name, ""))


def to_unicode(codepoint: str) -> str:
    if not codepoint:
        return ""
    return chr(int(codepoint, 16))


def remove_suffix(string: str, suffix: str) -> str:
    if suffix and string.endswith(suffix):
        return string[: -len(suffix)]
    return string[:]


def remove_prefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix) :]
    return string[:]


def stem(string: str) -> str:
    string = string.lower()
    string = remove_suffix(string, "wards")
    string = remove_suffix(string, "ing")
    return string


def get_cache_path(cache: str = ".unicode-lookup-cache.pkl"):
    data_home = os.getenv("XDG_DATA_HOME", os.path.join(os.getenv("HOME"), ".local", "share"))
    return os.path.join(data_home, cache)
