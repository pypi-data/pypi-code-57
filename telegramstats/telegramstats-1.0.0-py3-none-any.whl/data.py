from typing import *
import json


def from_file(path) -> dict:
    with open(path, encoding="UTF8") as file:
        return json.load(file)
