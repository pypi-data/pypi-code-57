import json
import datetime
from django import template
from django.contrib.humanize.templatetags import humanize

register = template.Library()


@register.simple_tag
def json_load(value):
    if value:
        return json.loads(value)
    return None


@register.filter
def easy_format(value):
    try:
        d = datetime.datetime.strptime(value)
        print(d)
        return d
    except Exception:
        pass
    try:
        d = datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S.%f")
        return d
    except Exception:
        pass

    try:
        d = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        return d
    except Exception:
        pass

    try:
        d = datetime.datetime.strptime(value, "%Y/%m/%d").date()
        return d
    except Exception:
        pass

    try:
        d = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        return d
    except Exception:
        pass

    try:
        c = humanize.intcomma(value)
        return c
    except Exception:
        pass
    return value
