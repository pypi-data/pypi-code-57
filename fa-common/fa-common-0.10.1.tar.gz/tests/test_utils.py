import os
import json
from fa_common import CamelModel, get_settings
from datetime import date, datetime, time, timezone


class TestModel(CamelModel):
    date_var: date
    dt_var: datetime
    time_var: time


def test_camel_model_dt():
    os.environ["TZ"] = "UTC"
    settings = get_settings()
    settings.TZ = "UTC"

    date_var = datetime.now().date()
    dt_var = datetime.now()
    time_var = datetime.now().time()

    model = TestModel(date_var=date_var, dt_var=dt_var, time_var=time_var)
    test_dict = model.json()
    test_dict = json.loads(test_dict)

    print(test_dict)
    assert test_dict["date_var"] == date_var.isoformat()
    assert (
        test_dict["dt_var"]
        == dt_var.replace(microsecond=0, tzinfo=timezone.utc).isoformat()
    )
    assert (
        test_dict["time_var"]
        == time_var.replace(microsecond=0, tzinfo=timezone.utc).isoformat()
    )
