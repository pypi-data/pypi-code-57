#! -*- coding: utf-8 -*-
import os

from django import forms
from django.conf import settings
from django.utils.html import smart_urlquote


class OssFileWidget(forms.URLInput):
    template_name = 'ossFileField.html'

    def __init__(self, attrs=None):
        final_attrs = {
            'domain': settings.OSS_PROXY_URL.strip('/').strip(''),
            'bucket': settings.OSS_BUCKET_NAME.strip(''),
            'get_token_url': os.path.join(settings.SERVER_URL.strip('/').strip(), settings.OSS_TOKEN_ROUTE.strip('/').strip())
        }

        if attrs is not None:
            final_attrs.update(attrs)
        super(OssFileWidget, self).__init__(attrs=final_attrs)

    def get_context(self, name, value, attrs):
        context = super(OssFileWidget, self).get_context(name, value, attrs)
        context['widget']['href'] = smart_urlquote(context['widget']['value']) if value else ''
        return context
