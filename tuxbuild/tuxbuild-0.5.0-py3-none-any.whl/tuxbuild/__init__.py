# -*- coding: utf-8 -*-

from . import build
from . import config
from . import exceptions


__config__ = None


def load_config():
    global __config__
    if not __config__:
        __config__ = config.Config()
        try:
            __config__.check_auth_token()
        except Exception as e:
            __config__ = None
            raise exceptions.InvalidToken("😔 Invalid Token: " + str(e))
    return __config__


class Configurable:
    def __init__(self, *args, **kwargs):
        cfg = load_config()
        if "token" not in kwargs:
            kwargs["token"] = cfg.auth_token
        if "kbapi_url" not in kwargs:
            kwargs["kbapi_url"] = cfg.kbapi_url
        super().__init__(*args, **kwargs)


class Build(Configurable, build.Build):
    """
    This class represents individual builds. It should be used to trigger
    builds, and optionally wait for them to finish.
    """


class BuildSet(Configurable, build.BuildSet):
    """
    This class represents a set of builds that can be triggered and watched
    simultaneously.
    """
