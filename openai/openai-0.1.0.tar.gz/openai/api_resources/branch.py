from openai import encoding, util
from openai.api_resources.abstract.engine_api_resource import EngineAPIResource
from openai.six.moves.urllib.parse import quote_plus


class Branch(EngineAPIResource):
    OBJECT_NAME = "branch"

    @classmethod
    def class_url(cls, engine):
        assert engine is not None
        engine = util.utf8(engine)
        extn = quote_plus(engine)
        return "/%s/engines/%s/branches" % (cls.api_prefix, extn)

    def make_encoding(self):
        return encoding.get(self.encoding)
