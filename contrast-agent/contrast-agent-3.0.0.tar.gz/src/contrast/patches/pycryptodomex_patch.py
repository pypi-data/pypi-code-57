# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import register_post_import_hook
from contrast.patches.pycrypto import cs__pycrypto_decrypt, DECRYPT
from contrast.utils.patch_utils import patch_cls_or_instance

PYCRYPTODOMEX = "pycryptodomeX"


def patch_pycryptodomex(cryptodome_module):
    patch_cls_or_instance(
        cryptodome_module.Cipher._mode_cbc.CbcMode, DECRYPT, cs__pycrypto_decrypt
    )


def register_patches():
    register_post_import_hook(patch_pycryptodomex, "Cryptodome")
