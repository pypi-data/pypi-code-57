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

from . import api


def predict(
    model_name: str, payload: Dict[str, Any], api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a prediction to a model.

    Args:
        model_name: String name of the model.
        payload:
            Dictionary of data to send to the model endpoint. Must be
            JSON-serializable.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.
    """

    response = api.raw_call(
        method="POST",
        path="models/{}/predict".format(model_name),
        api_key=api_key,
        payload=payload,
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise api.APIError(
            "Model '{}' was not found: {}".format(model_name, str(response.json()))
        )
    else:
        try:
            error = response.json()["error"]
        except (ValueError, KeyError):
            error = response.content
        raise api.APIError(error)
