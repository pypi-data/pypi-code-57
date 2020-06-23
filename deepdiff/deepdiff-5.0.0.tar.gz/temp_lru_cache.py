import random
from functools import lru_cache


@lru_cache(maxsize=100)
def func(key, report_type=None):
    print(f'running {key}, {report_type}')
    result = {key: 'bppjpp'}
    if report_type:
        result = func(key)
        result[report_type] = random.randint(0, 5000)
    return result


for i in range(1, 100):
    key = random.randint(0, 500)
    report_type = random.choice(['rep1', 'rep2', None, None, None, None])
    print(func(key, report_type=report_type))

print(func.cache_info())
