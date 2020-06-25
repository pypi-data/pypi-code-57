import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Callable, Dict, List

import click
import yaml

from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.errors import MissingParameters, ValidationError
from nomnomdata.engine.test import NominodeMock

from ..logging import NominodeLogHandler
from .base import Connection, ParameterGroup

__all__ = ["ModelType", "Model", "Action", "Engine"]

python_type = type
logger = logging.getLogger(__name__)

_engine = None


@click.group(help="CLI interface to your engine")
def _cli():
    pass


@_cli.command(help="Run the engine, the expected entry point of an engine container")
def run():
    _engine._run()


@_cli.command(help="Dump the engine model.yaml file, ready for the model-update command")
def dump_yaml():
    _engine._dump_yaml()


@_cli.command(
    help="Run a specific engine action with a mocked out version of the nominode available"
)
@click.option(
    "--action",
    "-a",
    required=True,
    help="Specific action you want to run, matches the function name",
)
@click.option("-p", "--parameter_json", default="params.json", type=click.File("r"))
def run_mock(action, parameter_json):
    _engine._run_mock(action, parameter_json)


class ModelType(str, Enum):
    ENGINE = "engine"
    CONNECTION = "connection"
    SHARED_OBJECT = "shared_object"

    def __str__(self):
        return self.value


class Model:
    nnd_model_version = 2
    model_type: ModelType


@dataclass
class Action:
    name: str
    parameter_groups: List[ParameterGroup]
    display_name: str
    as_kwargs: bool
    description: str
    help: Dict
    func: Callable

    @property
    def all_parameters(self):
        return {p.name: p for pg in self.parameter_groups.values() for p in pg.parameters}


