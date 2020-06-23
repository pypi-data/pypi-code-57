import datetime

from decorator import decorator


class CrashAtException(Exception):
    message = "This method has stopped worked"


@decorator
def crash_after(func, date: str = None, *args, **kwargs):
    if date is None:
        return func(*args, **kwargs)

    now = datetime.datetime.now()
    _crash_after = datetime.datetime.strptime(date, "%m/%d/%Y")
    if _crash_after < now:
        raise CrashAtException("This method expired in it's corrent form on {0}".format(date))

    return func(*args, **kwargs)
