"""
This module contains functions specifically designed to let the flags can be used with PyMongo.
"""
from bson import CodecOptions
from bson.codec_options import TypeRegistry, TypeEncoder

__all__ = ["register_encoder", "get_codec_options"]


def register_encoder(cls):
    """
    Register the flag class ``cls`` to the bson type encoder.

    :param cls: flag class the be registered
    """
    cls_encoder = type(f"Flag{cls.__name__}Encoder",
                       (TypeEncoder,),
                       {"transform_python": lambda self, value: value.code,
                        "python_type": property(lambda self: cls)})

    type_registry.append(cls_encoder())


type_registry: list = []


def get_codec_options() -> CodecOptions:
    """
    Get the bson codec options for PyMongo.

    :return: codec options for Pymongo
    """
    return CodecOptions(type_registry=TypeRegistry(type_registry))
