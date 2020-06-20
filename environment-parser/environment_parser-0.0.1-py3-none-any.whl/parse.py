
def parse_string(value: str):
    """
    Convert string value to the appropriate python object.

    Arguments:
        value {str} -- String value of an environment variable

    Mapping:
        null    --  None
        true    --  True
        false   --  False
        [0-9]+  --  int
        **      --  str
    """
    if value is None:
        return None
    elif value == 'null':
        return None
    elif value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        try:
            return int(value)
        except ValueError:
            return value
