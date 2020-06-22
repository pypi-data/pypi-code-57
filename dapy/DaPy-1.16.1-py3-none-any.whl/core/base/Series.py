from copy import copy
from collections import Counter
from itertools import repeat, compress, accumulate, filterfalse, chain
from datetime import datetime, timedelta
from operator import add, sub, mul, mod, pow
from operator import eq, gt, ge, lt, le
from operator import itemgetter
from math import sqrt
from heapq import nlargest, nsmallest
from time import clock

try:
    from numpy import darray
except ImportError:
    darray = list

from .constant import STR_TYPE, VALUE_TYPE, SEQ_TYPE, DUPLICATE_KEEP, PYTHON3, nan
from .utils import filter, map, range, xrange, zip, zip_longest, get_isnan
from .utils import is_iter, is_math, is_seq, is_value, isnan, auto_plus_one
from .utils.utils_isfunc import SET_SEQ_TYPE

if PYTHON3:
    from operator import truediv as div, itemgetter
else:
    from operator import div, itemgetter
    
SHAPE_UNEQUAL_WARNING = "can't broadcast together with lenth %d and %d"

def quickly_apply(operation, left, right, NaN=nan):
    assert callable(operation) is True
    return Series(map(operation, left, right), NaN)

getter1, getter0 = itemgetter(1), itemgetter(0)

