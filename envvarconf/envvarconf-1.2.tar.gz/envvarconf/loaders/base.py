from typing import Type, Any, TYPE_CHECKING

from envvarconf.converters.base import ConverterBase, ALLOWED_TYPES


if TYPE_CHECKING:
    from envvarconf import BaseSettings


class BaseLoader:
    """
    Abstract base loader class
    """
    converter: ConverterBase = ConverterBase()

    @classmethod
    def set_var(cls, settings: 'BaseSettings', varname: str, raw_value: Any, vartype: Type):
        assert vartype in ALLOWED_TYPES, f"Variable {varname} marked {vartype}, that not allowed for settings use"
        setattr(
            settings,
            varname,
            cls.converter.convert(raw_value, vartype)
        )

    def load(self, settings: 'BaseSettings') -> 'BaseSettings':
        raise NotImplementedError
