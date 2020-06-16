from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class CorgyCommonConfig(ModuleMixin, AppConfig):
    name = 'corgy_common'
    icon = '<i class="material-icons">settings_applications</i>'
