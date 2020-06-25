import logging
from typing import Callable, Dict

import click
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

from forge_template.config_generator import ConfigGenerator
from forge_template.constants import Tools
from forge_template.exception.exceptions import AccessDeniedException, ValidationException
from forge_template.exception.handler import (
    handle_access_denied_error,
    handle_file_not_found,
    handle_parser_error,
    handle_validation_error,
)
from forge_template.handler.handler import BaseHandler
from forge_template.tool_info import ToolInfo
from forge_template.user_interface import UserInterface
from forge_template.util.dict_util import assert_same_keys, assert_scope_matches, merge_dictionaries
from forge_template.util.file_util import load_and_validate_yaml


def _instantiate_config(tool_info: ToolInfo) -> Dict:
    configs = {}
    for info in tool_info.schema_info:
        configs[info.output_path] = load_and_validate_yaml(info.output_path, info.schema_path)

    if tool_info.assert_match:
        assert_same_keys(configs)

    if tool_info.assert_scope_match:
        assert_scope_matches(configs)

    merged = merge_dictionaries(list(configs.values()))

    return merged


def _instantiate_handler(tool_info: ToolInfo) -> BaseHandler:
    config = _instantiate_config(tool_info)
    return tool_info.handler(config, tool_info)


def generate(tool_info: ToolInfo) -> str:
    def action():
        is_custom = click.confirm(
            f"Do you want to do a custom configuration of {tool_info.name} (only recommended in very special cases)?",
            default=False,
            show_default=True,
        )

        generator = ConfigGenerator(file_type=tool_info.file_type)
        for schema_info in tool_info.schema_info:
            if tool_info.generate_all or click.confirm(f"Do you want to generate {schema_info.output_path}?"):
                generator.set_schema_info(
                    output_path=schema_info.output_path,
                    schema_path=schema_info.schema_path,
                    key=tool_info.name,
                    post_transforms=schema_info.post_transforms,
                )
                UserInterface.print_ok(f"\nGenerating {schema_info.output_path}")
                generator.generate(is_custom=is_custom)
                generator.preview()
                logging.info("\n")
                if click.confirm("Do you want to save the preview?"):
                    generator.save()
                else:
                    return

    do_action(action)
    return UserInterface.RETURN


def deploy(tool_info: ToolInfo) -> str:
    def action():
        handler = _instantiate_handler(tool_info)
        handler.run_create_preview()
        handler.run_print_preview()
        if click.confirm("Do you want to proceed?", default=False):
            handler.run_setup()
            UserInterface.print_ok(f"Successfully deployed {tool_info.name}")

    do_action(action)
    return UserInterface.RETURN


def delete(tool_info: ToolInfo) -> str:
    def action():
        handler = _instantiate_handler(tool_info)
        handler.run_delete_all_resources()
        UserInterface.print_ok(f"Successfully deleted {tool_info.name}")

    do_action(action)
    return UserInterface.RETURN


def upload_config() -> None:
    def action():
        handler = Tools.DATABRICKS.handler(_instantiate_config(Tools.DATABRICKS), Tools.DATABRICKS)
        handler.upload_config()

    do_action(action)


def do_action(action: Callable[[], None]) -> None:
    try:
        action()
    except FileNotFoundError as e:
        handle_file_not_found(e)
    except (ParserError, ScannerError) as e:
        handle_parser_error(e)
    except ValidationException as e:
        handle_validation_error(e)
    except AccessDeniedException as e:
        handle_access_denied_error(e)
