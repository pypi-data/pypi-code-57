from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from material.frontend.apps import ModuleMixin


class LaborConfig(ModuleMixin, AppConfig):
    name = 'labor'
    verbose_name = _('Munkaügy')
    icon = '<i class="material-icons">settings_applications</i>'
