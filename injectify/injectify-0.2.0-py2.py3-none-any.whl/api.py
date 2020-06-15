"""This module contains the apis that power Injectify."""


def inject(target, injector):
    """A decorator that injects code in the target object.

    Args:
        target: The object to inject code into.
        injector: A :class:`~injectify.injectors.BaseInjector` to represent an
            injection point.
    """

    def decorator(f):
        injector.prepare(target=target, handler=f)
        injector.compile(injector.visit_target())
        return f

    return decorator
