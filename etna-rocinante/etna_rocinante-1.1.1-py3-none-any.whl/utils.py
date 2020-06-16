from functools import reduce
import string


def sanitize_for_filename(name: str) -> str:
    """
    Sanitize a string so that it can be used as a file name

    :param name:        the string to sanitize
    :return:            the sanitized string
    """
    allowed_chars = string.ascii_lowercase + string.digits
    name = map(lambda x: x if x in allowed_chars else '_', name.lower())
    return reduce(lambda acc, x: (acc + x) if x != '_' or (len(acc) > 0 and acc[-1] != '_') else acc, name, "")
