from functools import wraps


def dummydec(*decorator_args, **decorator_kwargs):
    def dummy(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs) * decorator_kwargs['multiple_by']

        return func_wrapper

    return dummy
