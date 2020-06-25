import base64
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import toml
from cerberus import Validator
from ruamel.yaml import YAML, sys

from forge_template.exception.exceptions import ValidationException


def copy_tree_and_replace_placeholders(src_dest_pairs: List[Tuple[Path, Path]], placeholder: str, replacement: str):
    for src, dest in src_dest_pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = src.open("r").read()
        content = content.replace(placeholder, replacement)
        dest.open("w").write(content)


def get_rel_folder_paths(path: Path) -> List[Path]:
    return [d.relative_to(path) for d in path.rglob("**/*") if d.is_dir()]


def get_base64_encoded_content(path: Path) -> str:
    content = path.open("rb").read()
    return base64.b64encode(content).decode()


def load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe")
    dct = yaml.load(path.open("r", encoding="utf-8"))
    assert isinstance(dct, dict), f"YAML malformatted, couldn't load into dict (got {type(dct)})"
    return dct


def load_toml(path: Path) -> Dict:
    dct = toml.load(path.open(encoding="utf-8"))
    assert isinstance(dct, Dict), f"TOML malformatted, coldn't load into dict (got {type(dct)}"
    return dct


def save_yaml(path: Path, content: Dict) -> None:
    yaml = YAML(typ="safe")
    yaml.indent(sequence=4, offset=2)
    yaml.dump(content, path.open("w"))


def save_toml(path: Path, content: Dict) -> None:
    toml.dump(content, path.open("w"))


def dump_yaml_to_stdout(content: Any) -> None:
    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.dump(content, sys.stdout)


def dump_toml_to_stdout(content: Dict) -> None:
    print(toml.dumps(content))


def validate_yaml(schema_path: Path, document: Dict) -> Tuple[bool, Optional[Dict]]:
    schema = load_yaml(schema_path)
    validator = Validator(schema)
    return validator.validate(document), validator.errors or None


def load_and_validate_yaml(path: Path, schema_path: Path) -> Dict:
    loaded_yaml = load_yaml(path)
    is_valid, errors = validate_yaml(schema_path, loaded_yaml)
    if not is_valid:
        raise ValidationException(f"Validation of {path} failed.\n{errors}")
    return loaded_yaml


def read_file(path: Path) -> str:
    return path.open("r").read()


def write_file(path: Path, content: str) -> None:
    path.open("w").write(content)


def create_directory(path: Path, *, exist_ok: bool = False, parents: bool = False) -> None:
    path.mkdir(exist_ok=exist_ok, parents=parents)


def copy_file(path: Path, destination: Path) -> None:
    shutil.copy(str(path), str(destination))


def delete_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()
