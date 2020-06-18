import importlib
import inspect
from contextlib import contextmanager
from functools import wraps
from unittest.mock import patch


def delegate(*decorator_args, **decorator_kwargs):
    def decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return func_wrapper

    return decorator


@contextmanager
def undecorated_module(target_module, decorator):
    patcher = patch(decorator, side_effect=delegate)
    patcher.start()
    importlib.reload(target_module)

    try:
        yield target_module
    finally:
        patcher.stop()
        importlib.reload(target_module)


def assert_has_decorator(method, decorator, *args, **kwargs):
    decorator_mock = None
    mocked_module = None

    def get_full_name(func):
        return inspect.getmodule(func).__name__ + '.' + func.__qualname__

    tracked_full_name = get_full_name(method)

    tracked_calls = {}

    def tracker(*call_args, **call_kwargs):
        def tracker_decorator(func):
            full_name = get_full_name(func)
            tracked_calls[full_name] = True
            if tracked_full_name == full_name:
                decorator_mock.assert_called_with(*args, **kwargs)
                decorator_mock.reset_mock()

        return tracker_decorator

    try:
        with patch(decorator, wraps=tracker) as decorator_mock:
            mocked_module = inspect.getmodule(method)
            importlib.reload(mocked_module)
    finally:
        if mocked_module is not None:
            importlib.reload(mocked_module)

    if tracked_full_name not in tracked_calls:
        raise AssertionError('{} has no `{}` decorator!'.format(tracked_full_name, decorator))


def assert_not_null(env_var: str):
    if not env_var:
        raise OSError(f"{env_var} has not been set")
