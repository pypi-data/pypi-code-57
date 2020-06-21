"""Utility methods for use in the parser."""

import json
from contextlib import suppress
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Dict, Tuple

import lark

from mdfl.parser.exceptions import MissingNBTFieldError


__all__ = ["enter_tree", "get_nbt_items"]


@dataclass
class NBTItem:
    """Class representing an NBT item."""

    json_data: InitVar[dict]

    count: int = 1
    name: str = ""
    item: str = ""

    nbt_data: dict = field(default_factory=dict)

    def __post_init__(self, json_data: dict) -> None:
        """Initialise the NBTItem class."""
        for key in "item", "name":
            if key in json_data:
                setattr(self, key, json_data[key])
            else:
                raise MissingNBTFieldError(f"NBT item missing field: {key}")

        if "nbt" in json_data:
            self.nbt_data = json_data["nbt"]

    @property
    def nbt(self) -> str:
        """Dump the nbt_data dictionary as valid JSON."""
        return json.dumps(self.nbt_data)

    def __str__(self) -> str:
        """Return a string representation of the item."""
        string = f"{self.item} {self.count}"
        if self.nbt_data:
            string += f" {self.nbt}"
        return string


def enter_tree(tree: lark.Tree) -> Tuple[str, list]:
    """Return the name token and children of a tree."""
    name, *subtrees = tree.children
    if len(subtrees) == 1:
        return name, subtrees[0].children
    else:
        return name, subtrees


def get_nbt_items(root: Path) -> Dict[str, str]:
    """Look for nearby .json files, and return a list of global NBT items."""
    items: Dict[str, str] = {}
    paths = [*root.glob('*.json'), *root.glob('*/*.json')]

    for path in paths:
        # Skip the file if it doesn't contain a valid NBT item
        with suppress(MissingNBTFieldError):
            with path.open() as file:
                data = json.load(file)
            if type(data) is dict:
                item = NBTItem(data)
                items[item.name] = str(item)
            elif type(data) is list:
                items.update({
                    item.name: str(item)
                    for item in map(NBTItem, data)
                })
    return items
