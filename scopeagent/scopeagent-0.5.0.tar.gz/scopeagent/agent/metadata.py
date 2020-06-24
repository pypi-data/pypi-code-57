def parse_env_dictionary(raw_metadata):
    if not raw_metadata:
        return {}

    metadata = {}

    for key_value in raw_metadata.split(','):
        key, value = key_value.split('=', 1)
        metadata[key] = value

    return metadata


def parse_env_list(value):
    if not value:
        return []

    return value.split(',')


def parse_env_number(value):
    return int(value)
