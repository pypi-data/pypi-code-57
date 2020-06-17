"""
   SDC Utilities module
"""


def parse_query_string_parameters(*, query_string_parameters: dict) -> dict:
    """
        Parse HTTP query string parameters into a more usable dictionary

        args:
            query_string_parameters (dict): The query string parameters from a request

        return:
            query_string_parameters (dict) : Returns the usable dictionary

    """
    parameters = {}
    for key, value in query_string_parameters.items():
        parts = key.replace(']', '').split('[')
        if len(parts) == 2:
            if not parameters.get(parts[0]):
                parameters[parts[0]] = {}
            parameters[parts[0]][parts[1]] = value
        else:
            parameters[parts[0]] = value

    return parameters


def dict_query(*, dictionary: dict, path: str):
    """
        Perform a 'dot notation' query on a dictionary

        args:
            dictionary (dict): The dictionary to query
            path (string): The dot notation query path

        return:
            value: Returns the value at the specified path

    """
    keys = path.split('.')
    value = None
    for key in keys:
        if value:
            if isinstance(value, list):
                if not key.isdigit():
                    return None

                value = list(value)[int(key)]
            else:
                value = value.get(key, None)
        else:
            value = dictionary.get(key, None)

        if not value:
            break

    return value
