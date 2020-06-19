from django.conf import settings


def is_remo_local():
    return settings.RUNNING_MODE == 'standalone'
