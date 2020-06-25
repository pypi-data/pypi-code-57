import json
import os
from typing import Callable, Dict, Optional, Tuple

import torch

from ..training.metrics import Metric

MODEL_PARAMETERS_FILE_NAME = "model_parameters.json"


class ModelParameters:
    TYPE_PARAMETER = "type"

    def __init__(
        self,
        transformer_model_name: str,
        head_dropout: float,
        loss: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        metrics: Optional[Dict[str, Metric]] = None,
        torchscript: bool = False,
    ) -> None:
        self.transformer_model_name = transformer_model_name
        self.head_dropout = head_dropout
        self.metrics = metrics
        self.loss = loss
        self.torchscript = torchscript

        self._init_parameters = {
            "head_dropout": head_dropout,
            "transformer_model_name": transformer_model_name,
        }

    def _to_json_file(self, json_file_path: str) -> None:
        with open(json_file_path, "w", encoding="utf-8") as writer:
            writer.write(self._to_json_string())

    def _to_json_string(self) -> str:
        return json.dumps(self._init_parameters, indent=2, sort_keys=True) + "\n"

    def save(self, save_directory: str, model_type: Optional[str] = None) -> None:
        if model_type is not None:
            self._init_parameters[self.TYPE_PARAMETER] = model_type
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        output_config_file = os.path.join(save_directory, MODEL_PARAMETERS_FILE_NAME)
        self._to_json_file(output_config_file)

    @classmethod
    def load(cls, path: str) -> Tuple["ModelParameters", Optional[str]]:
        with open(os.path.join(path, MODEL_PARAMETERS_FILE_NAME), "r", encoding="utf-8") as reader:
            text = reader.read()
        model_parameters = json.loads(text)
        model_type = model_parameters.pop(cls.TYPE_PARAMETER, None)
        return cls(**model_parameters), model_type
