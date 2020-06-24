from collections import namedtuple
import importlib
import importlib.util
import importlib.machinery
import json
from pathlib import Path
import sys
from typing import Dict, Optional, Union

from starlette.requests import Request
from starlette.responses import Response

from spell.serving import BasePredictor
from spell.serving.exceptions import InvalidPredictor
from spell.serving.types import APIResponse, PredictorClass

ModelInfo = namedtuple("ModelInfo", ["name", "version"])
# Set the default value of fields to None. I wish we could use dataclasses
ModelInfo.__new__.__defaults__ = (None,) * len(ModelInfo._fields)


class API:
    FILE_IMPORT_NAME = "spell_predictor"

    def __init__(self, predictor_class: PredictorClass) -> None:
        self.predictor_class = predictor_class
        self.predictor = None
        self.predict_arg_generator = None
        self.health_arg_generator = None

    @classmethod
    def from_file(cls, path: Path, classname: Optional[str] = None):
        spec = importlib.util.spec_from_file_location(cls.FILE_IMPORT_NAME, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[cls.FILE_IMPORT_NAME] = module
        spec.loader.exec_module(module)
        return cls.create_cls(classname)

    @classmethod
    def from_module(
        cls,
        module_path: Union[Path, str],
        python_path: Union[Path, str],
        classname: Optional[str] = None,
    ):
        # module_path is the path in the filesystem to the module
        # python_path is the python path to the predictor in the form path.to.module
        cls.validate_python_path(python_path)
        sys.path.append(str(module_path))  # Path objects can't be used here
        importlib.import_module(python_path)
        return cls.create_cls(classname)

    @classmethod
    def create_cls(cls, classname: Optional[str]):
        predictor_class = cls.get_predictor_class(classname)
        predictor_class.validate()
        return cls(predictor_class)

    @classmethod
    def get_predictor_class(cls, classname: Optional[str]) -> PredictorClass:
        predictors = {p.__name__: p for p in BasePredictor.__subclasses__()}
        if not predictors:
            raise InvalidPredictor(
                "No predictors found. Make sure your predictors extend BasePredictor."
            )
        if not classname:
            if len(predictors) > 1:
                raise InvalidPredictor(
                    "More than one predictor found, but no classname was specified."
                )
            predictor_name = next(iter(predictors))
            return predictors[predictor_name]
        try:
            return predictors[classname]
        except KeyError:
            raise InvalidPredictor(
                f"No predictor named {classname} was found. The predictors found were ({', '.join(predictors)})"
            )

    @staticmethod
    def validate_python_path(python_path: str):
        split_python_path = python_path.split(".")
        if split_python_path[0] == "spell":
            raise InvalidPredictor('Top-level module for predictor cannot be named "spell"')
        invalid_path_identifier = next(
            (identifier for identifier in split_python_path if not identifier.isidentifier()), None
        )
        if invalid_path_identifier:
            raise InvalidPredictor(f"Invalid python path element {invalid_path_identifier}")

    def initialize_predictor(self, config: Dict) -> None:
        model_info = config.pop("model_info", {})
        self.predictor = self.predictor_class(config)
        if not hasattr(self.predictor, "model_info"):
            self.predictor.model_info = ModelInfo(**model_info)
        self.predict_arg_generator = self.predictor.get_predict_argument_generator()
        self.health_arg_generator = self.predictor.get_health_argument_generator()

    async def predict(self, request: Request) -> APIResponse:
        # TODO(justin) BentoML-style hooks go here
        try:
            json_content = await request.json()
        except json.JSONDecodeError:
            return Response("Request must contain a JSON object", status_code=400), None
        kwargs, tasks = self.predict_arg_generator(request)
        return self.predictor.predict(json_content, **kwargs), tasks

    async def health(self, request: Request) -> APIResponse:
        kwargs, tasks = self.health_arg_generator(request)
        return self.predictor.health(**kwargs), tasks
