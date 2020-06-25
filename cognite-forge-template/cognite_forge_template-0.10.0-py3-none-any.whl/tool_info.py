from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Callable, List, Type

from forge_template.config_generator import FileType

if TYPE_CHECKING:
    from forge_template.handler.handler import BaseHandler


class SchemaInfo:
    def __init__(self, schema_path: Path, output_path: Path, post_transforms: List[Callable[[str, str], str]] = None):
        self.schema_path = schema_path
        self.output_path = output_path
        self.post_transforms = post_transforms


class ToolInfo:
    def __init__(
        self,
        name: str,
        handler: Type[BaseHandler],
        schema_info: List[SchemaInfo],
        github_actions_script_path: Path = None,
        github_actions_template_path: Path = None,
        assert_match: bool = False,
        assert_scope_match: bool = False,
        file_type: FileType = FileType.YAML,
        generate_all: bool = True,
    ):
        self.name = name
        self.handler = handler
        self.schema_info = schema_info
        self.github_actions_script_path = github_actions_script_path
        self.github_actions_template_path = github_actions_template_path
        self.assert_match = assert_match
        self.assert_scope_match = assert_scope_match
        self.file_type = file_type
        self.generate_all = generate_all
