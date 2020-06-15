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

from typing import Any, Dict, Optional

from modelzoo import predict as base_predict


def generate(
    model_name: str,
    input_str: Optional[str] = "",
    api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Send a prediction to a Transformers model. In addition to an optional input
    string, this function accepts the same arguments as
    `transformers.PreTrainedModel.generate()
    <https://huggingface.co/transformers/main_classes/model.html#transformers.PreTrainedModel.generate>`_.


    Args:
        model_name: String name of the model.
        input_str: An optional input string that will be used to prime the
        language model.
        api_key: Will override the environment api key, if present.
        **kwargs: Add any keyword arguments that would be accepted by
        `transformers.PreTrainedModel.generate()
        <https://huggingface.co/transformers/main_classes/model.html#transformers.PreTrainedModel.generate>`_.

    Returns:
        The output prediction
    """
    return base_predict(
        model_name, {"input": input_str, **kwargs}, api_key=api_key
    ).get("output")
