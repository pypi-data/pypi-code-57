__all__ = ["private_field"]

from dataclasses import field, MISSING


def private_field(default=MISSING, default_factory=MISSING):
    return field(init=False, repr=False, compare=False,
                 default=default, default_factory=default_factory)
