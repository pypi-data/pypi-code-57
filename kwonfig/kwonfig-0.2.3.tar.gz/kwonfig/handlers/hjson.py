from kwonfig.constants import HJSON_SUPPORTED
from . import Handler

if HJSON_SUPPORTED:
    import hjson


class HJsonHandler(Handler):
    enabled = HJSON_SUPPORTED

    suffix = 'hjson'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        return hjson.load(fp)
