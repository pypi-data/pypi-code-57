import os
import re
from abc import ABCMeta, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import lightgbm
import xgboost

from sktmls.model_registry import ModelRegistry


MLS_MODEL_DIR = os.path.join(Path.home(), "mls_temp_dir")
MODEL_BINARY_NAME = "model.joblib"
MODEL_META_NAME = "model.json"
BUCKET = "mls-model-registry"

EDD_OPTIONS = """-Dfs.s3a.proxy.host=awsproxy.datalake.net \
                 -Dfs.s3a.proxy.port=3128 \
                 -Dfs.s3a.endpoint=s3.ap-northeast-2.amazonaws.com \
                 -Dfs.s3a.security.credential.provider.path=jceks:///user/tairflow/s3_mls.jceks \
                 -Dfs.s3a.fast.upload=true -Dfs.s3a.acl.default=BucketOwnerFullControl"""


class AWSENV(Enum):
    STG = "stg"
    PRD = "prd"
    DEV = "dev"


class MLSModelError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MLSModel(metaclass=ABCMeta):
    def __init__(self, model_name: str, model_version: str):
        assert type(model_name) == str
        assert type(model_version) == str

        if not bool(re.search("^[A-Za-z0-9_]+_model$", model_name)):
            raise MLSModelError(
                "model_name should follow naming rule. MUST be in alphabet, number, underscore and endwiths '_model'"
            )

        if not bool(re.search("^[A-Za-z0-9_]+$", model_version)):
            raise MLSModelError("model_name should follow naming rule. MUST be in alphabet, number, underscore")

        self.model_name = model_name
        self.model_version = model_version

    def save(self, aws_env: str = AWSENV.STG.value, training_env: str = "ye", force: bool = False) -> None:
        """
        Upload model_binary (model.joblib) and model_meta (model.json) to MLS model registry.

        Args:
            aws_env (str): AWS ENV
            training_env (str): Your ENV (ye or edd)
            force (bool): Force to overwrite model files on S3 if exists
        """
        model_registry = ModelRegistry(aws_env, training_env)
        model_registry.save(self, force)

    @abstractmethod
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        pass


class MLSLightGBMModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str, features: List[str] = None):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "lightgbm"
        self.model_lib_version = lightgbm.__version__

        if not features:
            self.features = self.model.feature_name()
        else:
            if len(features) < len(self.model.feature_name()):
                raise MLSModelError(
                    "The number of input features should be greater or equal to the number of features used on ML Model"
                )
            else:
                self.features = features


class MLSXGBoostModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "xgboost"
        self.model_lib_version = xgboost.__version__

        try:
            if (
                all(isinstance(s, str) for s in features)
                and len(features) >= len(self.model.feature_importances_)
                and type(features) == list
            ):
                self.features = features
            else:
                raise MLSModelError(
                    "Input feature list shold have more(or equal) to the number of model input feature or list STRING type"
                )
        except MLSModelError as e:
            print("MLSModelError", e)


class MLSRuleModel(MLSModel):
    def __init__(self, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model_lib = "rule"
        self.model_lib_version = "N/A"

        if features:
            self.features = features
        else:
            raise MLSModelError("No feature provided")
