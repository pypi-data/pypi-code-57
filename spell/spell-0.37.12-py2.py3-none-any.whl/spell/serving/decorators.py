from typing import Callable

from spell.serving.predictor import _InjectedParams


def with_background_tasks(name: str = "tasks") -> Callable:
    def decorator(f):
        if not hasattr(f, "__injected_params__"):
            f.__injected_params__ = _InjectedParams(background_tasks=name)
        else:
            f.__injected_params__.background_tasks = name
        return f

    return decorator


def with_full_request(name: str = "request") -> Callable:
    def decorator(f):
        if not hasattr(f, "__injected_params__"):
            f.__injected_params__ = _InjectedParams(request=name)
        else:
            f.__injected_params__.request = name
        return f

    return decorator
