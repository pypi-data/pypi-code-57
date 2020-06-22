
def timer(func):
    """@timer decorator"""
    from functools import wraps
    from time import time

    def concat_args(*args, **kwargs):
        for arg in args:
            yield str(arg)
        for key, value in kwargs.items():
            yield str(key) + '=' + str(value)

    @wraps(func)  # sets return meta to func meta
    def wrapper(*args, **kwargs):
        start = time()
        ret = func(*args, **kwargs)
        dur = format((time() - start) * 1000, ".2f")
        print('{}{}({}) -> {}ms.'.format(
            func.__module__ + '.' if func.__module__ else '',
            func.__qualname__,
            ', '.join(concat_args(*args, **kwargs)),
            dur,
            ))
        print()
        return ret
    return wrapper
