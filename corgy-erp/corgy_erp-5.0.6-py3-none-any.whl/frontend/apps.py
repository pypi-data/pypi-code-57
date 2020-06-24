from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class FrontendConfig(ModuleMixin, AppConfig):
    name = 'frontend'
    verbose_name = _('Ügyfélkapu')
    icon = '<i class="material-icons">settings_applications</i>'
