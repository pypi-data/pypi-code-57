from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

from starlette.requests import Request
from starlette.responses import Response

from spell.serving.background import BackgroundTasks, MetricsValue

__all__ = [
    "APIResponse",
    "MetricsValue",
    "PredictorArgumentGenerator",
    "PredictorClass",
    "PredictorMethod",
    "PredictorMethodArguments",
    "PredictorResponse",
]

PredictorResponse = Union[str, bytes, Response, Dict, List]
APIResponse = Tuple[PredictorResponse, BackgroundTasks]
PredictorClass = TypeVar("PredictorClass")
PredictorMethod = Callable[[Tuple[Any, ...]], PredictorResponse]
PredictorMethodArguments = Tuple[Dict[str, Any], Optional[BackgroundTasks]]
PredictorArgumentGenerator = Callable[[Request], PredictorMethodArguments]
