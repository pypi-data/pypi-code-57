from datetime import datetime

import pytz


def hello_world(name: str) -> str:
    return f"Hello World {name}"


def time_now() -> datetime:
    return pytz.utc.localize(datetime.utcnow())
