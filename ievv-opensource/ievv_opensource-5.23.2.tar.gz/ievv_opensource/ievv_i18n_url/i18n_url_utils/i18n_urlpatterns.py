import re

from django import urls
from django.conf.urls import url
from django.conf import settings

from ievv_opensource.ievv_i18n_url import active_i18n_url_translation
from ievv_opensource.ievv_i18n_url.views import RedirectToLanguagecodeView

#
# Note: Basically copy and tuning from https://github.com/django/django/blob/1.11.29/django/conf/urls/i18n.py
#
# When updating for Django 2+, see https://github.com/django/django/blob/master/django/conf/urls/i18n.py
#


def i18n_patterns(*urls, include_redirect_view=True):
    """
    Adds the language code prefix to every URL pattern within this
    function. This may only be used in the root URLconf, not in an included
    URLconf.
    """
    if not settings.USE_I18N:
        return list(urls)
    return [
        url(r'^_ievv-i18n-redirect-to/(?P<languagecode>[a-zA-Z-]+)/(?P<path>.*)$',
            RedirectToLanguagecodeView.as_view(),
            name='ievv_i18n_url_redirect_to_languagecode'),
        I18nRegexURLResolver(list(urls)),
    ]


class I18nRegexURLResolver(urls.RegexURLResolver):
    """
    A URL resolver that always matches the active language code as URL prefix.

    Rather than taking a regex argument, we just override the ``regex``
    function to always return the active language-code as regex.
    """
    def __init__(
        self, urlconf_name, default_kwargs=None, app_name=None, namespace=None,
        prefix_default_language=False
    ):
        super().__init__(None, urlconf_name, default_kwargs, app_name, namespace)
        self.prefix_default_language = prefix_default_language

    @property
    def regex(self):
        language_code = active_i18n_url_translation.get_active_languagecode()

        if language_code not in self._regex_dict:
            urlpath_prefix = active_i18n_url_translation.get_active_language_urlpath_prefix()
            if urlpath_prefix:
                regex_string = '^%s/' % urlpath_prefix
            else:
                regex_string = ''
            self._regex_dict[language_code] = re.compile(regex_string, re.UNICODE)
        return self._regex_dict[language_code]
