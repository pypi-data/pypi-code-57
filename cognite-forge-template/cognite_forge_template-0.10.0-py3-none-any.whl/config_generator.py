from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

from cerberus import Validator

from forge_template.user_interface import UserInterface
from forge_template.util.dict_util import merge_dictionaries
from forge_template.util.file_util import (
    dump_toml_to_stdout,
    dump_yaml_to_stdout,
    load_toml,
    load_yaml,
    save_toml,
    save_yaml,
)


class FileType(Enum):
    TOML = "toml"
    YAML = "yaml"


class ConfigGenerator:
    def __init__(self, file_type: FileType = FileType.YAML):
        self.ui = UserInterface()
        self.file_type = file_type
        self.config_schema: Dict[str, Any] = {}
        self.output_path: Union[Path, None] = None
        self.config: Dict[str, Any] = {}
        self.key = ""
        self.post_transforms: List[Callable[[str, str], str]] = []
        self.project_name = ""

    def set_schema_info(
        self, *, output_path: Path, schema_path: Path, key: str, post_transforms: List[Callable[[str, str], str]]
    ):
        self.config_schema = load_yaml(schema_path)
        self.output_path = output_path
        self.key = key
        self.post_transforms = post_transforms
        self.config = {}

        if self.file_type == FileType.YAML:
            self.config = load_yaml(output_path) if output_path.exists() else {}
        elif self.file_type == FileType.TOML:
            self.config = load_toml(output_path) if output_path.exists() else {}

    def generate(self, is_custom: bool = False) -> None:
        self.config = self._generate_config(self.key, self.config_schema[self.key], is_custom=is_custom)
        for transform in self.post_transforms:
            self._perform_post_transform(transform, self.config[self.key])

    def preview(self) -> None:
        print()
        self.ui.print_ok(f"Preview: {Path(str(self.output_path)).name}")
        if self.file_type == FileType.YAML:
            dump_yaml_to_stdout(self.config)
        elif self.file_type == FileType.TOML:
            dump_toml_to_stdout(self.config)

    def save(self) -> None:
        print()
        if self.file_type == FileType.YAML:
            save_yaml(Path(str(self.output_path)), self.config)
            self.ui.print_ok(f"Saved {self.output_path}")
        elif self.file_type == FileType.TOML:
            save_toml(Path(str(self.output_path)), self.config)
            self.ui.print_ok(f"Saved {self.output_path}")

    def _generate_config(self, key: str, schema: Dict[str, Any], is_custom: bool = False) -> Dict[str, Any]:
        config = {}
        if type(schema) is dict:
            if schema["type"] == "dict":
                config[key] = merge_dictionaries(
                    [self._generate_config(k, s, is_custom) for k, s in schema["schema"].items()]
                )

            elif schema["type"] == "list" and schema["schema"]["type"] == "dict":
                return {key: self._get_input_list_of_dict(schema)}
            else:
                default = self._get_default_value(schema)
                if not is_custom and default:
                    return {key: default}
                else:
                    transform = self._get_transformer(schema)
                    value = transform(self._get_input(schema, key, default, transform))
                    if key == "project_name":
                        self.project_name = value
                    return {key: value}

        return config

    def _get_input_list_of_dict(self, schema):
        return self.ui.get_input_list_of_dicts(
            prompt=schema["meta"]["prompt"],
            validators=self._get_validators_for_list_of_dicts(schema["schema"]["schema"]),
            keys=list(dict(schema["schema"]["schema"]).keys()),
        )

    def _get_input(self, schema: Dict, key: str, default: str, transform: Callable[[str], Any]) -> str:
        return self.ui.get_input(
            prompt=schema["meta"]["prompt"], default=default, validate=self._get_validator(key, schema, transform)
        )

    def _get_validators_for_list_of_dicts(self, schema: Dict[str, Any]) -> Dict[str, Callable[[str], bool]]:
        validators = {}
        for key in schema:
            validators[key] = self._get_validator(key, schema[key])

        return validators

    def _get_validator(
        self, key: str, schema: Dict[str, Any], transform: Callable[[str], Any] = None
    ) -> Callable[[str], bool]:
        v = Validator({key: schema})
        ui = self.ui

        def validator(input_value: str) -> bool:
            if transform:
                input_value = transform(input_value)
            is_valid = v.validate({key: input_value})
            if not is_valid:
                ui.print_warning(f"Error message: {v.errors}")
                if "meta" in schema and "help" in schema["meta"]:
                    ui.print_warning(f"Explanation: {schema['meta']['help']}")
            return is_valid

        return validator

    @staticmethod
    def _get_transformer(schema: Dict[str, Any]) -> Callable[[str], Any]:
        def transform_list(input_value: str) -> List[str]:
            if input_value:
                return list(map(lambda x: x.strip(), input_value.split(",")))
            return []

        def base_transform(input_value: str) -> str:
            if input_value:
                return input_value.strip()
            return ""

        if schema["type"] == "list":
            return transform_list
        else:
            return base_transform

    @staticmethod
    def _get_default_value(schema: Dict[str, Any]) -> str:
        return schema["default"] if "default" in schema else ""

    def _perform_post_transform(self, transform: Callable[[str, str], str], config: Dict) -> None:
        for k, v in config.items():
            if type(v) is dict:
                self._perform_post_transform(transform, v)
            elif type(v) is str:
                config[k] = transform(v, self.project_name)
