from .patches import *
'''
from django.contrib.auth import authenticate
from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class SocialAccount(models.Model):
    """A simplified version of allauth.socialaccount.models.SocialAccount"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=False, blank=False)  # allauth was ForeignKey because there could be several social accounts in theory
    uid = models.CharField(verbose_name=_('uid'), max_length=255, unique=True, null=False, blank=False)  # MySQL does not allow unique CharFields to have a max_length > 255
    last_login = models.DateTimeField(verbose_name=_('last login'), auto_now=True)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    json_response = models.TextField(verbose_name=_('JSON Response'))  # allauth actually creates a JSONField class to support this

    class Meta:
        # unique_together = ('provider', 'uid')
        verbose_name = _('social account')
        verbose_name_plural = _('social accounts')

    def authenticate(self):  # This could be useful at some point
        return authenticate(account=self)

    def __str__(self):
        return force_str(self.user)
'''
