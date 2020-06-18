import base64
import json

import zlib


# @lru_cache(15)  # Caching actually makes this slower, so don't.
def inflate(compressed_byte_string):
    if isinstance(compressed_byte_string, dict):
        # The assumed-json byte string is actually an object already.
        dict_object = compressed_byte_string

        # So just return it as is.
        return dict_object

    compressed_byte_string = base64.b64decode(compressed_byte_string)

    json_string = zlib.decompress(compressed_byte_string)

    dict_object = json.loads(json_string)

    return dict_object


def inflate_data(data: dict) -> dict:
    """
    Decompress the values of a data dictionary, if they were compressed.

    :param data: The data dictionary whose values shall be decompressed.

    :return: The data dictionary with its values decompressed.
    """
    data: dict = {
        sink: {
            source: inflate(value)
            for source, value in data[sink].items()
        } for sink in data
    }

    return data
