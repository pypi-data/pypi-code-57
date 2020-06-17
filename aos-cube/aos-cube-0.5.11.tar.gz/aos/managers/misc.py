import os
import re
import sys
import bz2
import gzip
import shutil
from aos.util import error, warning

_available_compression = ['gz', 'bz2']

class MiscError(Exception):
    pass

def aos_print(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()

def aos_info(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()

def aos_warning(msg):
    warning(msg)

def aos_error(msg):
    error(msg)

def version_greater_than(v1, v2):
    """ Return True is v1 > v2, False if v1 <= v2 """
    if not v1 or not v2:
        return False

    for i, j in zip(map(int, v1.split(".")), map(int, v2.split("."))):
        if i == j:
            continue
        return i > j

    return len(v1.split(".")) > len(v2.split("."))

def version_not_less_than(v1, v2):
    """ Return True is v1 > v2, False if v1 <= v2 """
    if not v1 or not v2:
        return False

    for i, j in zip(map(int, v1.split(".")), map(int, v2.split("."))):
        if i == j:
            continue
        return i > j

    return len(v1.split(".")) >= len(v2.split("."))

def _decompress_chunked(source, dest, ztype):
    """ Decompress metadata files """
    if ztype not in _available_compression:
        raise MiscError("%s compression not available" % ztype)

    if ztype == 'bz2':
        with bz2.BZ2File(source) as read, open(dest, "wb") as write:
            shutil.copyfileobj(read, write)
    elif ztype == 'gz':
        with gzip.open(source, "rb") as read, open(dest, "wb") as write:
            shutil.copyfileobj(read, write)


def decompress(filename, dest=None):
    """ take a filename and decompress it into the same relative location.
    if the file is not compressed just return the file """
    out = dest
    if not dest:
        out = filename

    if filename.endswith('.gz'):
        ztype='gz'
        if not dest:
            out = filename.replace('.gz', '')
    elif filename.endswith('.bz2'):
        ztype='bz2'
        if not dest:
            out = filename.replace('.bz2', '')
    else:
        return filename

    try:
        _decompress_chunked(filename, out, ztype)
    except:
        os.unlink(out)
        raise

    return out


_re_compiled_glob_match = None
def re_glob(s):
    """ Tests if a string is a shell wildcard. """
    global _re_compiled_glob_match
    if _re_compiled_glob_match is None:
        _re_compiled_glob_match = re.compile('[*?]|\[.+\]').search
    return _re_compiled_glob_match(s)
