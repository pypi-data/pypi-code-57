from envvarconf.converters.base import ConverterBase


class StringConverter(ConverterBase):
    """
    Simple convert string representation to value
    """

    def convert(self, value: str, to_type):
        return to_type(value)
