from decimal import Decimal

from envvarconf.converters.string_converter import StringConverter


def test_string_converter():
    converter = StringConverter()

    assert converter.convert("0.001", Decimal) == Decimal("0.001")
    assert converter.convert("hello", str) == "hello"
    assert converter.convert("0.1", float) == 0.1
    assert converter.convert("5", int) == 5
