import time
from django import template

register = template.Library()

@register.simple_tag
def millisecond_timestamp():
    return str(int(round(time.time()*1000)))