from dataclasses import dataclass
from xtelligent_serial.data_class import DataClassProxy
from xtelligent_serial.json import from_json
from .fixtures import deep_json, DeepClass # pylint: disable=unused-import

@dataclass
class DC:
    x: int

def test_is_instance():
    assert isinstance(DC(1), DataClassProxy)
    assert issubclass(DC, DataClassProxy)

def test_deep_data_class(deep_json): # pylint: disable=redefined-outer-name
    dc = from_json(DeepClass, deep_json)
    assert dc.n.x == 'hello'
    assert dc.cb.ca.a == 2112