class Series(list):
    def __init__(self, array=[], NaN=nan):
        if is_iter(array) is False:
            array = (array,)
        if isinstance(array, Series):
            NaN = array.nan
        list.__init__(self, array)
        self.nan = NaN

    @property
    def src(self):
        return self

    @property
    def nan(self):
        return self._NaN

    @nan.setter
    def nan(self, NaN):
        self._NaN = NaN
        self._isnan = get_isnan(NaN)

    @property
    def shape(self):
        return (len(self), 1)

    def __repr__(self):
        if len(self) > 10:
            head = ','.join(map(str, self[:5]))
            tail = ','.join(map(str, self[-5:]))
            return 'Sereis([%s, ..., %s])' % (head, tail)
        return 'Series(%s)' % list.__repr__(self)

    def __eq__(self, other):
        other = self._check_operate_value(other)
        return quickly_apply(eq, self, other)

    def __gt__(self, other):
        other = self._check_operate_value(other)
        return quickly_apply(gt, self, other)

    def __ge__(self, other):
        other = self._check_operate_value(other)
        return quickly_apply(ge, self, other)

    def __lt__(self, other):
        other = self._check_operate_value(other)
        return quickly_apply(lt, self, other)

    def __le__(self, other):
        other = self._check_operate_value(other)
        return quickly_apply(le, self, other)

    def __setitem__(self, key, val):
        '''refresh data from current series

        Parameters
        ----------
        key : slice, int, same-size series and tuple

        val : single value or iterable container

        Return
        ------
        None
        '''
        setitem = list.__setitem__
        if isinstance(key, int):
            setitem(self, key, val)

        if isinstance(key, Series):
            err = 'Index should be same size with current series'
            assert len(key) == len(self), err
            for i, key in enumerate(key):
                if key is True:
                    setitem(self, key, val)

        if is_seq(key):
            for key in key:
                setitem(self, key, val)

        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            start = start if start > 0 else start + len(self)
            stop = start if stop > 0 else stop + len(self)
            val = repeat(val, int((stop - start) / 2)) if is_value(val) else val
            setitem(self, key, val)                        
    
    def __getitem__(self, key):
        '''get data from current series

        Parameters
        ----------
        key : slice, int, same-size series and tuple

        Return
        ------
        number or numbers in Series

        Example
        -------
        >>> ser = Series(range(2, 10))
        >>> ser[2:5] # get elements by slice
        [4, 5, 6]
        >>> ser[-1] # get element by index
        9
        >>> ser[ser > 4] # get elements by sequence of bool
        [5, 6, 7, 8, 9]
        >>> ser[2, 4, 2, 3] # get elements by multiple index
        [4, 6, 4, 5]
        '''
        if isinstance(key, int):
            return list.__getitem__(self, key)
        
        if isinstance(key, Series):
            assert len(key) == len(self)
            return Series(compress(self, key), self.nan)

        if is_seq(key):
            if len(key) == 1:
                return Series([list.__getitem__(self, key[0])], self.nan)
            
            if len(key) < len(self) * 0.1:
                return Series(map(list.__getitem__, repeat(self, len(key)), key),
                              NaN=self.nan)
        
        if is_iter(key):
            try:
                key = itemgetter(*key)
            except TypeError:
                return Series(NaN=self.nan)
            
        if isinstance(key, itemgetter):
            list_self = list(self)
            return Series(key(list_self), self.nan) 
        
        if isinstance(key, slice):
            return Series(list.__getitem__(self, key), self.nan)

    def __delitem__(self, key):
        '''delete data from current series

        Parameters
        ----------
        key : slice, int, same-size series and tuple

        Return
        ------
        number or numbers in Series

        Example
        -------
        >>> ser = Series(range(2, 10))
        >>> ser[2:5] # get elements by slice
        [4, 5, 6]
        >>> ser[-1] # get element by index
        9
        >>> ser[ser > 4] # get elements by sequence of bool
        [5, 6, 7, 8, 9]
        >>> ser[2, 4, 2, 3] # get elements by multiple index
        [4, 6, 4, 5]
        '''
        func = list.__delitem__
        if isinstance(key, int):
            return func(self, key)
        
        if isinstance(key, Series):
            assert len(key) == len(self)
            for ind, val in enumerate(key):
                if val:
                    func(self, ind)

        if isinstance(key, (tuple, list)):
            key = sorted(set(key), reverse=True)
            for ind in key:
                func(self, ind)

        if isinstance(key, slice):
            func(self, key)

    def __getslice__(self, start, stop, step=1):
        token = slice(start, stop, step)
        return Series(list.__getitem__(self, token), self.nan)

    def _check_operate_value(self, value):
        lself = len(self)
        if is_value(value):
            return repeat(value, lself)
        
        if hasattr(value, 'len') is False:
            value = list(value)
            
        rl = len(value)
        assert lself == rl, SHAPE_UNEQUAL_WARNING % (lself, rl)
        return value

    def __add__(self, right):
        '''[1, 2, 3] + 3 -> [4, 5, 6]
        [1, 2, 3] + [4, 5, 6] -> [5, 7, 9]
        '''
        right = self._check_operate_value(right)
        return quickly_apply(add, self, right, self.nan)

    def __radd__(self, left):
        '''3 + [1, 2, 3] -> [4, 5, 6]
        '''
        left = self._check_operate_value(left)
        return quickly_apply(add, left, self, self.nan)

    def __sub__(self, right):
        '''[1, 2, 3] - 3 -> [-2, -1 ,0]
        '''
        value = self._check_operate_value(right)
        return quickly_apply(sub, self, value, self.nan)
    
    def __rsub__(self, left):
        '''3 - [1, 2, 3] -> [2, 1, 0]
        '''
        value = self._check_operate_value(left)
        return quickly_apply(sub, value, self, self.nan)

    def __mul__(self, right):
        '''[1, 2, 3] * 3 -> [3, 6, 9]
        '''
        value = self._check_operate_value(right)
        return quickly_apply(mul, self, value, self.nan)

    def __rmul__(self, left):
        '''3 * [1, 2, 3] -> [3, 6, 9]
        '''
        value = self._check_operate_value(left)
        return quickly_apply(mul, value, self, self.nan)

    def __div__(self, right):
        '''[1, 2, 3] / 2 -> [0.5, 1, 1.5]
        '''
        value = self._check_operate_value(right)
        return quickly_apply(div, self, value, self.nan)

    def __truediv__(self, right):
        return self.__div__(right)

    def __rdiv__(self, left):
        '''3 / [1, 2, 3] -> [3, 1.5, 1]
        '''
        value = self._check_operate_value(left)
        return quickly_apply(div, value, self, self.nan)

    def __mod__(self, right):
        '''[1, 2, 3] % 3 -> [0, 0, 1]
        '''
        value = self._check_operate_value(right)
        return quickly_apply(mod, self, value, self.nan)

    def __rmod__(self, left):
        '''3 % [1, 2, 3] -> [3, 1, 1]
        '''
        value = self._check_operate_value(left)
        return quickly_apply(mod, value, self, self.nan)

    def __pow__(self, right):
        '''[1, 2, 3] ** 2 -> [1, 4, 9]
        '''
        value = self._check_operate_value(right)
        return quickly_apply(pow, self, value, self.nan)

    def __float__(self):
        '''float([1, 2, 3]) -> [1.0, 2.0, 3.0]
        '''
        return Series(map(float, self), self.nan)

    def __abs__(self):
        '''abs([-1, 2, -3]) -> [1, 2, 3]
        '''
        return Series(map(abs, self), self.nan)

    def abs(self):
        return self.__abs__()

    def accumulate(self, func=None, skipna=True):
        '''return accumulate for each item in the series'''
        assert skipna in (True, False), '`skipna` must be True or False'
        values = Series(self, self.nan) if skipna else self
        if skipna:
            values[self.isnan()] = 0.0
        return Series(accumulate(values, func), self.nan)

    def apply(self, func, *args, **kwrds):
        return Series((func(_, *args, **kwrds) for _ in self), self.nan)

    def argmax(self):
        max_val, max_ind = - float('inf'), None
        for ind, val in enumerate(self):
            if val > max_val:
                max_val, max_ind = val, ind
        return max_ind

    def argmin(self):
        min_val, min_ind = float('inf'), None
        for ind, val in enumerate(self):
            if val < min_val:
                min_val, min_ind = val, ind
        return min_ind

    def argsort(self, key=None, reverse=False):
        '''return the indices that would sort an array

        Parameters
        ----------
        key : function or None (default=None)

        reverse : True or False (default=False)

        Return
        ------
        Series : index of original data

        Example
        -------
        >>> Series([5, 2, 1, 10]).argsort()
        Series([2, 1, 0, 3])
        '''
        arr = map(getter0, sorted(enumerate(self), key=getter1, reverse=reverse))
        return Series(arr, self.nan)

    def between(self, left, right, boundary='both'):
        '''select the values which fall between `left` and `right`

        this function quickly select the values which are larger
        than `left` as well as smaller than `right`

        Parameters
        ----------
        left : val
            to select values which are all larger than `left`

        right : val
            to select values which are all less than `right`

        boundary : 'both', False, 'left', 'right (default='both')
        '''
        assert boundary in ('both', False, 'left', 'right')
        bound_left, bound_right = ge, ge
        if boundary in (False, 'right'):
            bound_left = gt
        if boundary in (False, 'left'):
            bound_right = gt
        def func(x):
            bound_left(left, x) and bound_rgiht(right, x)
        return Series(map(func, self), self.nan)

    def cv(self):
        '''Coefficient of variation of series data'''
        Ex, Ex2, length = 0, 0, float(len(self))
        if length <= 1:
            return 0
        
        for val in self:
            Ex += val
            Ex2 += pow(val, 2)
        if Ex == 0:
            return sqrt((Ex2 - Ex ** 2 / length) / (length - 1.0))
        return sqrt((Ex2 - Ex ** 2 / length) / (length - 1.0)) / (Ex / length)

    def count(self, compare_val=None):
        return self.countif(lambda val: val == compare_val, skipna=False)

    def countif(self, condition, skipna=True):
        '''return the number of values that satisfies the condition'''
        assert callable(condition), '`condition` must be a callable object'
        arr = self.dropna() if skipna is True else self
        return sum(map(condition, arr))

    def count_nan(self):
        '''return the number of NaN in the series'''
        return self.countif(self._isnan, False)
    
    def count_values(self):
        '''return a counter object that contains frequency of values'''
        return Counter(self)

    def diff(self, lag=1, keep_head=False):
        '''return a differential series that has only len(arr) - lag elements'''
        done = Series((r - l for l, r in zip(self[::lag], self[1::lag])), self.nan)
        if keep_head:
            done.insert(0, self.nan)
        return done

    def drop(self, todrop):
        '''remove values that matches `label` from the series'''
        if is_seq(todrop) is False:
            todrop = (todrop,)
        todrop = set(todrop)
        return Series(filterfalse(todrop.__contains__, self), self.nan)

    def drop_duplicates(self, keep=['first', 'last', False]):
        assert keep in ('first', 'last', False)
        
        # find the all ununiqual values: O(n)
        val_ind = {}
        for i, value in enumerate(self):
            val_ind.setdefault(value, []).append(i)

        # get index from the quickly preview table: O(k)
        to_drop_index, keep_arg = set(), DUPLICATE_KEEP[keep]
        for value, index in val_ind.items():
            if len(index) != 1:
                to_drop_index.update(index[keep_arg])

        # drop out these index: O(n)
        return Series((val for i, val in enumerate(self) if i not in to_drop_index), self.nan)

    def dropna(self):
        return Series(filterfalse(self._isnan, self), self.nan)

    def find_peaks(self, mode='peak', min_interval=None, min_variance=None, max_peaks=None):
        '''return indexes of peaks

        Find out all peaks / trough from the current series. This
        model can identify the platforms in trends and it will not
        return the index of platforms.
        
        This function is similar to 'findpeaks` function in MATLAB.
        The time complexity of this approach is O(n).

        Parameters
        ----------
        mode : str (default='peak')
            find out peaks or throughes from the series, choose
            'peak' or 'trough'

        min_interval : int (default=None)
            the peak will not appear again in which size of local window?

        min_variance : float (default=None)
            remove peaks that fluctuate less than `min_variance` from the top N peaks 

        Returns
        -------
        list : indexes of peak / trough in a list

        Examples
        --------
        >>> s1 = dp.Series([-5, 10, 10, 14, 8, 8, 6, 6, -3, 2, 2, 2, 2, -3])
        >>> s1.find_peaks() # return the index sequence of peaks
        [3, 9]
        >>> s1[s1.find_peaks()] # select the values of peaks
        Series([14, 2])
        
        >>> s2 = dp.Series([-5, 10, 12, 11, 13, 14, 11, 12, 10])
        >>> s2.find_peaks() # minimal interval between peaks is 1
        [2, 5, 7]
        >>> s2.find_peaks(min_interval=2) # minimal interval between peaks is 2
        [2, 5]

        >>> s1.find_peaks(mode='trough') # select the indexes of troughes
        [0, 8, 13] 
        '''
        assert mode in ('peak', 'trough')
        mode = mode == 'peak'
        assert min_interval is None or isinstance(min_interval, int), '`min_interval must be integer.'
        assert min_interval is None or min_interval > 1, '`min_interval` must be greater than 0.'
        assert min_variance is None or 0 <= min_variance <= 1, '`min_variance` must between 0 and 1.'
        #assert not(min_interval and min_variance)
        
        # calculate the first derivative of the sequence
        trend = self.diff(1, True).sign()
        
        # find platforms in bands and set them as parts of trend
        for i in range(len(trend) - 1, 0, -1):
            if trend[i] == 0:
                try:
                    if trend[i + 1] >= 0:
                        trend[i] = 1
                    else:
                        trend[i] = -1
                except IndexError:
                    pass
                result = trend.diff()

        # calculate the second derivative of the sequence
        if mode:
            ind = [i for i, val in enumerate(trend.diff()) if val < 0]
            if self[-1] > self[-2]:
                ind.append(len(trend) - 1)
        else:
            ind = [i for i, val in enumerate(trend.diff()) if val > 0]
            if self[-1] < self[-2]:
                ind.append(len(trend) - 1)

        # make sure there is only one peak in each minimal local window
        if min_interval or min_variance or max_peaks:
            # find out the top N peaks and flatten peaks that near to N peaks
            max_peaks = float('inf') if not max_peaks else max_peaks
            drop_index = set()
            top_peaks = set()

            # sort peaks
            peaks_info = [(self[i], i, loc) for loc, i in enumerate(ind)]
            sorted_peaks = sorted(peaks_info, reverse=mode)

            if min_interval:
                # max number of peaks
                max_num_peaks = int(len(self) / min_interval) + 1
                # number of peaks that need to be remove
                drop_peak_num = len(ind) - max_num_peaks
                _bias = lambda x, y: abs(x - y)
            else:
                _bias = lambda x, y: abs((x - y) / y)

            # flatten area that close to N top peaks
            for top_val, top_peak, loc in sorted_peaks:
                top_peaks.add(top_peak)
                if min_interval and len(drop_index) >= drop_peak_num or len(top_peaks) >= max_peaks:
                        break
                if min_variance and top_val == 0:
                    raise ZeroDivisionError('one of the peak is value 0, we cannot calculate the variance of this peak.')
                
                if top_peak in drop_index:
                    continue
                left, right = ind[loc:], ind[loc::-1]
                # flatten the surrounding area of the N toppest peak
                if min_interval:
                    for area in (left, right):
                        for peak_ind in area:
                            if _bias(peak_ind, top_peak) >= min_interval:
                                break
                            if peak_ind not in top_peaks:
                                drop_index.add(peak_ind)
                if min_variance:
                    for area in (zip(self[left], left), zip(self[right], right)):
                        for peak_val, peak_ind in area:
                            if _bias(peak_val, top_val) >= min_variance:
                                break
                            if peak_ind not in top_peaks:
                                drop_index.add(peak_ind)
            return [_ for _ in ind if _ not in drop_index]
        return ind
        
    def get(self, index, default=None):
        try:
            return list.__getitem__(self, index)
        except Exception:
            return default

    def has_duplicates(self):
        return len(self) != len(set(self))

    def head(self, numbers=5):
        return self.__getslice__(0, numbers, 1)

    def normalize(self):
        mini, maxm = float(min(self)), max(self)
        rang = maxm - mini
        return Series(map(lambda x: (x - mini) / rang, self), self.nan)
        
    def isnan(self):
        return Series(map(self._isnan, self))

    def kurt(self, skipna=True):
        arr = self.dropna() if skipna else self
        E = arr.mean(skipna=False)
        D = arr.std(skipna=False)
        return E ** 4 / D ** 2 - 3

    def map(self, func):
        '''given a map, return values that are tranformed by map

        Parameters
        ----------
        func : callable-object or dict

        Return
        ------
        Series : mapped values

        Examples
        --------
        >>> arr = dp.Series([3, 5, 7, 1])
        >>> arr.map(lambda val: val + 1)
        Series([4, 6, 8, 2])
        >>> arr.map({3: 'C'})
        Series(['C', 5, 7, 1])
        '''
        if isinstance(func, dict):
            obj = func
            func = lambda val: obj.get(val, val)
        assert callable(func), '`func` expects a callable object or dict-like object'
        return Series(map(func, self), self.nan)

    def max(self, skipna=True):
        arr = self.dropna() if skipna else self
        return max(arr)

    def max_n(self, n=1):
        return Series(nlargest(n, self))

    def mode(self, skipna=True):
        arr = self.dropna() if skipna else self
        return self.count_values().most_common()[0][0]

    def min(self, skipna=True):
        arr = self.dropna() if skipna else self
        return min(arr)

    def min_n(self, n=1):
        return Series(nsmallest(1, self))

    def mean(self, skipna=True):
        arr = self.dropna() if skipna else self
        return sum(arr, 0.0) / len(arr)

    def percenttile(self, q, skipna=True):
        arr = self.dropna() if skipna else self
        return sorted(arr)[int(q * len(arr))]

    def pop(self, ind):
        if isinstance(ind, int):
            return list.pop(self, ind)
        
        if isinstance(ind, slice):
            start, stop = ind.start, ind.stop
            return Series((list.pop(self, i) for i in xrange(start, stop)), self.nan)
        
        if is_seq(ind):
            ind = sorted(set(ind), reverse=True)
            to_ret = Series((list.pop(self, i) for i in ind), self.nan)
            to_ret.reverse()
            return to_ret

    @classmethod
    def range(cls, start, stop=None, step=1, NaN=nan):
        if stop is None:
            return cls(range(start, step), NaN)
        return cls(range(start, stop, step), NaN)
    
    def replace(self, old, new):
        return Series((new if _ == old else _ for _ in self), self.nan)

    @classmethod
    def repeat(cls, val=0, times=1, NaN=nan):
        '''Series.repeat(val=3, times=2) -> Series([3, 3])
        efficiently create a Series which contains `times` `val` as elements.
        '''
        return cls(repeat(val, times), NaN)

    def rolling(self, window, func, keep_head=False):
        '''Series.rolling(window) -> Series'''
        assert isinstance(window, int) and window > 0, '`window` must be an integer greater than 0'
        assert callable(func), '`func` must be a callable object'
        getter = list.__getitem__
        begin, stop = range(len(self) - window + 1), range(window, len(self))
        lag = window - 1 if keep_head else 0
        seq = (self[i, j] for i, j in zip(begin, stop))
        return Series(chain(repeat(self.nan, lag), map(func, seq)))

    def sign(self):
        '''arr.sign() -> arr
        Return the symbol of elements, NaN for un-numerical values
        '''
        def _sign(x):
            if not isinstance(x, (float, int)):
                return self.nan
            if x > 0:
                return 1
            if x < 0:
                return -1
            return 0
        return self.map(_sign)
    
    def sum(self, skipna=True):
        arr = self.dropna() if skipna else self
        return sum(arr, 0.0)

    def std(self, skipna=True):
        arr = self.dropna() if skipna else self
        Ex, Ex2, length = 0, 0, float(len(arr))
        if length <= 1:
            return 0
        
        for val in arr:
            Ex += val
            Ex2 += val ** 2
        return sqrt((Ex2 - Ex ** 2 / length) / (length - 1.0))

    def skew(self, skipna=True):
        arr = self.dropna() if skipna else self
        E = arr.mean(skipna=False)
        D = arr.std(skipna=False)
        E3 = arr.apply(pow, 3).mean(skipna=False)
        return (E3 - 3 * E * D - E ** 3) / (D ** 1.5)

    def tail(self, numbers=5):
        return self.__getslice__(len(self) - abs(numbers), len(self), 1)

    def tolist(self):
        return list(self)

    def toarray(self):
        try:
            from numpy import array
        except ImportError:
            raise ImportError("can't find numpy")
        else:
            return array(self)

    def unique(self):
        '''return unique items in the series'''
        uniq_vals, temp_vals = Series(NaN=self.nan), set()
        additem, appitem = set.add, list.append
        for i, val in enumerate(self):
            if val not in uniq_vals:
                additem(temp_vals, val)
                appitem(uniq_vals, val)
        return uniq_vals

    def var(self, skipna=True):
        arr = self.dropna() if skipna else self
        mean = self.mean(skipna=False)
        return sum((arr - mean()) ** 2)


