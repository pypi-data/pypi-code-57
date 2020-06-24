from typing import AnyStr, Optional, Union

from numpy import bool as np_bool, integer as np_int, floating as np_float
from starlette.background import BackgroundTasks as StarletteBackgroundTasks

from spell.metrics import send_metric

MetricsValue = Union[bool, np_bool, int, np_int, float, np_float, AnyStr]


class BackgroundTasks(StarletteBackgroundTasks):
    def send_metric(self, name: str, value: MetricsValue, index: Optional[int] = None) -> None:
        super().add_task(send_metric, name, value, index=index)
