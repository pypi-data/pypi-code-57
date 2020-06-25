from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MailBoxConfig(AppConfig):
    name = 'django_mailbox_abstract'
    verbose_name = _("Mail Box")
