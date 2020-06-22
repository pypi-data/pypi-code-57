from math import isnan as _isnan
from re import compile as _compile
from operator import itemgetter
from collections import Counter

from DaPy.core.base.constant import PYTHON2, PYTHON3, STR_TYPE

from .utils_2to3 import (filter, map, pickle, range, split,
                         strip, xrange, zip, zip_longest)
from .utils_isfunc import is_empty, is_iter, is_math, is_seq, is_str, is_value, is_dict

__all__ = ['str2value', 'argsort', 'hash_sort',
           'is_value', 'is_math', 'is_iter', 'is_seq', 
           'range', 'xrange', 'map', 'zip', 'filter']

# since these functions are commonly used,
# we use saching mechanisms to optimize them.
if PYTHON3 is True:
    from functools import lru_cache
else:
    from repoze.lru import lru_cache

from .py_string_transfer import str2int, str2float, str2pct, str2bool, str2dt, str2date, str2time
    
def isnan(value):
    try:
        return _isnan(value)
    except Exception:
        return False

def get_isnan(nan_val):
    if isnan(nan_val) is True:
        return isnan
    return lambda val: val == nan_val

# following masks are used to recognize string patterns
FLOAT_MASK = _compile(r'^[-+]?[0-9]\d*\.\d*$|[-+]?\.?[0-9]\d*$')
PERCENT_MASK = _compile(r'^[-+]?[0-9]\d*\.\d*%$|[-+]?\.?[0-9]\d*%$')
INT_MASK = _compile(r'^[-+]?[-0-9]\d*$')
DATE_MASK = _compile(r'^(?:(?:1[6-9]|[2-9][0-9])[0-9]{2}([-/.]?)(?:(?:0?[1-9]|1[0-2])\1(?:0?[1-9]|1[0-9]|2[0-8])|(?:0?[13-9]|1[0-2])\1(?:29|30)|(?:0?[13578]|1[02])\1(?:31))|(?:(?:1[6-9]|[2-9][0-9])(?:0[48]|[2468][048]|[13579][26])|(?:16|[2468][048]|[3579][26])00)([-/.]?)0?2\2(?:29))$')
TIME_MASK = _compile(r'(^([01]{0,1}[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$)|(^([01]{0,1}[0-9]):[0-5][0-9](:[0-5][0-9]){0,1}[ ]{0,1}[A|P]M$)')
DT_MASK = _compile('^(?:(?:1[6-9]|[2-9][0-9])[0-9]{2}([-/.]?)(?:(?:0?[1-9]|1[0-2])\1(?:0?[1-9]|1[0-9]|2[0-8])|(?:0?[13-9]|1[0-2])\1(?:29|30)|(?:0?[13578]|1[02])\1(?:31))|(?:(?:1[6-9]|[2-9][0-9])(?:0[48]|[2468][048]|[13579][26])|(?:16|[2468][048]|[3579][26])00)([-/.]?)0?2\2(?:29))\ (([01]{0,1}[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])|(([01]{0,1}[0-9]):[0-5][0-9](:[0-5][0-9]){0,1}[ ]{0,1}[A|P]M)$')
BOOL_MASK = _compile('^(true)|(false)|(yes)|(no)|(\u662f)|(\u5426)|(on)|(off)$')

