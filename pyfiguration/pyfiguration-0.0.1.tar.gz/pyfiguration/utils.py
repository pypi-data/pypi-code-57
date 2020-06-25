import operator

from functools import reduce
from typing import Optional, List


def mergeDictionaries(a: dict, b: dict, path: Optional[List[str]] = None):
    """ Merges dictionary b into a, prefering keys in b over keys in a.

    Args:
        a: The destination dictionary
        b: The source dictionary
        path: The full path in the destination dictionary (for recursion)

    Returns:
        merged: The merged dictionaries
    """

    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergeDictionaries(a[key], b[key], path + [key])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

def fromDotNotation(field: str, obj: dict):
    """ Method to retrieve a value from the configuration using dot-notation.
    Dot-notation means nested fields can be accessed by concatenating all the parents
    and the key with a "." (e.g. db.driver.name).

    Args:
        field: The field (in dot-notation) to access
        obj: The object to access using dot-notation

    Returns:
        value: The value at the specified key, in the specified obj
    """

    # Split the key into separate element
    keys = field.split(".")

    def retrievePart(obj, key):
        # Return an empty dict when the key doesn't exist
        if key not in obj:
            obj[key] = {}
        return operator.getitem(obj, key)

    # Use reduce to traverse the dictionary and retrieve the required keys
    value = reduce(retrievePart, keys, obj)
    return value
