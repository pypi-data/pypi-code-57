import os
from json import dump
from typing import Dict, Any

DEFAULT_SCHEMA = {
    "schedules": {},
    "slots": {}
}


def init_json_database(
        path: str, schema: Dict[str, Any] = DEFAULT_SCHEMA) -> bool:
    if os.path.exists(path):
        return False
    with open(path, 'w') as f:
        dump(schema, f)  # type: ignore
    return True
