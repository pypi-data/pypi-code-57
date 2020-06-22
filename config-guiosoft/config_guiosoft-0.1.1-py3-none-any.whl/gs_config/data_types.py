from datetime import date, datetime

from dateutil.parser import parse

from gs_config.logger import get_logger

CONFIG_TYPES = {
    str: lambda value: str(value),
    int: lambda value: int(value),
    float: lambda value: float(value),
    bool: lambda value: (str(value)+'0')[0].upper() in '1TSY',
    datetime: lambda value: parse(str(value)),
    date: lambda value: parse(str(value)).date()
}

CONFIG_TYPES_STR = {key: str(CONFIG_TYPES[key])
                    for key in CONFIG_TYPES}


def convert(value, data_type, default_value, key_name):
    """
    Converts value to type. Raises exception when invalid data
    """

    try:
        if data_type in CONFIG_TYPES:
            result = CONFIG_TYPES[data_type](value)
            if not isinstance(default_value, data_type):
                default_value = value
                raise DataTypeException(
                    'Default value must be of same type of data type ({0}) for env {1}'
                    .format(data_type, key_name)
                )
        else:
            raise DataTypeException(
                "Invalid data_type {0} for env {1}. Expected: {1}"
                .format(data_type,
                        key_name,
                        list(CONFIG_TYPES.keys())))

    except Exception as exc:
        get_logger().exception(exc)
        result = default_value

    return result


class DataTypeException(Exception):
    pass
