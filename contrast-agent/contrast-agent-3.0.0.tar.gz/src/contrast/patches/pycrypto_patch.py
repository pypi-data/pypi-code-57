# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import register_post_import_hook

from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


PYCRYPTO = "pycrypto"
DECRYPT = "decrypt"


def __cs_decrypt(original_decrypt, *args, **kwargs):
    """
    :param original_decrypt: decrypt_method
    :param args: 1 => self, 2 => cipher_text
    :return:

    If the mode is CBC attempt to decrypt the cipher_text and validate the padding.
    If the padding is invalid, apply the padding oracle rule.
    """
    from Crypto.Cipher.blockalgo import MODE_CBC

    if args[0].mode == MODE_CBC:
        value = original_decrypt(*args, **kwargs)

        try:
            if not __cs_validate_padding(value.decode()):
                # TODO: revisit this: we deleted the padding oracle rule
                # apply_rule("Invalid Padding")
                pass
        except UnicodeDecodeError:
            _announce_unicode_decode_error()

        return value

    return original_decrypt(*args, **kwargs)


def __cs_validate_padding(padded_text):
    return all([n == padded_text[-1] for n in padded_text[-ord(padded_text[-1]) :]])


def _announce_unicode_decode_error():
    logger.warning(
        "Crypto decryption could not be decoded with UTF-8. PaddingOracleRule not applied."
    )


def patch_pycrypto(crypto_module):
    patch_cls_or_instance(
        crypto_module.Cipher.blockalgo.BlockAlgo, DECRYPT, __cs_decrypt
    )


def register_patches():
    register_post_import_hook(patch_pycrypto, "Crypto")
