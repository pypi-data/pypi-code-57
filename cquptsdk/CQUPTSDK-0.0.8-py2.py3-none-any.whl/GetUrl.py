import CQUPTSDK
import json
import os
#  @author Longm
#  @date 2020/6/23 16:34
#  Blog https://Longm.top

def ids():
    data = open(CQUPTSDK.__file__[:-11]+'config/url.json').read()
    djson = json.loads(data)
    ids= djson['ids']
    return ids
def jwzx():
    data = open(CQUPTSDK.__file__[:-11]+'config/url.json').read()
    djson = json.loads(data)
    jwzx = djson['jwzx']
    return jwzx