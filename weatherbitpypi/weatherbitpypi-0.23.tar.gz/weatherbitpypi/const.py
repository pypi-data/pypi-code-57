"""Constant definitions for Weatherbit."""

BASE_URL = "https://api.weatherbit.io/v2.0"

DATA_TYPES = [
    "current",
    "forecast",
    "alert",
]

ALERT_ADVISORY = "Advisory"
ALERT_WATCH = "Watch"
ALERT_WARNING = "Warning"

WEATHER_ALERTS = [
    ALERT_ADVISORY,
    ALERT_WATCH,
    ALERT_WARNING
]

DEFAULT_TIMEOUT = 10

SUPPORTED_LANGUAGES = [
    "en",
    "da",
    "nl",
    "es",
    "de",
    "fr",
    "it",
    "nb",
    "sv",
    "pt",
]
