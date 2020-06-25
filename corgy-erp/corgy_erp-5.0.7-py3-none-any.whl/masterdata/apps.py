from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class MasterdataConfig(ModuleMixin, AppConfig):
    name = 'masterdata'
    verbose_name = _('Törzsadat')
    icon = '<i class="material-icons">library_books</i>'
