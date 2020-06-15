from typing import Dict, Optional, TypeVar

T = TypeVar("T")


def get_or_else(
    dictionary: Dict[str, T], key: str, default_value_optional: Optional[T] = None
) -> Optional[T]:
    """
    Get the value safely from the dictionary.

    Parameters
    ----------
    dictionary : Dict[str, T]
        Dictionary
    key : str
        Key to get the value
    default_value_optional : Optional[T], optional
        Default if there is no value, by default None

    Returns
    -------
    Optional[T]
        If `default_value_optional` is not specified, None is returned if there is no value.
    
    Notes
    -----
    .. versionadded:: 0.1.1
    """
    return dictionary.get(key, default_value_optional)
