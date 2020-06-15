"""
Settings module for ai_kit_file_management.

Settings are namespaces under AI_KIT_FILE_MANAGEMENT in
the settings module. So your projects settings.py might look like

AI_KIT_FILE_MANAGEMENT = {
    "MODEL": "",
    ...
}

To access the settings, an api_settings object is provided that gives back the
configured settings or falls back to defaults
"""
from django.conf import settings
from django.test.signals import setting_changed
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
from ai_kit_file_management.models import File

DEFAULT_FORMATS = [
    "image/jpeg",
    "image/png",
    "application/pdf",
    "application/zip",
    "text/comma-separated-values",
]


class DefaultSetting:
    pass


DEFAULTS = {
    "FILE_MODEL": File,
    "SERIALIZER": DefaultSetting(),
    "MAX_FILE_SIZE_KB": 1000000,
    "ALLOWED_FORMATS": DEFAULT_FORMATS,
    "PERMISSION_CLASSES": (IsAuthenticated,),
    "FILESERVER_BACKEND": "dev",
}


class UnknownConfigurationError(Exception):
    pass


class InvalidConfigurationError(Exception):
    pass


class APISettings:
    """
    The settings are implemented as an object for two reasons: it allows access
    to the configuration parameters as properties and it enables validation
    of the settings.

    In your code you can use this object like so:

    from ai_kit_file_management.settings import api_settings
    print(api_settings.MODEL)
    """

    def __init__(self, user_settings, default=DEFAULTS):
        for setting in user_settings:
            if setting not in default:
                raise UnknownConfigurationError(setting)
            elif not isinstance(user_settings[setting], type(default[setting])):
                # exception for File and Serializer, since they are allowed to have another type
                if setting not in ("FILE_MODEL", "SERIALIZER",):
                    raise InvalidConfigurationError(
                        f"Type of setting {setting} should be {type(default[setting])}, "
                        f"but was {type(user_settings[setting])}."
                    )

            # guard for misconfiguration
            if setting == "FILESERVER_BACKEND":
                options = ["dev", "nginx", "x-sendfile"]
                user_setting = user_settings[setting]
                if user_setting not in options:
                    raise InvalidConfigurationError(
                        f"unkown configuration option {user_setting} for FILESERVER_BACKEND. Must be on of {options}."
                    )

        merged = {**default, **user_settings}
        self._settings = {
            k: APISettings.convert_settings_node(v, default[k])
            for k, v in merged.items()
        }

    def __getattr__(self, attr):
        # some special sauce to get around the circular import
        # We need the settings in the definition of the Serializer to get the
        # model, but we also have to set the serializer
        if attr == "SERIALIZER" and isinstance(
            self._settings["SERIALIZER"], DefaultSetting
        ):
            from ai_kit_file_management.serializers import FileSerializer

            return FileSerializer
        return self._settings[attr]

    @classmethod
    def convert_settings_node(cls, node, default):
        if isinstance(node, dict):
            return cls(node, default)
        return node


api_settings = APISettings(getattr(settings, "AI_KIT_FILE_MANAGEMENT", {}))


@receiver(setting_changed)
def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "AI_KIT_FILE_MANAGEMENT":
        global api_settings
        api_settings = APISettings(getattr(settings, "AI_KIT_FILE_MANAGEMENT", {}))
