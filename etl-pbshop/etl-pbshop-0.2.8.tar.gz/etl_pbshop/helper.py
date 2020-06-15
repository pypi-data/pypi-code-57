from functools import wraps


def wrap_name(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        return func(*args,  **{**kwargs, **{'func_name': func.__name__}})
    return tmp