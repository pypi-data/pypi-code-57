from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CommonsConfig(AppConfig):
    name = 'commons'
    verbose_name = _('COMMONS')
    icon = '<i class="material-icons">settings_applications</i>'
