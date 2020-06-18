from contextlib import contextmanager
from threading import local

# FIXME: For Django 3.0 support, replace this with asgiref.Local
_amp_mode_active = local()


@contextmanager
def activate_amp_mode():
    _amp_mode_active.value = True
    try:
        yield
    finally:
        del _amp_mode_active.value


def amp_mode_active():
    return hasattr(_amp_mode_active, 'value')
