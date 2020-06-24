from datetime import datetime
from typing import List, Optional, Any, Union, Dict, Tuple

from pydantic import BaseModel, validator, BaseConfig

try:
    import rapidjson

    BaseConfig.json_dumps = rapidjson.dumps
    BaseConfig.json_loads = rapidjson.loads
except ImportError:
    pass


class TelemetryValueV2(BaseModel):
    name: str
    samples: int
    latest: Optional[Any] = None
    min: Union[None, int, float] = None
    max: Union[None, int, float] = None
    sum: Union[None, int, float] = None
    raw: Optional[Dict[datetime, Any]] = None
    all: Optional[List[Tuple[datetime, Any]]] = None


class TelemetryDataV1(BaseModel):
    samples: int
    latest: Optional[Any] = None
    min: Union[None, int, float] = None
    max: Union[None, int, float] = None
    sum: Union[None, int, float] = None
    all: Optional[List[Tuple[datetime, Any]]] = None


class TelemetryValueV1(BaseModel):
    parameterName: str
    data: TelemetryDataV1


class TelemetryV1(BaseModel):
    version: int = 1
    dateTime: datetime
    parameterValues: List[TelemetryValueV1]
    raw_values: Optional[dict] = None


class TelemetryV2(BaseModel):
    version: int = 2
    type: str
    timestamp: datetime
    values: List[TelemetryValueV2]
    serial: Optional[str] = None
    raw_values: Optional[dict] = None


def get_model(model: dict) -> BaseModel:
    return globals()[model["name"]]


if __name__ == "__main__":
    import datetime
    import pyaware.mqtt.transformations

    test_data = {'type': 'imac-controller-master', 'hello': 'world',
                 'timestamp': datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                 'values': {'ethernet-mac-address': {"latest": '00:50:c2:b4:41:d0',
                                                     "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                                     "samples": 1},
                            'ethernet-ip-mask': {"latest": '255.255.255.0',
                                                 "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                                 "samples": 1},
                            'ethernet-ip-gateway': {"latest": '10.1.1.1',
                                                    "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                                    "samples": 1},
                            'ethernet-ip-address': {"latest": '10.1.1.10',
                                                    "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                                    "samples": 1},
                            'l1-line-speed': {"latest": 500,
                                              "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                              "samples": 1},
                            'ethernet-dhcp': {"latest": False,
                                              "timestamp": datetime.datetime(2020, 1, 8, 7, 21, 37, 512471),
                                              "samples": 1},
                            }
                 }
    print(TelemetryV2.parse_obj(test_data).json(exclude_none=True))
    print(pyaware.mqtt.transformations.rename_keys(test_data, {"values": "parameterValues"}))
    print(TelemetryV1.parse_obj(
        pyaware.mqtt.transformations.rename_keys(test_data, {"values": "parameterValues",
                                                             "timestamp": "dateTime"})).json(
        exclude_none=True))
