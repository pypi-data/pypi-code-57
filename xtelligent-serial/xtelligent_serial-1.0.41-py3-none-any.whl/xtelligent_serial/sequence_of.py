from dataclasses import dataclass
from typing import Type

from .registry import register_deserializer, deserialize

seq_type_cache = {}

@dataclass(frozen=True, eq=True, repr=True)
class SequenceOfType:
    type: Type

    def __getitem__(self, t):
        sot = seq_type_cache.get(t, None)
        if sot:
            return sot
        def initializer(self, **kwargs): # pylint: disable=unused-argument
            SequenceOfType.__init__(self, t)
        new_sot = type(f'SequenceOfType[{t}]', (SequenceOfType,), {
            '__init__': initializer
        })
        seq_type_cache[t] = new_sot
        def ds(raw_data: new_sot): # pylint: disable=invalid-name
            return [deserialize(t, item) for item in raw_data] # pylint: disable=no-value-for-parameter
        register_deserializer(new_sot, ds)
        return new_sot

SequenceOf = SequenceOfType(object)
''' In a `dataclass`, tells the (de)serializer to expect a sequence (usually list)
    of a specific type. `Sequence[SomeClass]` tells the deserializer to read the
    array and try to deserialize a `SomeClass` instance for each item.
'''
