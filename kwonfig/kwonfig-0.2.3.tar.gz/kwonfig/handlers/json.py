import json
from . import Handler


class JsonHandler(Handler):
    suffix = 'json'

    @classmethod
    def load(cls, fp) -> Handler.Data:
        return json.load(fp)
