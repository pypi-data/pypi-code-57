import base64
from typing import Any, Dict, Optional
from google.protobuf.pyext._message import (
    RepeatedScalarContainer,
    ScalarMapContainer,
)


def unconvert_complextype(j, r, f):
    v = unconvert_obj(getattr(r, f.json_name))
    if v is not None:
        j[f.json_name] = v


def unconvert_field(j, r, f):
    if f.type == 11:  # object
        unconvert_complextype(j, r, f)
        return

    v = getattr(r, f.json_name)
    if isinstance(v, RepeatedScalarContainer):
        j[f.json_name] = []
        while True:
            try:
                j[f.json_name].append(v.pop())
            except IndexError:
                break
        return

    if f.type == 12:  # bytes
        j[f.json_name] = base64.b64encode(v).decode("ascii")
        return

    j[f.json_name] = v


def unconvert_obj(r) -> Optional[Dict[str, Any]]:
    """
    Convert a gRPC object into a dict.
    """
    if isinstance(r, ScalarMapContainer):
        return {k: v for k, v in r.items()}

    if not hasattr(r, "DESCRIPTOR"):
        print("No DESCRIPTOR for {} {}".format(type(r), r))
        return None

    j: Dict[str, Any] = {}
    for f in r.DESCRIPTOR.fields:
        unconvert_field(j, r, f)
    return j
