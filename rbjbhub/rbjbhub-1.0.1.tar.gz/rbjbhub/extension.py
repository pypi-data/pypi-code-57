from __future__ import unicode_literals

import os.path

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djblets.siteconfig.forms import SiteSettingsForm
from djblets.siteconfig.models import SiteConfiguration

import requests

from requests.auth import HTTPBasicAuth

from reviewboard.accounts.backends import AuthBackend
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import AuthBackendHook


def _update_user(user, token):
    """ Updates a user according to what is set it hub.  This is mostly to deal
        with email changes, but they can also change their name and username so
        this just updates everything.
    """

    siteconfig = SiteConfiguration.objects.get_current()

    # look up the user in hub
    base_url = siteconfig.get('auth_jetbrains_hub_url')
    uri = os.path.join(base_url, 'api/rest/oauth2/userinfo')

    headers = {
        'Authorization': 'Bearer ' + token
    }

    resp = requests.get(uri, headers=headers)
    resp.raise_for_status()

    hub_user = resp.json()

    # we don't have a good way to split the username to a first name/last name,
    # so we split on the first space and then treat the two parts as the first
    # and last names.
    name_parts = hub_user['name'].split(' ', 1)

    # figure the users email address
    email = hub_user.get('email', '')

    # only set the users email address if it is verified.  This is problematic
    # when a user is anonymized, but we'll come back to that.
    if hub_user.get('email_verified', False):
        user.email = email

    # now update the django user
    user.first_name = name_parts[0]
    user.last_name = len(name_parts) > 1 and name_parts[1] or ''

    user.save()

    return user


class JetBrainsHubSettingsForm(SiteSettingsForm):
    """ JetBrains Hub Settings Form """

    auth_jetbrains_hub_url = forms.CharField(
        label=_('JetBrains Hub instance URL'),
        help_text=_('The URL of your JetBrains Hub instance.'),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}),
    )

    auth_jetbrains_hub_client_id = forms.CharField(
        label=_('Client ID'),
        help_text=_('The client ID for the JetBrains Hub Service'),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}),
    )

    auth_jetbrains_hub_client_secret = forms.CharField(
        label=_('Client Secret'),
        help_text=_('The client secret for the JetBrains Hub Service'),
        required=True,
        widget=forms.PasswordInput(render_value=True, attrs={'size': '40'}),
    )

    auth_jetbrains_hub_scopes = forms.CharField(
        label=_('Scopes'),
        help_text=_('A space separated list scopes that you are requesting '
                    'from the issuer.'),
        required=True,
        widget=forms.TextInput(attrs={'size': '40'}),
    )

    class Meta:
        title = _("JetBrains Hub Settings")


class JetBrainsHubAuthBackend(AuthBackend):
    backend_id = 'grim-jbhub'
    name = _('JetBrains Hub')
    settings_form = JetBrainsHubSettingsForm
    login_instructions = _('If you have 2FA enabled in your Hub account, you '
                           'will need to use an application password.')

    def authenticate(self, username, password, **kwargs):
        siteconfig = SiteConfiguration.objects.get_current()

        username = username.strip()

        data = {
            'grant_type': 'password',
            'scope': siteconfig.get('auth_jetbrains_hub_scopes'),
            'username': username,
            'password': password,
        }

        uri = os.path.join(
            siteconfig.get('auth_jetbrains_hub_url'),
            'api/rest/oauth2/token',
        )

        auth = HTTPBasicAuth(
            siteconfig.get('auth_jetbrains_hub_client_id'),
            siteconfig.get('auth_jetbrains_hub_client_secret'),
        )

        resp = requests.post(uri, auth=auth, data=data)
        if resp.status_code != 200:
            return None

        json = resp.json()
        token = json.get('access_token', '')

        return self.get_or_create_user(username, token)

    def get_or_create_user(self, username, token, request=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username)

        return _update_user(user, token)


class JetBrainsHubExtension(Extension):
    metadata = {
        'Name': _('JetBrains Hub Authentication'),
        'Summary': _('Support for JetBrains Hub'),
    }

    def initialize(self):
        AuthBackendHook(self, JetBrainsHubAuthBackend)
