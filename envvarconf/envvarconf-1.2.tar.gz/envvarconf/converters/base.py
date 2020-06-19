from decimal import Decimal

ALLOWED_TYPES = [
    str,
    int,
    float,
    Decimal,
]


class ConverterBase:
    def convert(self, value, to_type):
        """
        Convert variable raw value to typed variable

        :param value: variable raw value
        :param to_type: Target type
        :return: typed variable
        """
        raise NotImplementedError
