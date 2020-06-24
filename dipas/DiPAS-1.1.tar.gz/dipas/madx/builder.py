from collections import UserString
from numbers import Real
from typing import Any, Optional


class LiteralString(UserString):
    pass


def write_attribute_assignment(label: str, attribute: str, value: Any) -> str:
    return f'{label}->{attribute} = {write_attribute_value(value)};'


def write_attribute_increment(label: str, attribute: str, value: Real) -> str:
    operator = '+' if value >= 0. else '-'
    return f'{label}->{attribute} = {label}->{attribute} {operator} {write_attribute_value(abs(value))};'


def write_command(keyword: str, attributes: Optional[dict] = None, label: Optional[str] = None) -> str:
    """Convert the given keyword and attributes to a corresponding MADX command string."""
    if keyword == 'select' and 'column' in attributes:
        attributes.update(column=LiteralString(', '.join(attributes.pop('column'))))  # pop and update to make sure 'column' comes last.
    attr_string = write_attributes(attributes or {})
    if attr_string:
        cmd = f'{keyword}, {attr_string}'
    else:
        cmd = keyword
    if label is not None:
        cmd = f'{label}: {cmd}'
    return cmd


def write_attributes(attributes: dict) -> str:
    """Convert the given attributes to a corresponding MADX attribute string."""
    return ', '.join(f'{k} = {write_attribute_value(v)}' for k, v in attributes.items())


def write_attribute_value(x) -> str:
    """Convert an attribute value to its corresponding MADX representation."""
    if isinstance(x, bool):
        return str(x).lower()
    elif isinstance(x, (tuple, list)):
        return '{' + ', '.join(write_attribute_value(y) for y in x) + '}'
    elif isinstance(x, LiteralString):
        return str(x)
    elif isinstance(x, str):
        return f'"{x}"'
    return str(x)
