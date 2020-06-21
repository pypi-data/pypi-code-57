"""Parsing logic and grammar for MDFL."""

import re
import shutil
from pathlib import Path
from typing import List, Optional
from zipfile import ZipFile

from cookiecutter.main import cookiecutter

from lark import Lark, lark

from mdfl.parser.exceptions import InvalidNBTReferenceError
from mdfl.parser.utils import enter_tree, get_nbt_items


__all__ = ["parser", "create_pack"]

NBT_REFERENCE = re.compile(r'\$"(.+)"')
GRAMMAR = r"""
    start: (namespace | description)+

    description: "description" STRING
    namespace: "namespace" NAME "{" definition+ "}"

    definition: objective
              | function

    objective: "objective" NAME ";"
    function: "fun" NAME "{" instruction+ "}"

    instruction: objective
               | command
               | COMMENT

    command: TEXT ";"

    TEXT: /[^\/\n};]+/
    STRING: /"[^\n]+"/
    COMMENT: /\/\/[^\n]+/
    WHITESPACE: (" " | "\n")+

    %ignore COMMENT
    %ignore WHITESPACE
    %import common.CNAME -> NAME
"""

parser = Lark(GRAMMAR)


def create_pack(tree: lark.Tree, pack_name: str, source: Path, target: Optional[Path]) -> None:
    """Create a data pack, given an AST."""
    nbt_items = get_nbt_items(source)

    destination = Path(target) if target else Path(f"{pack_name}.zip")
    destination = destination.expanduser().absolute()
    if destination.is_dir():
        destination = destination / f"{pack_name}.zip"

    namespaces: List[dict] = []
    pack = {
        "name": pack_name,
        "namespaces": namespaces,
    }
    root = Path(pack_name)

    for subtree in tree.children:
        if subtree.data == "description":
            description = subtree.children[0].strip('"')
            pack["description"] = description
            continue

        functions: List[dict] = []
        name, definitions = enter_tree(subtree)
        namespace = {
            "name": str(name),
            "functions": functions
        }
        namespaces.append(namespace)

        for definition in definitions:
            first_child = definition.children[0]

            if getattr(first_child, "data", "") == "objective":
                scoreboard = first_child.children[0]
                # TODO: Implement scoreboard generators

            if definition.data == "function":
                commands: List[str] = []
                name, instructions = enter_tree(definition)
                for instruction in instructions:
                    command = str(instruction.children[0])
                    match = NBT_REFERENCE.search(command)
                    if match:
                        reference = match.group(1)
                        item = nbt_items.get(reference)
                        if item is None:
                            raise InvalidNBTReferenceError(
                                f"{reference} is not an existing NBT item."
                            )
                        command = NBT_REFERENCE.sub(item, command)
                    commands.append(command)
                functions.append({
                    "name": str(name),
                    "instructions": {
                        "commands": list(commands)
                    }
                })

    if "description" not in pack:
        pack["description"] = input(f"Description of {pack_name}: ")

    templates = Path(__file__).parent.parent / "templates"
    cookiecutter(
        str(templates / "pack"),
        extra_context=pack,
        no_input=True
    )

    for namespace in namespaces:
        name = namespace["name"]
        functions = root / "data" / name / "functions"
        functions.mkdir(parents=True)

        for function in namespace["functions"]:
            name = function["name"]
            cookiecutter(
                str(templates / "function"),
                extra_context=function,
                no_input=True
            )
            shutil.copy(
                f"{name}.function/{name}.mcfunction",
                functions / f"{name}.mcfunction"
            )
            shutil.rmtree(f"{name}.function")

    with ZipFile(str(destination), "w") as zipfile:
        for file in root.rglob("*"):
            zipfile.write(file, file.relative_to(root))

    shutil.rmtree(pack_name)
