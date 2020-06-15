#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import tempfile
from typing import Optional

import tensorflow as tf

from modelzoo import deploy_lib, exceptions, util, ResourcesConfig
from modelzoo.tensorflow import util as tensorflow_util


def deploy(
    model: tf.keras.models.Model,
    model_name: Optional[str] = None,
    resources_config: Optional[ResourcesConfig] = None,
    api_key: Optional[str] = None,
    wait_until_healthy: bool = True,
) -> None:
    """
    Deploy a TensorFlow model to your zoo.

    .. note::

        This function will serialize a model to a temporary directory on the
        filesystem before uploading it to Model Zoo.

    Args:
        model:
            A ``tf.keras.models.Model`` to deploy.
        model_name:
            Optional string name of the model. If not provided, a random name
            will be generated. Model name must be unique across all of a user's
            models.
        resources_config:
            A ResourcesConfig
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.
        wait_until_healthy:
            If True (default), this function will refrain from returning until
            the model has reached a :py:class:`HEALTHY <modelzoo.ModelState>` state.

    Returns:
        The name of the created model.
    """
    model_name = model_name or util.generate_model_name()

    if isinstance(model, tf.keras.models.Model):
        with tempfile.TemporaryDirectory() as tempdir:
            model.save(tempdir)
            return deploy_from_saved_model_dir(
                model_dir=tempdir,
                model_name=model_name,
                resources_config=resources_config,
                api_key=api_key,
                wait_until_healthy=wait_until_healthy,
            )
    else:
        raise exceptions.InvalidArgumentError(
            "Model type is not supported: {}".format(type(model))
        )


def deploy_from_saved_model_dir(
    model_dir: str,
    model_name: Optional[str] = None,
    resources_config: Optional[ResourcesConfig] = None,
    api_key: Optional[str] = None,
    wait_until_healthy: bool = True,
) -> None:
    documentation = tensorflow_util.generate_default_tensorflow_docs(
        model_name, model_dir
    )

    return deploy_lib.deploy_from_dir(
        model_name=model_name,
        model_dir=model_dir,
        resources_config=resources_config,
        documentation=documentation,
        framework="TENSORFLOW",
        api_key=api_key,
        wait_until_healthy=wait_until_healthy,
    )