SET_SEQ_TYPE.add(Series)

if __name__ == '__main__':
    init = Series(xrange(2, 8))
    assert all(init == [2, 3, 4, 5, 6, 7])
    assert len(init) == 6
    assert str(init) == 'Series([2, 3, 4, 5, 6, 7])'
    assert all(init[2:5] == [4, 5, 6])
    assert init[-1] == 7
    assert all(init[init >= 4] == [4, 5, 6, 7])
    
    assert all(init + 1 == [3, 4, 5, 6, 7, 8])
    assert all(init + init == [4, 6, 8, 10, 12, 14])
    assert all(init - 1 == [1, 2, 3, 4, 5, 6])
    assert all(init - init == [0, 0, 0, 0, 0, 0])
    assert all(init * 1 == [2, 3, 4, 5, 6, 7])
    assert all(init * init == [4, 9, 16, 25, 36, 49])
    assert all(init / 2.0 == [1, 1.5, 2, 2.5, 3, 3.5])
    assert all(init / init == [1, 1, 1, 1, 1, 1])

    assert all(1.0 + init == [3, 4, 5, 6, 7, 8])
    assert all(1 - init == [-1, -2, -3, -4, -5, -6])
    assert all(1 * init == [2, 3, 4, 5, 6, 7])
    assert all(10.0 / init == [5.0, 3.3333333333333335, 2.5, 2.0, 1.6666666666666667, 1.4285714285714286])
