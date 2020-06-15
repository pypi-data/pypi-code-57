"""Top-level package for Django Prepared Properties."""

__author__ = """Robin Ramael"""
__email__ = "robin.ramael@gmail.com"
__version__ = "0.1.0"

from .prepared_properties import (
    AnnotatedProperty,
    annotated_property,
    PrefetchedProperty,
    PropertiedQueryset,
)

__all__ = [
    "AnnotatedProperty",
    "annotated_property",
    "PrefetchedProperty",
    "PropertiedQueryset",
]
