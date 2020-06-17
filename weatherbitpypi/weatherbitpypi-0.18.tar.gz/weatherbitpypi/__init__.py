"""Init File for weatherbit."""
from weatherbitpypi.client import Weatherbit
from weatherbitpypi.errors import WeatherbitError
from weatherbitpypi.const import (
    ALERT_ADVISORY,
    ALERT_WATCH,
    ALERT_WARNING,
    WEATHER_ALERTS,
)