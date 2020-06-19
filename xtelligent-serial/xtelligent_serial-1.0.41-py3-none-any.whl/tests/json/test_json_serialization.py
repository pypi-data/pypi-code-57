from xtelligent_serial.json import to_json, from_json

from ..fixtures import Yah

def test_json_serialization():
    y1 = Yah(2112)
    json = to_json(y1)
    assert isinstance(json, str)
    y2 = from_json(Yah, json)
    assert isinstance(y2, Yah)
    assert y2.root == y1.root
