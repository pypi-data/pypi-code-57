# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, TYPE_CHECKING, Union

from azureml.automl.runtime._run_history.abstract_run import AbstractRun


if TYPE_CHECKING:
    # Single type representing an object that exposes Run APIs
    from azureml.core import Run
    RunType = Union[AbstractRun, Run]
else:
    RunType = Any
