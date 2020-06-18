from scrapy import Request
from scrapy.http import Response, Headers


def _serialize(o):
    if isinstance(o, str):
        return o
    elif isinstance(o, bytes):
        return o.decode("utf8")
    elif isinstance(o, Request):
        return request_serialize(o)
    elif isinstance(o, Headers):
        return o.to_unicode_dict()
    return o


def request_serialize(r: Request):
    fields = ["_encoding", "method", "_url", "priority", "cookies", "headers",
              "dont_filter", "_meta", "_body"]
    return {rk: _serialize(rv) for rk, rv in r.__dict__.items() if rk in fields}


def response_serialize(r: Response):
    fields = ["headers", "status", "text", "_url", "flags", "encoding"]
    return {rk: _serialize(rv) for rk, rv in r.__dict__.items() if rk in fields}
