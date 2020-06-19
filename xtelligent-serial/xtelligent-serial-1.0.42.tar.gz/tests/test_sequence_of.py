from xtelligent_serial.sequence_of import SequenceOf, SequenceOfType
from xtelligent_serial.json import from_json, to_json

from .fixtures import container_class_json, DCContainer # pylint: disable=unused-import

def test_sequence_of_syntax():
    s1 = SequenceOfType(int)
    s2 = SequenceOf[int]
    assert s1.type == s2().type
    assert s2().type == int

def test_deep_container(container_class_json): # pylint: disable=redefined-outer-name
    inst = from_json(DCContainer, container_class_json)
    j2 = to_json(inst)
    assert j2 == container_class_json
