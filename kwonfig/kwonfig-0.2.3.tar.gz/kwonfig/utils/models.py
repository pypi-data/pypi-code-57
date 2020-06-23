"""
Pydantic helpers
"""
from kwonfig.constants import PYDANTIC_SUPPORTED

if PYDANTIC_SUPPORTED:
    def alias_generator(field_name: str) -> str:
        return field_name.replace('_', '-')

    class AliasConfig:
        alias_generator = alias_generator
