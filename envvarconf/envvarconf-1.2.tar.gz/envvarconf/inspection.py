from typing import Type, Dict, get_type_hints, TYPE_CHECKING

if TYPE_CHECKING:
    from envvarconf import BaseSettings


def get_settings_variables(settings: 'BaseSettings') -> Dict[str, Type]:
    annotations = {}
    for inherited_class in reversed(settings.__class__.__mro__):
        if inherited_class != object:
            annotations.update(get_type_hints(inherited_class))
    return annotations
