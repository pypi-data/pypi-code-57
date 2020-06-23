from pydantic import BaseModel, Field, ValidationError
from pydantic.generics import GenericModel

__all__ = ["IntrospectableObject", "Field", "ValidationError", "GenericModel"]


class IntrospectableObject(BaseModel):
    """ Introspectable object based on pydantic """

    class Config:
        validate_assignment = True
