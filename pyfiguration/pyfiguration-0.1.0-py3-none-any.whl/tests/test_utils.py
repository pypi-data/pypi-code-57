from pyfiguration.utils import from_dot_notation, merge_dictionaries


def test_from_dot_notation():
    testDict = {"level1": {"level2": {"level3": "test"}}}
    value = from_dot_notation(field="level1.level2.level3", obj=testDict)
    assert value == "test"


def test_merge_dictionaries():
    testDict1 = {"level1": {"level2": 123}}
    testDict2 = {"level1": {"level2": 321}}
    value = merge_dictionaries(testDict1, testDict2)
    assert isinstance(value, dict)
    assert "level1" in value
    assert "level2" in value["level1"]
    assert value["level1"]["level2"] == 321
