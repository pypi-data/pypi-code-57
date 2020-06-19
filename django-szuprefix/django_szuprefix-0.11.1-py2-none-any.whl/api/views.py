# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.http import JsonResponse
from . import signals

def csrf_token(request):
    from django.middleware.csrf import get_token
    get_token(request)
    return JsonResponse(dict(code=0, msg="ok"))

# def get_app_configs(request):
#     srs = signals.to_get_app_setting.send(request=request)
#     data = {}
#     for config, setting in srs:
#         opt = config._meta
#         n = "as_%s_%s" % (opt.app_label, opt.model_name)
#         data[n] = rs.data
#     return JsonResponse(srs)
