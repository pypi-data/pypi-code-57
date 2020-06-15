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


def logs(
    model_name: str, api_key: Optional[str] = None, max_num_logs: Optional[int] = None
) -> Dict[str, Any]:
    """
    Print the most recent logs emitted by the model.

    Args:
        model_name: String name of the model.
        max_num_logs:
            The maximum number of log lines to retrieve. Defaults to the
            maximum allowed number, 10,000 log lines. If there are more log
            lines than max_num_logs, the most recent log lines will be
            returned.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.

    Returns:
        Dictionary containing a list of models.
    """
    payload = {"max_num_logs": max_num_logs} if max_num_logs else None
    response = api.call(
        method="GET",
        path="models/{}/logs".format(model_name),
        api_key=api_key,
        payload=payload,
    )
    return response
