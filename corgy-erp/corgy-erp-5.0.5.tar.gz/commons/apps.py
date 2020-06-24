from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _

class CommonsConfig(ModuleMixin, AppConfig):
    name = 'commons'
    verbose_name = _('Személyi adatlapok')
    icon = '<i class="material-icons">account_circle</i>'
