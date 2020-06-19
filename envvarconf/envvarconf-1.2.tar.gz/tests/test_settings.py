from envvarconf import BaseSettings, validation_errors
from envvarconf.loaders import environ


class Settings(BaseSettings):
    SENTRY_DSN: str
    LOGGING_LEVEL: str = 'debug'

    HOST: str = "aaaakehgeiuhgiweurhiuerhf"*200
    PORT: int


def test_settings_invalid():
    settings = Settings(appname="evc_tests")
    settings.load([environ.Loader()], failfast=False)
    errors = validation_errors(settings)
    assert len(errors) == 2
    assert errors == ['SENTRY_DSN is not defined', 'PORT is not defined']


def test_settings_valid(monkeypatch):
    monkeypatch.setenv("SENTRY_DSN", "123")
    monkeypatch.setenv("PORT", "123")

    settings = Settings(appname="evc_tests")
    settings.load([environ.Loader()])
    errors = validation_errors(settings)
    assert len(errors) == 0
    assert settings.SENTRY_DSN == "123"
    assert settings.PORT == 123
