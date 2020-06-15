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

"""The Model Zoo Python client."""

from ._delete import delete
from ._info import info
from ._list import list
from ._logs import logs
from ._predict import predict
from ._start import start
from ._stop import stop
from ._wait import wait
from .model_state import ModelState
from .resources_config import ResourcesConfig
from .config import auth

__all__ = (
    "auth",
    "delete",
    "info",
    "list",
    "logs",
    "predict",
    "start",
    "stop",
    "wait",
    "ModelState",
    "ResourcesConfig",
)
