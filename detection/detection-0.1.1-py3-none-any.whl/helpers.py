"""Detector's little helpers"""
from importlib import import_module
from typing import Any


def friendlyname_to_modulepath(friendlyname: str) -> str:
    """Convert a detector's "friendly name" to its implementation's path"""
    return f"detection.detectors.{friendlyname}.detector"


def friendlyname_to_classname(friendlyname: str) -> str:
    """Convert a detector's "friendly name" to its class name"""
    return f"{friendlyname.capitalize()}Detector"


def import_detector(friendlyname: str) -> Any:
    """Import a detector implementation"""
    return getattr(import_module(friendlyname_to_modulepath(friendlyname)), friendlyname_to_classname(friendlyname))
