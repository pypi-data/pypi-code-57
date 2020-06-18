"""INCached cache"""
import pickle
from typing import Dict, Any, Callable, Iterator
from deprecation import deprecated  # type: ignore
from .exceptions import ElementNotFoundException, ValueNotFoundException, ArgumentException

__version__ = "1.3 beta"
REMOVE_BY_ARGS = False
REMOVE_BY_VALUE = True


class _IncacheElement:
    def __init__(self, args, label):
        self.args = args
        self.label = label

    def __eq__(self, other):
        if not isinstance(other, _IncacheElement):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.args == other.args and self.label == other.label

    def __hash__(self):
        return hash((self.args, self.label))


class _IncacheValue:
    def __init__(self, value):
        self.value = value
        self.hash = hash(self.value)  # for future versions

    def __eq__(self, other):
        if not isinstance(other, _IncacheValue):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.value == other.value and self.hash == other.hash

    def __hash__(self):
        return hash((self.value, self.hash))


class INCached:
    """Provides cache for your func"""
    def __init__(self, cachesize: int = 100):
        """
        cachesize - max size of cache, set to 0 for no limits
        """
        self.original: bool = True  # for future versions
        self._cache: Dict[_IncacheElement, _IncacheValue] = {}
        self._cachesize: int = cachesize
        self.hits: int = 0
        self.misses: int = 0
        self.rejected: int = 0
        self._iter: Iterator

    def __eq__(self, other):
        return self._cache == other._cache

    def __ne__(self, other):
        return self._cache != other._cache

    def __lt__(self, other):
        return len(self._cache) < len(other._cache)

    def __gt__(self, other):
        return len(self._cache) > len(other._cache)

    def __le__(self, other):
        return len(self._cache) < len(other._cache) or self._cache == other._cache

    def __ge__(self, other):
        return len(self._cache) > len(other._cache) or self._cache == other._cache

    def __add__(self, other):
        ret = INCached(self._cachesize)
        ret._cache = {**self._cache, **other._cache}
        return ret

    def __sub__(self, other):
        ret = INCached(self._cachesize)
        ret._cache = self._cache
        for key in other._cache.keys():
            if key in ret._cache and ret._cache[key] == other._cache[key]:
                del ret._cache[key]
        return ret

    def __hash__(self):
        return hash(self._cache)

    def wrap(self, label: str = "default", filter_func: Callable = lambda args, kwargs: True):
        """Cache decorator"""
        def function_receiver(func):
            def wrapper(*args, **kwargs):
                return self.cache(func=func, args=args, kwargs=kwargs, label=label, filter_func=filter_func)
            return wrapper
        return function_receiver

    def check_original(self):  # for future versions
        """For future versions"""
        return self.original

    def cache(self, func: Callable, args: tuple, kwargs: Dict, label: str = "default",
              filter_func: Callable = lambda args, kwargs: True):
        """
        func - your function without ()
        args - tuple with args
        label - need for multiple funcs in one cache
        filter - function for filtering cache requests
        """
        if not filter_func(args, kwargs):
            self.rejected += 1
            return func(*args, **kwargs)
        try:
            cache_value = self._cache[_IncacheElement(args, label)]
            self.hits += 1
            return cache_value.value
        except KeyError:
            self.misses += 1
            if self._cachesize != 0:
                self._iter = iter(self._cache.keys())
                if len(self._cache) >= self._cachesize:
                    self.remove_element(next(self._iter))
            elem = _IncacheElement(args, label)
            self._cache[elem] = _IncacheValue(func(*args, **kwargs))
            return self._cache[elem].value

    def add_element(self, args: tuple, value: Any, label: str = "default"):
        """Add element to cache"""
        self._cache[_IncacheElement(args, label)] = _IncacheValue(value)

    def remove_element(self, args: tuple = None, label: str = "default", value: Any = None,
                       mode: bool = REMOVE_BY_ARGS):
        """Remove element from cache"""
        if mode and value is not None:
            try:
                self._cache.pop(list(self._cache.keys())[list(self._cache.values()).index(_IncacheValue(value))])
            except ValueError:
                raise ValueNotFoundException(value) from None
        elif not mode and args is not None:
            try:
                self._cache.pop(_IncacheElement(args, label))
            except KeyError:
                raise ElementNotFoundException(args) from None
        else:
            raise ArgumentException

    def cache_info(self) -> Dict[str, int]:
        """Get cache info"""
        return {"hits": self.hits, "misses": self.misses, "rejected": self.rejected, "cachesize": len(self._cache)}

    def clear_cache(self):
        """Clear cache"""
        self._cache = {}
        self.hits = 0
        self.misses = 0

    def clear_stats(self):
        """Clear hits and misses"""
        self.hits = 0
        self.misses = 0

    @deprecated(deprecated_in="1.3", removed_in="1.4", current_version=__version__,
                details="Use utils.save_full_cache instead")
    def save_cache(self, path: str, save_stats: bool = False, protocol=pickle.HIGHEST_PROTOCOL):
        """Save cache to file"""
        if save_stats:
            save = (self._cache, self.hits, self.misses)
        else:
            save = (self._cache, 0, 0)
        with open(path, "wb") as output:
            pickle.dump(save, output, protocol)

    @deprecated(deprecated_in="1.3", removed_in="1.4", current_version=__version__,
                details="Use utils.load_full_cache instead")
    def load_cache(self, path: str, load_stats: bool = False):
        """Load cache from file"""
        self.clear_cache()
        with open(path, "rb") as inp:
            self._cache, hits, misses = pickle.load(inp)
            if load_stats:
                self.hits, self.misses = hits, misses
