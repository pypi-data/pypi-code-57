import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, List

import click
import yaml

from nomnomdata.engine.api import NominodeClient
from nomnomdata.engine.errors import MissingParameters, ValidationError
from nomnomdata.engine.test import NominodeMock

from ..logging import NominodeLogHandler
from .base import Connection, Help, ParameterGroup
from .encoders import ModelEncoder

python_type = type
logger = logging.getLogger(__name__)


class RepoType(str, Enum):
    AWS = "aws"

    def __str__(self):
        return self.value


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
    help: Help
    func: Callable

    @property
    def all_parameters(self):
        return {p.name: p for pg in self.parameter_groups.values() for p in pg.parameters}


class Icons:
    def __init__(self, one_x: Path, two_x: Path = None, three_x: Path = None):
        self.__dict__["1x"] = one_x
        if two_x:
            self.__dict__["2x"] = two_x
        if three_x:
            self.__dict__["3x"] = three_x


class Engine(Model):
    model_type = ModelType.ENGINE
    description: str
    alias: str
    image: str
    repo: str
    region: str
    repo_type: RepoType
    description: str
    categories: List[str]
    icons: Dict[str, Path]
    actions: Dict[str, Action]

    def __init__(
        self,
        uuid: str,
        alias: str,
        image: str,
        repo: str = "445607516549.dkr.ecr.us-east-1.amazonaws.com",
        region: str = "us-east-1",
        repo_type: RepoType = RepoType.AWS,
        description: str = "",
        categories: List[str] = None,
        icons: Icons = None,
    ):
        self.model = {
            "uuid": uuid,
            "alias": alias,
            "description": description,
            "location": {
                "image": image,
                "repo": repo,
                "region": region,
                "repo_type": str(repo_type),
            },
            "nnd_model_version": self.nnd_model_version,
            "categories": [{"name": val} for val in categories]
            if categories
            else [{"name": "General"}],
            "type": self.model_type.__str__(),
        }
        if icons:
            self.model["icons"] = icons.__dict__
        logger.debug(f"New Engine Registered '{uuid}'")
        self.actions = defaultdict(lambda: dict(parameters={}))
        super().__init__()

        @self.cli.command()
        def run():
            self.run()

        @self.cli.command()
        def dump_yaml():
            self.dump_yaml()

        @self.cli.command()
        @click.argument("action")
        @click.argument(
            "parameter_json_file", default="params.json", type=click.File("r")
        )
        def run_mock(action, parameter_json_file):
            self.run_mock(action, parameter_json_file)

    @staticmethod
    @click.group()
    def cli():
        pass

    def run(self):
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
        kwargs = self.finalize_kwargs(action.all_parameters, params)
        logger.debug(f"Calling Action {action.name}")
        if action.as_kwargs:
            return action.func(**kwargs)
        else:
            return action.func(kwargs)

    def run_mock(self, action, parameter_json_file):
        params = json.load(parameter_json_file)
        action: Action = self.actions[action]
        kwargs = self.finalize_kwargs(action.all_parameters, params)
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
            self.run()

    @staticmethod
    def check_missing(params, all_parameters, parent="."):
        missing_params = set([k for k, v in all_parameters.items() if v.required]) - set(
            params.keys()
        )
        if missing_params:
            for p in missing_params:
                logger.error(f"Missing Required Parameter {parent}:{p}")
            raise MissingParameters(f"{parent}:" + "+".join(missing_params))

    def finalize_kwargs(self, model_params, params, parent="."):
        kwargs = {}
        self.check_missing(params, model_params, parent)
        for keyword, val in params.items():
            parameter = model_params.get(keyword)
            if not parameter:
                logger.warning(f"\tUnknown parameter '{keyword}', discarding")
            elif isinstance(parameter.type, Connection):
                kwargs[keyword] = self.finalize_kwargs(
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

    def dump_yaml(self):
        full_model = self.model.copy()
        actions = {}
        for name, action in self.actions.items():
            safe_name = re.sub("[^\w]", "", action.name.lower())
            actions[safe_name] = {
                "display_name": action.display_name or action.name.capitalize(),
                "description": action.description,
            }
            if action.help:
                actions[safe_name]["help"] = action.help
            actions[safe_name]["parameters"] = [
                p for p in action.parameter_groups.values()
            ]
        full_model["actions"] = actions
        json_dump = json.dumps(full_model, indent=4, cls=ModelEncoder)
        with open("model.yaml", "w") as f:
            f.write(yaml.dump(json.loads(json_dump), sort_keys=False))

    def main(self):
        self.cli.main()

    def action(self, name, help: Help = None, description="", as_kwargs=False):
        def action_dec(func):
            logger.debug(f"Action '{name}'")
            for pg in func.parameter_groups.values():
                logger.debug(f"\tParameter Group {pg.name}")
                for p in pg.parameters:
                    logger.debug(f"\t\tParameter {p.name} {p.type}")

            self.actions[func.__name__] = Action(
                parameter_groups=func.parameter_groups,
                name=func.__name__,
                display_name=name,
                description=description,
                as_kwargs=as_kwargs,
                func=func,
                help=help,
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
            final_kwargs = self.finalize_kwargs(action.all_parameters, kwargs)
            if action.as_kwargs:
                return func(**final_kwargs)
            else:
                return func(final_kwargs)

    def parameter_group(
        self, parameter_group: ParameterGroup, name="", description="", alias=""
    ):
        def parameter_dec(func):
            params = getattr(func, "parameter_groups", {})
            parameter_group.name = name
            params[name] = parameter_group
            func.parameter_groups = params
            return func

        return parameter_dec
