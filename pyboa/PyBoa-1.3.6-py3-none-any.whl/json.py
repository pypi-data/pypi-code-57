import json
from .boa_obj import boa


def load(stream, **kw):
    """
        ``stream`` is ``string`` or have ``.read()`` like an ``fp``
        :return: the corresponding Python object
    """
    if hasattr(stream, 'read'):
        stream = stream.read()
    return boa(json.loads(stream, **kw))


loads = load

dump = json.dump
dumps = json.dumps