def auto_str2value(value, dtype=None):
    '''using preview masks to auto transfer a string to matchest date type

    Parameters
    ----------
    value : str 
        the string object that you expect to transfer

    dtype : str (default=None)
        "float" -> transfer value into float type
        "int" -> transfer value into int type
        "bool" -> transfer value into bool type
        "datetime" -> transfer value into datetime type
        "percent" -> str2value.auto("3.3", 'percent') -> 0.033
        "str" -> drop out all blanks in the both sides

    Examples
    --------
    >>>> str2value.auto('3')
    3
    >>> str2value.auto('3.3')
    3.3
    >>> str2value.auto(' 3.3.')
    '3.3.'
    >>> str2value.auto('2019-3-23')
    datetime.datetime(2019, 3, 23, 0, 0)
    >>> str2value.auto('3.3%')
    0.033
    >>> str2value.auto('Yes')
    True
    '''
    if dtype is not None:
        assert isinstance(dtype, STR_TYPE), 'prefer_type should be a string'
        assert dtype.lower() in ('float', 'int', 'bool', 'datetime', 'str')
        try:
            return fast_str2value[dtype](value)
        except ValueError:
            pass

    if INT_MASK.match(value):
        return str2int(value)    

    elif FLOAT_MASK.match(value):
        return str2float(value)

    elif PERCENT_MASK.match(value):
        return str2pct(value)

    elif DT_MASK.match(value):
        return str2dt(value)

    elif TIME_MASK.match(value):
        return str2time(value)

    elif DATE_MASK.match(value):
        return str2date(value)

    elif BOOL_MASK.match(value.lower()):
        return str2bool(value)

    else:
        return value

# this parser offers a higher speed than `if else` statement
fast_str2value = {'float': str2float,
            'int': str2int,
            'bool': str2bool,
            'datetime': str2date,
            'percent': str2pct,
            'str': lambda x: x,
            'bytes': lambda x: x,
            'date': str2date,
            'time': str2time}
if PYTHON3:
    fast_str2value['bytes'] = lambda x: x

def argsort(seq, key=None, reverse=False):
    '''sort a sequence than return the index of sequence

    Parameters
    ----------
    See: sorted

    Return
    ------
    list : index of original data

    Example
    -------
    >>> argsort([5, 2, 1, 10])
    [2, 1, 0, 3]
    '''
    sorted_seq = sorted(enumerate(seq), key=itemgetter(1), reverse=reverse)
    return tuple(map(itemgetter(0), sorted_seq))

def hash_sort(records, *orders):
    assert all(map(lambda x: isinstance(x[0], int), orders)), 'keyword must be int'
    assert all(map(lambda x: x[1] in ('ASC', 'DESC'), orders)), 'orders symbol should be "ASC" or "DESC"'

    compare_pos = [x[0] for x in orders]
    compare_sym = [x[1] for x in orders]
    size_orders = len(compare_pos) - 1
    
    def _hash_sort(datas_, i=0):
        # initialize values
        index = compare_pos[i]
        inside_data, HashTable = list(), dict()

        # create the diction
        for item in datas_:
            key = item[index]
            if key in HashTable:
                HashTable[key].append(item)
            else:
                HashTable[key] = [item]

        # sorted the values
        sequence = sorted(HashTable)

        # transform the record into Frame
        for each in sequence:
            items = HashTable[each]
            if i < size_orders:
                items = _hash_sort(items, i+1)
            inside_data.extend(items)

        # finally, reversed the list if necessary.
        if i != 0 and compare_sym[i] != compare_sym[i-1]:
            inside_data.reverse()
        return inside_data
    
    output = _hash_sort(records)
    if compare_sym[0] == 'DESC':
        output.reverse()
    return output

def auto_plus_one(exists, item, start=1):
    exists = set(map(str, exists))
    while '%s_%d' % (item, start) in exists:
        start += 1
    return '%s_%d' % (item, start)

def count_nan(nan_func, series):
    return sum(map(nan_func, series))

def beautiful_str_val(val):
    if isinstance(val, float) and abs(val) > 1:
        int_length = len(str(int(val)))
        template = '%10.' + str(10 - int_length + 1) + 'f'
        return template % val
    if isinstance(val, int):
        template = '%g' if val > 1e10 else '%10.' + str(11 - len(str(int(val)))) + 'g'
        return template % val
    return str(val).replace('\n', '')

def count_not_char(string):
    return len(tuple(filter(lambda val: ord(val) > 126, string)))

def count_str_printed_length(string):
    return len(string) + count_not_char(string)

def string_align(string, length, mode='center'):
    padding = length - count_not_char(string)
    if mode == 'center':
        return string.center(padding)
    if mode == 'left':
        return string.ljust(padding)
    return string.rjust(padding)
    
