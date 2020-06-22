import re
import sys
import time
from difflib import SequenceMatcher

def ismac():
    return True if sys.platform == 'darwin' else False

def iswin():
    return True if sys.platform == 'win32' else False

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dict2attr(kv):
    kv = kv or {}
    o = type('', (), {})()
    for key, val in kv.items():
        setattr(o, key, val)
    return o

def attr2dict(o):
    o = o or type('', (), {})()
    r = {}
    attrs = [a for a in dir(o) if not a.startswith('_')]
    for attr in attrs:
        r[attr] = getattr(o, attr)
    return r

def tbl2dict(h, rs):
    '''h：表头list，rs：数据二维list。
    将每条数据（r）与表头按顺序匹配，形成dict list
    '''
    return [dict(zip(h, r)) for r in rs]

def extend_attrs(o, kv):
    o = o or type('', (), {})()
    kv = kv or {}
    if isinstance(o, dict):
        o = dict2attr(o)
    if not isinstance(kv, dict):
        kv = attr2dict(kv)

    for key, val in kv.items():
        setattr(o, key, val)
    return o

def update_attrs(o, kv):
    o = o or type('', (), {})()
    kv = kv or {}
    if isinstance(o, dict):
        o = dict2attr(o)
    if not isinstance(kv, dict):
        kv = attr2dict(kv)

    for key, val in kv.items():
        if hasattr(o, key):
            setattr(o, key, val)
    return o

def print_duration(method):
    """Prints out the runtime duration of a method in seconds
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed

def list_intersection(a, b, ordered=False):
    if ordered:
        return [i for i, j in zip(a, b) if i == j]
    else:
        return list(set(a).intersection(b)) # choose smaller to a or b?

def contains_digits(s):
    _digits = re.compile(r'\d')
    return bool(_digits.search(s))
