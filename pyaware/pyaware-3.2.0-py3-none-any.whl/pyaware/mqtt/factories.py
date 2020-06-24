from typing import Callable


def get_factory(factory: dict) -> Callable:
    return globals()[factory["name"]]


def telemetry_v1(data, timestamp, **kwargs) -> dict:
    msg = {
        "dateTime": timestamp,
        "raw_values": data,
        "parameterValues": []
    }
    for item in data:
        name = item.pop("name")
        msg["parameterValues"].append(
            {"parameterName": name,
             "data": item}
        )
    return msg


def telemetry_v2(data, meta, timestamp, **kwargs) -> dict:
    msg = meta.copy()
    msg["timestamp"] = timestamp
    msg["values"] = data
    msg["raw_values"] = data
    return msg
