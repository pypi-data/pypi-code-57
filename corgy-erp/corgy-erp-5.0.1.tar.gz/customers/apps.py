from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class CustomersConfig(ModuleMixin, AppConfig):
    name = 'customers'
    verbose_name = _('Ügyfelek')
    icon = '<i class="material-icons">settings_applications</i>'
