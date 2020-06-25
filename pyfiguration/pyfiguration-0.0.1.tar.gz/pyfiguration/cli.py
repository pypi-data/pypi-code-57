from __future__ import annotations

import os
import io
import re
import yaml
import click
import operator
import importlib.util

from .configuration import Configuration
from functools import reduce
from typing import List, Dict
from importlib.abc import Loader


def printDefinition(definition: dict, indent: int = 0):
    """ Helper method for printing a defintion in a nice way.

    Args:
        definition: The definition to display
        indent: The number of spaces to use for indentation
    """

    # Create a buffer to hold the YAML output (the YAML library can only write to file)
    buffer = io.StringIO()

    # Dump the definition as YAML in the buffer and convert back to text
    yaml.dump(definition, buffer)
    definitionYAML = buffer.getvalue()

    # Replace Python classes with their name (e.g. str, int, list, float, ...)
    definitionYAML = re.sub(r"!!python\/name:builtins\.(\w+).+", r"\1", definitionYAML)

    # Show the output
    click.echo(definitionYAML)


def printDebug(context: click.Context, message: str):
    if context.obj["DEBUG"]:
        click.echo(click.style(f"🠊 {message}", fg="blue"))


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(context: click.Context, debug: bool = False):
    """ PyFiguration commandline tool

    Use this commandline tool to inspect scripts and have a look at the
    configuration options that the script provides. Furthermore you can
    inspect configuration files directly.
    """

    # Create the context for all commands
    context.ensure_object(dict)

    # Set the debug mode
    context.obj["DEBUG"] = debug

    # Show info if we're in debug mode
    printDebug(context, "Debug mode is enabled")


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
@click.argument("module", type=click.Path(exists=True))
def module(context: click.Context, module: str):
    """ Inspect a module

    Provide a file or module to inspect it with PyFiguration. This command
    will load the script from file and inspect the PyFiguration decorators
    to find out what the configuration options are. Then, it will display all
    the option as the output of this command.

    MODULE is the filename of the module to inspect with PyFiguraton
    """

    # Extract the module name from the file
    printDebug(context, f"Start inspection of file '{module}'")
    moduleName = os.path.splitext(os.path.split(module)[-1])[0]

    # Load the module from file
    spec = importlib.util.spec_from_file_location(moduleName, module)
    importedModule = importlib.util.module_from_spec(spec)
    if isinstance(spec.loader, Loader):
        spec.loader.exec_module(importedModule)

    # Get the configuration from the module
    conf = getattr(importedModule, "conf")
    printDebug(context, f"Loaded the configuration from the module")

    click.echo(
        f"The following options can be used in a configuration file for the module '{module}':"
    )
    printDefinition(conf.configuration.getDefinition())


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
@click.argument("module", type=click.Path(exists=True))
def config(context: click.Context, module: str):
    """ Inspect a configuration file

    This command will load the MODULE and look at the defintion. Then
    it will load the CONFIGFILE and makes sure the CONFIGFILE is valid
    for the provided MODULE.

    MODULE is the filename of the module to inspect with PyFiguraton
    CONFIGFILE is the configuration file to inspect, against the MODULE
    """

    # Extract the module name from the file
    printDebug(context, f"Start inspection of file '{module}'")
    moduleName = os.path.splitext(os.path.split(module)[-1])[0]

    # Load the module from file
    os.environ["CLI"] = "TRUE"
    spec = importlib.util.spec_from_file_location(moduleName, module)
    importedModule = importlib.util.module_from_spec(spec)
    if isinstance(spec.loader, Loader):
        spec.loader.exec_module(importedModule)

    # Get the configuration from the module
    conf = getattr(importedModule, "conf")
    printDebug(context, f"Loaded the configuration from the module")

    # Set the configfile explicitly on the configuration of the module
    conf.set_configuration()

    # Access all keys to check if they're valid
    def checkConfig(configuration: Configuration, definition: dict, parents: List[str] = []):
        """
        """
        errors: List[str] = []
        warnings: List[str] = []
        for key in configuration.keys():

            # Set the value to a default value (None = not set)
            value = None

            # Access the configuration (triggers the checks as well)
            try:
                value = configuration[key]
            except Warning as w:
                warnings.append(str(w))
            except Exception as e:
                errors.append(str(e))

            # Make sure it exists
            try:
                definitionForKey = reduce(operator.getitem, parents, definition)
                assert definitionForKey[key] != {}
            except Warning as w:
                warnings.append(str(w))
            except AssertionError as e:
                warnings.append(
                    f"Key '{'.'.join([*parents, key])}' doesn't exist in the definition and is not used in the module."
                )
            except Exception as e:
                errors.append(str(e))

            # Recursion
            if isinstance(value, Configuration):
                nestedErrors, nestedWarnings = checkConfig(
                    value, definition, parents=parents + [key]
                )
                errors += nestedErrors
                warnings += nestedWarnings

        # Return the errors and warnings
        return errors, warnings

    def checkDefinition(configuration: dict, definition: dict, parents: List[str] = []):
        """
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Check from the definition
        for key, value in definition.items():

            # Make sure all required fields are in the configuration
            try:
                if (
                    isinstance(value, dict)
                    and "required" in value
                    and value["required"]
                ):
                    configurationForKey = reduce(
                        operator.getitem, parents, configuration
                    )
                    configurationForKey[key]
            except Warning as w:
                warnings.append(str(w))
            except Exception as e:
                errors.append(str(e))

            # Recursion
            if isinstance(value, dict):
                nestedErrors, nestedWarnings = checkDefinition(
                    configuration, value, parents=parents + [key]
                )
                errors += nestedErrors
                warnings += nestedWarnings

        return errors, warnings

    # Trigger the checks
    configErrors, configWarnings = checkConfig(
        configuration=conf.configuration, definition=conf.configuration.getDefinition()
    )
    definitionErrors, definitionWarnings = checkDefinition(
        configuration=conf.configuration, definition=conf.configuration.getDefinition()
    )

    # Make sure to show each error/warning only once
    errors = set([e for e in configErrors + definitionErrors])
    warnings = set([w for w in configWarnings + definitionWarnings])

    # Show the found warnings and errors
    if len(errors) > 0:
        click.echo(click.style("--------\n Errors \n--------"))
    for error in errors:
        click.echo(click.style(f"   ✗ {error}", fg="red"))
    if len(warnings) > 0:
        click.echo(click.style("----------\n Warnings \n----------"))
    for warning in warnings:
        click.echo(click.style(f"   ! {warning}", fg="yellow"))
