# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.dispatch import receiver
from django.conf import settings

from django_szuprefix_saas.saas.signals import to_get_party_settings
from django_szuprefix.utils.datautils import access


@receiver(to_get_party_settings)
def get_media_settings(sender, **kwargs):
    d = settings.QCLOUD
    return {
        'media': {
            'qcloud': {
                'cos': {
                    'bucket': access(d, 'COS.BUCKET')
                },
                'vod': {
                    'appid': access(d, 'VOD.SUB_APP_ID')
                }
            }
        }
    }
