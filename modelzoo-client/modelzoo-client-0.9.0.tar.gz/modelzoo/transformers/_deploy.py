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

import pathlib
import tempfile
from typing import Dict, Optional

import transformers

from modelzoo import deploy_lib, exceptions, util
from modelzoo.transformers import util as transformers_util


SUPPORTED_PIPELINES = transformers.TextGenerationPipeline


def deploy(
    pipeline: transformers.Pipeline,
    model_name: Optional[str] = None,
    resources_config: Optional[Dict] = None,
    api_key: Optional[str] = None,
    wait_until_healthy: bool = True,
) -> None:
    """
    Deploy a `transformers.Pipeline
    <https://huggingface.co/transformers/main_classes/pipelines.html>`_.

    .. note::

        This function will serialize a model to a temporary directory on the
        filesystem before uploading it to Model Zoo.

    .. note::

        Currently, the Model Zoo free tier only supports
        `transformers.TextGenerationPipeline
        <https://huggingface.co/transformers/main_classes/pipelines.html?highlight=textgeneration#transformers.TextGenerationPipeline>`_.

    Args:
        pipeline:
            A `transformers.Pipeline
            <https://huggingface.co/transformers/main_classes/pipelines.html>`_
            object to deploy.
        model_name:
            Optional string name of the model. If not provided, a random name
            will be generated. Model name must be unique across all of a user's
            models.
        resources_config:
            TODO:
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

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)

        documentation = transformers_util.generate_default_transformers_docs(
            model_name=model_name, pipeline=pipeline
        )

        if not isinstance(pipeline, SUPPORTED_PIPELINES):
            raise exceptions.InvalidArgumentError(
                "Input type is not supported: {}".format(type(pipeline))
            )

        pipeline.save_pretrained(str(tempdir))

        return deploy_lib.deploy_from_dir(
            model_name=model_name,
            model_dir=str(tempdir),
            api_key=api_key,
            wait_until_healthy=wait_until_healthy,
            transformers_config={"pipeline_class": pipeline.__class__.__name__},
            resources_config=resources_config,
            documentation=documentation,
            framework="TRANSFORMERS",
        )
