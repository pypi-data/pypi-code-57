from time import time
from functools import lru_cache
from collections.abc import Mapping
import json

from copy import deepcopy
from contextlib import contextmanager

from spintop.models.serialization import get_json_serializer
from spintop.utils import utcnow_aware, dict_ops

from . import singer
from ..logs import _logger

logger = _logger('singer')

DATETIME_TYPE = {'type': 'string', 'format': 'date-time'}

SCHEMA_ADDITIONS = {
    singer.SEQUENCE : {"type": "integer"},
    singer.BATCHED_AT: DATETIME_TYPE
}

@lru_cache()
def utcdatetime(_currenttime):
    """Computed only if current time changes."""
    return utcnow_aware()

class SingerMessagesFactory(object):
    def __init__(self, stream_name, add_null_to_fields=True):
        self.stream_name = stream_name
        self.transform_schema_kwargs = dict(
            add_null_to_fields=add_null_to_fields
        )
        self.logger = logger.getChild(stream_name)

    def schema(self, schema , key_properties):
        schema = deepcopy(schema)
        schema['properties'].update(SCHEMA_ADDITIONS)
        _schema_transform(schema, **self.transform_schema_kwargs)
        schema = change_keys_deep(schema, sanitize_key)
        return {
            'type': 'SCHEMA',
            'stream': self.stream_name,
            'key_properties': key_properties,
            'schema': schema
        }

    def record(self, data):
        current_time = int(time()*1000*1000)
        data.update({
            singer.SEQUENCE: current_time,
            singer.BATCHED_AT: utcdatetime(current_time)
        })
        data = change_keys_deep(data, sanitize_key, remove_none)
        return {
            'type': 'RECORD',
            'stream': self.stream_name,
            'record': data
        }

class AbstractSingerTarget(object):
    add_null_to_fields = False
    message_factory = SingerMessagesFactory
    
    def __init__(self):
        self.serializer = get_json_serializer()
    
    @contextmanager
    def stream(self, stream_name):
        batch = CollectMessagesFromFactory(self.message_factory(stream_name, add_null_to_fields=self.add_null_to_fields))
        yield batch
        self.send_messages(self.json_dumps_messages(batch.messages))

    def json_dumps_messages(self, messages):
        serialized_messages = [self.serializer.serialize(msg) for msg in messages]
        return [json.dumps(ser_msg) for ser_msg in serialized_messages]
    
    def send_messages(self, messages_str):
        raise NotImplementedError()

class CollectMessagesFromFactory(object):
    def __init__(self, factory):
        self.messages = []
        self.factory = factory

    def __getattr__(self, key):
        factory_fn = getattr(self.factory, key)
        def _wrapper(*args, **kwargs):
            self.messages.append(factory_fn(*args, **kwargs))
        return _wrapper

### Replace datetime by string type.
_FIELD_TRANSFORM = {
    'datetime': lambda field: DATETIME_TYPE
}

def _schema_transform(schema, add_null_to_fields=True):
    try:
        fields = schema.get('properties', {})
    except AttributeError:
        return 
    
    for key, field in fields.items():
        # Try to get type in map, else keep same.
        # Also add null allowed everywhere.
        
        transformer = _FIELD_TRANSFORM.get(field['type'], None)
        if transformer:
            update = transformer(field)
            field.update(update)

        if add_null_to_fields:
            field['type'] = [field['type'], 'null']

        # in case it contains other properties (object)
        _schema_transform(field, add_null_to_fields=add_null_to_fields)

class RemoveValue(Exception):
    pass

def sanitize_key(key):
    return key.replace('.', '_')

def remove_none(value):
    if value is None:
        raise RemoveValue()
    else:
        return value

def noop(value):
    return value

def change_keys_deep(dict_obj, key_op, value_op=noop):
    new_flat = {}
    flat = dict_ops.flatten_dict(dict_obj)
    for key_tuple, value in flat.items():
        new_key_tuple = tuple(key_op(key) for key in key_tuple)
        try:
            new_flat[new_key_tuple] = value_op(value)
        except RemoveValue:
            pass

    return dict_ops.deepen_dict(new_flat)
