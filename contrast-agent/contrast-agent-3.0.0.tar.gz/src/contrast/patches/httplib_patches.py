# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Patches for HTTPConnection.putrequest

We can't simply use policy to patch this method because it is also instrumented for
the SSRF protect rule. If/when we start using policy for protect as well, we will be
able to remove these patches.
"""
from contrast.extern.wrapt import register_post_import_hook

from contrast.applies.ssrf import apply_rule
from contrast.utils.patch_utils import patch_cls_or_instance

HTTPCONNECTION = "http.client.HTTPConnection"
PUTREQUEST = "putrequest"


def putrequest(orig_func, patch_policy=None, *args, **kwargs):
    return apply_rule(HTTPCONNECTION, PUTREQUEST, orig_func, args, kwargs)


def patch_httplib_request(http_module):
    patch_cls_or_instance(http_module.HTTPConnection, PUTREQUEST, putrequest)


def patch_http_client_request(http_module):
    patch_cls_or_instance(http_module.HTTPConnection, PUTREQUEST, putrequest)


def register_patches():
    register_post_import_hook(patch_httplib_request, "httplib")
    register_post_import_hook(patch_http_client_request, "http.client")
