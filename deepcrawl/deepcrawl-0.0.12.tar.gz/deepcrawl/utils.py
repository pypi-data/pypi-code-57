from dateutil import parser

from deepcrawl.exceptions import ImmutableAttributeError


class ImmutableAttributesMixin:
    __slots__ = ['_instantiated']

    mutable_attributes = []

    def __init__(self):
        self._instantiated = True

    def __setattr__(self, key, value):
        # We don't want to allow immutable attributes to be changed after the object is instantiated
        if key not in self.mutable_attributes and getattr(self, "_instantiated", False):
            raise ImmutableAttributeError(f"Attribute {key} can't be added or changed.")
        super(ImmutableAttributesMixin, self).__setattr__(key, value)

    @property
    def to_dict(self):
        return {x: getattr(self, x, None) for x in self.__slots__}


def safe_string_to_datetime(str_):
    try:
        return parser.parse(str_)
    except Exception:
        return str_
