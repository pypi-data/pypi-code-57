from pytime_converter.helper import recognized_unit_measure as rum
from pytime_converter.helper.input_regex_parser import parse_input


class ConvertUnitNotRecognizedException(Exception):
    pass


class InputNotInValidFormatException(Exception):
    pass


def get_milliseconds_value_for_input(input_string: str) -> float:

    matches = parse_input(input=input_string)

    if len(matches) == 0:
        raise InputNotInValidFormatException('the input is not recognized')

    number_value = convert_string_to_float(input=matches[0])

    convert_value = 1

    if len(matches) > 1 and matches[1] != '':
        if matches[1] in rum.milliseconds_allowed_strings():
            convert_value = 1
        elif matches[1] in rum.seconds_allowed_strings():
            convert_value = 1000
        elif matches[1] in rum.minutes_allowed_strings():
            convert_value = 1000 * 60
        elif matches[1] in rum.hours_allowed_strings():
            convert_value = 1000 * 60 * 60
        elif matches[1] in rum.days_allowed_strings():
            convert_value = 1000 * 60 * 60 * 24
        elif matches[1] in rum.years_allowed_strings():
            convert_value = 1000 * 60 * 60 * 24 * 365
        else:
            raise ConvertUnitNotRecognizedException(
                f'no unit conversion value found for unit {matches[1]}'
            )

    return int(number_value * convert_value)


def convert_string_to_float(input: str) -> float:
    try:
        return float(input)
    except ValueError:
        raise InputNotInValidFormatException('the value is not a valid float')