class Engine(Model):
    """
    The engine object represents the model that will be presented to the Nominode UI,
    it also implements parameter validation.

    :example:

    .. code-block:: python

        from nomnomdata.engine.components import Engine

        engine = Engine(
            uuid="ENGINE-1",
            alias="engine-1",
            description="Some cool engine that does interesting things",
            categories=["cool", "powerful", "expensive"],
            help_md_path="s3://help-md-bucket/coolengine/help.md",
            icons={
                "1x": "s3://icon-bucket/coolengine/coolengine-icon-256.png",
                "2x": "./some-local-dir/coolengine-icon-512.png",
                "3x": "../other-dir/coolengine-icon-1024.png"
            }
        )
        general_settings = ParameterGroup(
                Parameter(Integer(), name="Maximum"),
                Parameter(Integer(), name="Minimum"),
                display_name="General Settings"
            )

        @engine.action(display_name="Do Something")
        @engine.parameter_group(general_settings)
        def do_something(parameters):
            print(parameters)

        if __name__ == "__main__":
            engine.main()

    """

    model_type = ModelType.ENGINE

    def __init__(
        self,
        uuid: str,
        alias: str,
        description: str = "",
        categories: List[str] = None,
        help_header_id: str = None,
        help_md_path: str = None,
        icons: Dict[str, str] = None,
    ):
        if help_header_id and help_md_path:
            raise ValueError("Cannot use both help_header_id and help_md_path")

        self.uuid = uuid
        self.alias = alias
        self.description = description
        self.categories = (
            [{"name": val} for val in categories] if categories else [{"name": "General"}]
        )
        if help_header_id:
            self.help = {"header_id": help_header_id}
        elif help_md_path:
            self.help = {"file": help_md_path}
        else:
            self.help = None
        if icons:
            self.icons = {k: v for k, v in icons.items() if k in ["1x", "2x", "3x"]}
        else:
            self.icons = None
        self.actions = defaultdict(lambda: dict(parameters={}))

        super().__init__()

        global _engine
        _engine = self

        logger.debug(f"New Engine Registered '{uuid}'")

    def _run(self):
        root_logger = logging.getLogger("")
        root_logger.addHandler(NominodeLogHandler(level="DEBUG", sync=True))
        logger.info("Fetching task from nominode")
        client = NominodeClient()
        checkout = client.checkout_execution()
        params = checkout["parameters"]
        secrets = client.get_secrets()
        for secret_uuid in secrets:
            for pname, p in params.items():
                if isinstance(p, dict) and p.get("connection_uuid") == secret_uuid:
                    params[pname] = secrets[secret_uuid]
        logger.info(f"Action: {params['action_name']}")
        action = self.actions[params.pop("action_name")]
        kwargs = self._finalize_kwargs(action.all_parameters, params)
        logger.debug(f"Calling Action {action.name}")
        if action.as_kwargs:
            return action.func(**kwargs)
        else:
            return action.func(kwargs)

    def _run_mock(self, action, parameter_json_file):
        params = json.load(parameter_json_file)
        action: Action = self.actions[action]
        kwargs = self._finalize_kwargs(action.all_parameters, params)
        connections = {
            pname: p
            for pname, p in action.all_parameters.items()
            if isinstance(p.type, Connection)
        }
        kwargs["config"] = {}
        for i, conn in enumerate(connections):
            kwargs[conn] = {"connection_uuid": str(i)}
            kwargs["config"][i] = params[conn]
        kwargs["action_name"] = action.name
        with NominodeMock(kwargs):
            logger.info("Nominode Mock in place")
            root_logger = logging.getLogger("")
            root_logger.addHandler(NominodeLogHandler(level="DEBUG", sync=True))
            self._run()

    @staticmethod
    def _check_missing(params, all_parameters, parent="."):
        missing_params = set([k for k, v in all_parameters.items() if v.required]) - set(
            params.keys()
        )
        if missing_params:
            for p in missing_params:
                logger.error(f"Missing Required Parameter {parent}:{p}")
            raise MissingParameters(f"{parent}:" + "+".join(missing_params))

    def _finalize_kwargs(self, model_params, params, parent="."):
        kwargs = {}
        self._check_missing(params, model_params, parent)
        for keyword, val in params.items():
            parameter = model_params.get(keyword)
            if not parameter:
                logger.warning(f"\tUnknown parameter '{keyword}', discarding")
            elif isinstance(parameter.type, Connection):
                kwargs[keyword] = self._finalize_kwargs(
                    parameter.type.all_parameters, val, keyword
                )
            else:
                logger.debug(f"\tValidating {keyword}:'{val}' with {parameter.type}")
                try:
                    parameter.type.validate(val)
                except ValidationError:
                    logger.exception(f"\tParameter {parent}:{keyword} failed validation")
                    raise
                kwargs[keyword] = val
        return kwargs

    def _dump_yaml(self):
        from .encoders import ModelEncoder

        json_dump = json.dumps(self, indent=4, cls=ModelEncoder)
        with open("model.yaml", "w") as f:
            f.write(yaml.dump(json.loads(json_dump), sort_keys=False))

    def main(self):
        """
            Entry point for the engine, your program should call this for your engine to function.
            Blocking and will only return once specified command is complete.
        """
        _cli.main()

    def action(
        self,
        display_name: str,
        help_header_id: str = None,
        help_md_path: str = None,
        description="",
        as_kwargs=False,
    ) -> Callable:
        """
        Use as a decorator on a function to add an 'action' to your engine.

        :param display_name: Descriptive name that will be displayed in the UI
        :param help_header_id:
            The header ID to scroll to in any parent MD files that are declared,
            cannot be used if help_md_path is not None.
        :param help_md_path:
            A file path or URI to the location of an MD file to use as the help,
            cannot be used if help_header_id is not None.
        :param description: The long form description of what this engine done.
        :param as_kwargs:
            Will cause parameters to be passed to the wrapped function as kwargs instead of args,
            defaults to False
        :example:

        .. code-block:: python

            # note this example is not functional
            # as we do not declared any parameter_groups yet
            @engine.action(
                display_name="Do Something",
                help_header_id="Do Something",
                description="This action does something very helpful",
            )
            def my_cool_engine_action(parameters):
                print(parameters)
        """
        if help_header_id and help_md_path:
            raise ValueError("Cannot use both help_header_id and help_md_path")

        def action_dec(func):
            logger.debug(f"Action '{display_name}'")
            for pg in func.parameter_groups.values():
                logger.debug(f"\tParameter Group {pg.name}")
                for p in pg.parameters:
                    logger.debug(f"\t\tParameter {p.name} {p.type}")
            if help_header_id:
                helpdict = {"header_id": help_header_id}
            elif help_md_path:
                helpdict = {"file": help_md_path}
            else:
                helpdict = None
            self.actions[func.__name__] = Action(
                parameter_groups=func.parameter_groups,
                name=func.__name__,
                display_name=display_name,
                description=description,
                as_kwargs=as_kwargs,
                func=func,
                help=helpdict,
            )

            @wraps(func)
            def call(*args, **kwargs):
                return self.__call__action__(func, *args, **kwargs)

            return call

        return action_dec

    def __call__action__(self, func, *args, **kwargs):

        with NominodeMock({}):
            root_logger = logging.getLogger("")
            root_logger.addHandler(NominodeLogHandler(level="DEBUG", sync=True))
            action = self.actions[func.__name__]
            logger.debug(f"Action Called '{action.display_name}'")
            final_kwargs = self._finalize_kwargs(action.all_parameters, kwargs)
            if action.as_kwargs:
                return func(**final_kwargs)
            else:
                return func(final_kwargs)

    def parameter_group(
        self,
        parameter_group: ParameterGroup,
        name=None,
        display_name=None,
        description=None,
        collapsed=None,
    ) -> Callable:
        """Decorate your action with this have it accept groups of parameters

        :param parameter_group: Instantiated :class:`~nomnomdata.engine.components.ParameterGroup` class
        :param name: Override parameter group name
        :param display_name: Override display name
        :param description: Override discription
        :param collapsed: Override collapsed status


        :example:
        .. code-block:: python

            general_settings = ParameterGroup(
                Parameter(Integer(), name="Maximum"),
                Parameter(Integer(), name="Minimum"),
                display_name="General Settings"
            )

            @engine.action(display_name="Do Something")
            @engine.parameter_group(general_settings)
            def do_something(parameters):
                print(parameters)

        """

        def parameter_dec(func):
            params = getattr(func, "parameter_groups", {})
            if name:
                parameter_group.name = name
            if display_name:
                parameter_group.display_name = display_name
            if description:
                parameter_group.description = description
            if collapsed is not None:
                parameter_group.collapsed = collapsed
            params[parameter_group.name] = parameter_group
            func.parameter_groups = params
            return func

        return parameter_dec
