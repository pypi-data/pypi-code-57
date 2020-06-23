"""
Alicorn dependency injector
"""
import inspect
from typing import Optional, Union, Callable
from functools import wraps


def inject(app: 'alicorn.Alicorn' = None):
    """A decorator to automatically inject dependencies into the wrapped function when called. If app is specified then
    allows named dependencies to be specified using `Depends('name')`, otherwise only callables can be evaluated"""

    def wrap(f):
        injectables = {}

        for parameter in inspect.signature(f).parameters.values():
            if parameter.default is Depends or isinstance(parameter.default, Depends):
                if parameter.default.reference:
                    if app:
                        def run_dependency(*args, **kwargs):
                            return app._dependencies.get(parameter.default.reference)(*args, **kwargs)

                        injectables[parameter.name] = inject(app)(run_dependency)
                elif parameter.default.callable:
                    injectables[parameter.name] = inject(app)(parameter.default.callable)
                elif callable(parameter.annotation):
                    injectables[parameter.name] = inject(app)(parameter.annotation)
                else:
                    injectables[parameter.name] = lambda: parameter.annotation

        if not injectables:
            # Don't bother creating a wrapper if there aren't any injections
            return f

        @wraps(f)
        def wrapper(*args, **kwargs):
            """Find all dependencies and inject them into the function call"""
            for name, call in injectables.items():
                # print(injectables)
                kwargs[name] = call(*args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return wrap


class Depends:
    """Creates a new dependency-injected value that will be injected when called. If not initialised or initialised
    without any arguments it will call the type annotation of the argument. If a string is specified, it will find a
    reference to the value in the list of named dependencies created by `alicorn.Alicorn.dependency`. If a
    callable is specified, the callable will be called as the function is called.
    """
    callable = None
    reference = None

    def __init__(self, name_or_callable: Optional[Union[str, Callable]] = None):
        if isinstance(callable, str):
            self.reference = callable
        else:
            self.callable = callable
