from pyfiguration.utils import fromDotNotation, mergeDictionaries


def test_fromDotNotation():
    testDict = {"level1": {"level2": {"level3": "test"}}}
    value = fromDotNotation(field="level1.level2.level3", obj=testDict)
    assert value == "test"


def test_mergeDictionaries():
    testDict1 = {"level1": {"level2": 123}}
    testDict2 = {"level1": {"level2": 321}}
    value = mergeDictionaries(testDict1, testDict2)
    assert isinstance(value, dict)
    assert "level1" in value
    assert "level2" in value["level1"]
    assert value["level1"]["level2"] == 321
