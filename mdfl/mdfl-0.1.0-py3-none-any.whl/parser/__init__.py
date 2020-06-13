"""Parsing logic and grammar for MDFL."""

import shutil
from pathlib import Path
from typing import List, Tuple
from zipfile import ZipFile

from cookiecutter.main import cookiecutter

from lark import Lark, lark


__all__ = ['parser']


GRAMMAR = r"""
    start: namespace+

    namespace: "namespace" NAME "{" definition+ "}"

    definition: objective
              | function

    objective: "objective" NAME ";"
    function: "fun" NAME "{" instruction+ "}"

    instruction: objective
               | COMMENT
               | command

    command: COMMAND ";"

    COMMENT: /\/\/[^\n]+/
    COMMAND: /[^\/\n};]+/
    WHITESPACE: (" " | "\n")+

    %ignore COMMENT
    %ignore WHITESPACE
    %import common.CNAME -> NAME
"""

parser = Lark(GRAMMAR)


def enter_tree(tree: lark.Tree) -> Tuple[str, list]:
    """Return the name token and children of a tree."""
    name, subtree = tree.children
    return name, subtree.children


def create_pack(tree: lark.Tree, pack_name: str) -> None:
    """Create a data pack, given an AST."""
    namespaces: List[dict] = []
    pack = {
        "name": pack_name,
        "namespaces": namespaces,
        "description": input(f"Description of {pack_name}: ")
    }
    root = Path(pack_name)

    for subtree in tree.children:
        functions: List[dict] = []
        name, definitions = enter_tree(subtree)
        namespace = {
            "name": str(name),
            "functions": functions
        }
        namespaces.append(namespace)
        for definition in definitions:
            if definition.data == 'function':
                name, instructions = enter_tree(definition)
                commands = [
                    str(instruction.children[0])
                    for instruction in instructions
                ]
                functions.append({
                    "name": str(name),
                    "instructions": {
                        "commands": list(commands)
                    }
                })

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

    with ZipFile(f"{pack_name}.zip", "w") as zipfile:
        for file in root.rglob("*"):
            zipfile.write(file, file.relative_to(root))

    shutil.rmtree(pack_name)
