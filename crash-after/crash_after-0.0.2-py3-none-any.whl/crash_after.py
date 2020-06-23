import datetime

from decorator import decorator


class DateTimeException(Exception):
    message = "This method has stopped worked"


@decorator
def crash_after(func, date: str, *args, **kwargs):
    now = datetime.datetime.now()
    _crash_after = datetime.datetime.strptime(date, "%m/%s/%y")
    if _crash_after < now:
        raise DateTimeException

    return func(*args, **kwargs)


# pypi-AgENdGVzdC5weXBpLm9yZwIkOGU5MGU4ZDMtYTE3OC00YzI3LTg1ZDItOWM3MWYxMjY4YTZlAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiBrGH_xGISuiJGDn3oqqDwK323WVIjxMYpKN9K6Xv9Gxg
