import random
from functools import lru_cache
from deepdiff.lfucache import LFUCache


def test_lfu():

    lfucache = LFUCache(10)
    for i in range(1, 100000):
        key = random.randint(0, 5000)
        value = random.randint(0, 5000)
        lfucache.set(key=key, value=value)


def test_lru():

    @lru_cache(maxsize=100)
    def func(key, report_type=None):
        result = {'baja': 'bppjpp'}
        if report_type:
            result = func(key)
            result[report_type] = random.randint(0, 5000)
        return result

    for i in range(1, 100000):
        key = random.randint(0, 5000)
        report_type = random.choice(['rep1', 'rep2', None, None, None, None])
        func(key)

    print(func.cache_info())


if __name__ == '__main__':
    # import timeit
    # if True:
    #     print('LFU')
    #     print(timeit.timeit("test_lfu()", number=10, setup="from __main__ import test_lfu"))
    # if True:
    #     print('LRU')
    #     print(timeit.timeit("test_lru()", number=10, setup="from __main__ import test_lru"))
