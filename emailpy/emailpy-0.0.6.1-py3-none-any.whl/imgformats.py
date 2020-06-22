import os
import re
from base64 import *

formats = [x for x in os.listdir(os.path.join(os.path.dirname(__file__)))
           if '.' not in x and not os.path.isdir(os.path.join(
               os.path.dirname(__file__), x))]

def match(name):
    l = []
    for x in formats:
        l.append(x if bool(re.match(r'(.*).'+x, name)) else None)
    for x in l:
        if x:
            return x

def valid(data, ext):
    f = open(os.path.join(os.path.dirname(__file__), ext), 'rb').read()
    if type(data) == str:
        data = data.encode()
    if ext in formats:
        return data.startswith(f)
    return True

def get(attachment):
    ac = type(attachment)
    data = attachment.data
    name = os.path.basename(attachment.path)
    ext = match(name)
    if ext in formats:
        if not valid(data, ext):
            return ac(name, b64decode(data))
        return ac(name, data)
    return attachment
