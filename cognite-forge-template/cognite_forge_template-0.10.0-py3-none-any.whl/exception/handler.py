from ruamel.yaml.parser import ParserError

from forge_template.exception.exceptions import AccessDeniedException, ValidationException
from forge_template.paths import YAML_CONFIG_PATH, YAML_SECRETS_PATH
from forge_template.user_interface import UserInterface


def handle_file_not_found(e: FileNotFoundError) -> None:
    if e.filename == YAML_CONFIG_PATH or e.filename == YAML_SECRETS_PATH:
        UserInterface.print_failure(f"\nConfiguration file named {e.filename} not found. Please generate config.")
    else:
        raise e


def handle_parser_error(e: ParserError) -> None:
    UserInterface.print_failure(f"\n{str(e)}\nPlease verify that the content of your .yaml files is parseable")


def handle_validation_error(e: ValidationException) -> None:
    UserInterface.print_failure(f"\n{str(e)}")


def handle_access_denied_error(e: AccessDeniedException) -> None:
    UserInterface.print_failure(f"\n{str(e)}")
