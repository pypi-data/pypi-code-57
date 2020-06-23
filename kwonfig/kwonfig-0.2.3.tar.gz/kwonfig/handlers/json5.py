from kwonfig.constants import JSON5_SUPPORTED
from . import Handler

if JSON5_SUPPORTED:
    import json5


class Json5Handler(Handler):
    enabled = JSON5_SUPPORTED

    suffix = 'json5'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        return json5.load(fp)
