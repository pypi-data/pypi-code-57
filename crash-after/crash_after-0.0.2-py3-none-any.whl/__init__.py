import datetime

from decorator import decorator


class DateTimeException(Exception):
    message = "This method has stopped worked"


@decorator
def crash_after(func, date: str = None, *args, **kwargs):
    if date is None:
        return func(*args, **kwargs)

    now = datetime.datetime.now()
    _crash_after = datetime.datetime.strptime(date, "%m/%s/%y")
    if _crash_after < now:
        raise DateTimeException

    return func(*args, **kwargs)
