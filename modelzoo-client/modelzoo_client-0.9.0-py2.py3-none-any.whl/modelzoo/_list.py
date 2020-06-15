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


def list(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve information about all of the user's deployed models.

    Args:
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.

    Returns:
        Dictionary containing a list of models.
    """
    return api.call(method="GET", path="models", api_key=api_key)
