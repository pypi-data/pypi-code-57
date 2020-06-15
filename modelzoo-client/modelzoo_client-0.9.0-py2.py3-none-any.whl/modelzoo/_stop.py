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

from typing import Optional

from . import api, model_state, _wait


def stop(model_name: str, wait: bool = True, api_key: Optional[str] = None) -> None:
    """
    Stop a model. This function has no effect if the model is already stopped.

    Args:
        model_name: String name of the model.
        wait:
            Boolean that specifies whether this function blocks until the model
            reaches a STOPPED state.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.

    Returns:
        Nothing

    Raises:
        APIError if the model doesn't exist.
    """
    api.call(method="POST", path="models/{}/stop".format(model_name), api_key=api_key)

    if wait:
        _wait.wait(model_name, model_state.ModelState.STOPPED.value, api_key)
