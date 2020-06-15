import json
import os
import shlex
import shutil
import subprocess
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, TYPE_CHECKING

import boto3
import joblib

if TYPE_CHECKING:
    from sktmls.models.mls_model import MLSModel

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


class ModelRegistryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelRegistry:
    def __init__(self, aws_env: str = "stg", training_env: str = "ye"):
        """
        Init ModelRegistry instance

        Args:
            aws_env (str): AWS ENV
            training_env (str): Your ENV (ye or edd)
        """
        self.aws_env = aws_env
        self.training_env = training_env

        self.edd_options = EDD_OPTIONS if self.training_env == "edd" else ""

    def save(self, mls_model: "MLSModel", force: bool = False) -> None:
        """
        Upload model_binary (model.joblib) and model_meta (model.json) to MLS model registry.
        Equivalent to MLSModel.save method.

        Args:
            mls_model (MLSModel): Model instance declared with class inheriting MLSModel
            force (bool): Force to overwrite model files on S3 if exists
        """
        if self.training_env == "local" and self.aws_env != AWSENV.DEV.value:
            raise ModelRegistryError("On local mode, aws_env should be 'dev'")

        s3_path = BUCKET
        if self.aws_env in (AWSENV.STG.value, AWSENV.PRD.value):
            s3_path = f"{BUCKET}-{self.aws_env}"
        s3_path = f"{s3_path}/{mls_model.model_name}/{mls_model.model_version}"

        model_meta = {
            "name": mls_model.model_name,
            "version": mls_model.model_version,
            "model_lib": mls_model.model_lib,
            "model_lib_version": mls_model.model_lib_version,
            "model_data": f"s3://{s3_path}/{MODEL_BINARY_NAME}",
            "features": mls_model.features,
        }

        model_path = os.path.join(
            MLS_MODEL_DIR,
            f"{self.aws_env}_{mls_model.model_name}_{mls_model.model_version}_{datetime.today().strftime('%Y%m%d_%H%M%S')}",
        )
        model_binary_path = os.path.join(model_path, MODEL_BINARY_NAME)
        model_meta_path = os.path.join(model_path, MODEL_META_NAME)

        try:
            if not os.path.exists(model_binary_path):
                if not os.path.exists(model_path):
                    os.makedirs(model_path)
                joblib.dump(mls_model, model_binary_path)
                with open(model_meta_path, "w") as f:
                    json.dump(model_meta, f)
            else:
                raise ModelRegistryError(
                    f"{mls_model.model_name} / {mls_model.model_version} is already in PATH ({model_path})"
                )

            if self.training_env != "local":
                force_option = "-f" if force else ""

                process_mkdir = subprocess.Popen(
                    shlex.split(f"hdfs dfs {self.edd_options} -mkdir -p s3a://{s3_path}"),
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                process_mkdir.wait()
                if process_mkdir.returncode != 0:
                    raise ModelRegistryError(f"Making Directory on S3 ({s3_path}) is FAILED")

                process_model_binary = subprocess.Popen(
                    shlex.split(f"hdfs dfs {self.edd_options} -put {force_option} {model_binary_path} s3a://{s3_path}"),
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                process_model_binary.wait()
                if process_model_binary.returncode != 0:
                    raise ModelRegistryError(f"Loading model_binary(model.joblib) to S3 ({s3_path}) is FAILED.")

                process_model_meta = subprocess.Popen(
                    shlex.split(f"hdfs dfs {self.edd_options} -put {force_option} {model_meta_path} s3a://{s3_path}"),
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
                process_model_meta.wait()
                if process_model_meta.returncode != 0:
                    raise ModelRegistryError(f"Loading model_meta(meta.json) to S3 ({s3_path}) is FAILED")
            else:
                client = boto3.client("s3")
                if not force and client.list_objects_v2(
                    Bucket=BUCKET, Prefix=f"{mls_model.model_name}/{mls_model.model_version}"
                ).get("Contents"):
                    raise ModelRegistryError(f"S3 path ('s3://{s3_path}') already exists")

                client.upload_file(
                    Filename=model_binary_path,
                    Bucket=BUCKET,
                    Key=f"{mls_model.model_name}/{mls_model.model_version}/{MODEL_BINARY_NAME}",
                )
                client.upload_file(
                    Filename=model_meta_path,
                    Bucket=BUCKET,
                    Key=f"{mls_model.model_name}/{mls_model.model_version}/{MODEL_META_NAME}",
                )
        except ModelRegistryError as e:
            print("ModelRegistryError", e)
        finally:
            shutil.rmtree(model_path, ignore_errors=True)

    def list_models(self) -> List[str]:
        """
        List all registered models in model registry.
        """
        s3_path = BUCKET
        if self.aws_env in (AWSENV.STG.value, AWSENV.PRD.value):
            s3_path = f"{BUCKET}-{self.aws_env}"

        try:
            s3_path = f"s3a://{s3_path}/"
            process = subprocess.Popen(
                shlex.split(f"hdfs dfs {self.edd_options} -ls {s3_path}"), stdout=subprocess.PIPE, stdin=subprocess.PIPE
            )
            process.wait()
            if process.returncode != 0:
                raise ModelRegistryError(f"Listing models in ({s3_path}) is FAILED.")

            output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
            return output
        except ModelRegistryError as e:
            print("ModelRegistryError", e)

    def list_versions(self, model_name: str):
        """
        List all registered model versions for a model

        Args:
            model_name (str): Model name
        """
        s3_path = BUCKET
        if self.aws_env in (AWSENV.STG.value, AWSENV.PRD.value):
            s3_path = f"{BUCKET}-{self.aws_env}"
        s3_path = f"s3a://{s3_path}/{model_name}/"

        try:
            process = subprocess.Popen(
                shlex.split(f"hdfs dfs {self.edd_options} -ls {s3_path}"), stdout=subprocess.PIPE, stdin=subprocess.PIPE
            )
            process.wait()
            if process.returncode != 0:
                raise ModelRegistryError(f"Listing versions in ({s3_path}) is FAILED.")

            output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
            return output
        except ModelRegistryError as e:
            print("ModelRegistryError", e)

    def load(self, model_name: str, model_version: str) -> "MLSModel":
        """
        Get a model instance from model registry.

        Args:
            model_name (str): Model name
            model_version (str): Model version
        """
        s3_path = BUCKET
        if self.aws_env in (AWSENV.STG.value, AWSENV.PRD.value):
            s3_path = f"{BUCKET}-{self.aws_env}"
        s3_path = f"s3a://{s3_path}/{model_name}/{model_version}/{MODEL_BINARY_NAME}"

        model_path = os.path.join(
            MLS_MODEL_DIR, f"{self.aws_env}_{model_name}_{model_version}_{datetime.today().strftime('%Y%m%d_%H%M%S')}",
        )
        model_binary_path = os.path.join(model_path, MODEL_BINARY_NAME)

        try:
            if not os.path.exists(model_path):
                os.makedirs(model_path)

            process = subprocess.Popen(
                shlex.split(f"hdfs dfs {self.edd_options} -get {s3_path} {model_binary_path}"),
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            process.wait()
            if process.returncode != 0:
                raise ModelRegistryError(f"Getting model from ({s3_path}) is FAILED.")

            model = joblib.load(model_binary_path)
            return model
        except ModelRegistryError as e:
            print("ModelRegistryError", e)
        finally:
            shutil.rmtree(model_path, ignore_errors=True)
