
# from https://stackoverflow.com/a/8856387/781180

import inspect
import re

from alogging.pp import pf


def echo_format(value, depth=1, caller_name='echo_format'):
    # calling_frame_record = inspect.stack()[1]
    calling_frame_record = inspect.stack()[depth]
    frame = inspect.getframeinfo(calling_frame_record[0])
    out = ''
    if frame.code_context:
        m = re.search(r"%s\((.+)\)" % caller_name, frame.code_context[0])
        if m:
            out = "{0} = {1}".format(m.group(1), pf(value))
    return out


def echo(value):
    print(echo_format(value, depth=2, caller_name='echo'))
