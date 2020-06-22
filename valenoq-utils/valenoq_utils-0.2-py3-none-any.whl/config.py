import os
import json
import urllib.request

CONFIG_HOST = os.environ.get("CONFIG_HOST")
CONFIG_PORT = os.environ.get("CONFIG_PORT")
PARENT_HOST = os.environ.get("PARENT_HOST")
DEVELOP_HOST = os.environ.get("DEVELOP_HOST")
PRODUCTION_HOST = os.environ.get("PRODUCTION_HOST")

def get_config(name_container):
    address = "http://%s:%s?name=%s" %(CONFIG_HOST, CONFIG_PORT, name_container)
    if PARENT_HOST == DEVELOP_HOST:
        address += "&type=development"
    reply = urllib.request.urlopen(address).read()
    return json.loads(reply.decode("utf-8"))
