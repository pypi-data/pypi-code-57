import logging
from fastutils import dictutils
from fastutils import cipherutils
from django.db import models
from django.conf import settings
from django.db.models.lookups import IContains


logger = logging.getLogger(__name__)


class SafeFieldMixinBase(object):
    default_cipher_class = cipherutils.AesCipher
    default_encoder_class = {
        cipherutils.AesCipher: cipherutils.HexlifyEncoder,
        cipherutils.S12Cipher: cipherutils.HexlifyEncoder,
    }
    force_text_default = True
    text_encoding_default = "utf-8"
    default_kwargs = {
        cipherutils.AesCipher: {
            "key": cipherutils.mysql_aes_key,
        },
    }
    default_encrypt_kwargs = {}
    default_decrypt_kwargs = {}

    def get_cipher(self, **params):
        password = params.get("password", settings.SECRET_KEY)
        cipher_class = params.get("cipher_class", self.default_cipher_class)
        encoder = params.get("encoder", None)
        if not encoder:
            encoder_class = params.get("encoder_class", self.default_encoder_class.get(cipher_class, None))
            if encoder_class:
                encoder = encoder_class()
            else:
                encoder = None
        encrypt_kwargs = {}
        encrypt_kwargs.update(self.default_encrypt_kwargs.get(cipher_class, {}))
        encrypt_kwargs.update(params.get("encrypt_kwargs", {}))
        decrypt_kwargs = {}
        decrypt_kwargs.update(self.default_decrypt_kwargs.get(cipher_class, {}))
        decrypt_kwargs.update(params.get("decrypt_kwargs", {}))
        kwargs = {}
        kwargs.update(self.default_kwargs.get(cipher_class, {}))
        kwargs.update(params.get("kwargs", {}))
        force_text = params.get("force_text", self.force_text_default)
        text_encoding = params.get("text_encoding", self.text_encoding_default)
        cipher_params = dictutils.ignore_none_item({
            "password": password,
            "encoder": encoder,
            "kwargs": kwargs,
            "encrypt_kwargs": encrypt_kwargs,
            "decrypt_kwargs": decrypt_kwargs,
            "force_text": force_text,
            "text_encoding": text_encoding,
        })
        return cipher_class(**cipher_params)


    def __init__(self, *args, **kwargs):
        cipher_params = dictutils.ignore_none_item({
            "password": kwargs.pop("password", None),
            "encoder": kwargs.pop("encoder", None),
            "encoder_class": kwargs.pop("encoder_class", None),
            "cipher_class": kwargs.pop("cipher_class", None),
            "kwargs": kwargs.pop("kwargs", None),
            "encrypt_kwargs": kwargs.pop("encrypt_kwargs", None),
            "decrypt_kwargs": kwargs.pop("decrypt_kwargs", None),
            "force_text": kwargs.pop("force_text", None),
            "text_encoding": kwargs.pop("text_encoding", None),
        })
        self.cipher = kwargs.pop("cipher", self.get_cipher(**cipher_params))
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if not value:
            return None
        try:
            value = self.cipher.decrypt(value)
            return value
        except Exception as error:
            logger.exception("Error: SafeCharField.from_db_value decrypt failed: error={} value={}".format(error, value))
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            return self.cipher.encrypt(value)
        else:
            return value

    def get_lookup(self, lookup_name):
        cipher = self.cipher
        def get_db_prep_lookup(self, value, connection):
            result = ('%s', [cipher.encrypt(value)])
            return result
        base_lookup = super().get_lookup(lookup_name)
        return type(base_lookup.__name__, (base_lookup,), {"get_db_prep_lookup": get_db_prep_lookup})


class SafeStringFieldMixin(SafeFieldMixinBase):
    pass

class SafeCharField(SafeStringFieldMixin, models.CharField):
    pass

class SafeTextField(SafeStringFieldMixin, models.TextField):
    pass

class SafeEmailField(SafeStringFieldMixin, models.EmailField):
    pass

class SafeURLField(SafeStringFieldMixin, models.URLField):
    pass

class SafeGenericIPAddressField(SafeStringFieldMixin, models.GenericIPAddressField):

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop("max_length", 128)
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def get_internal_type(self):
        return "CharField"

class SafeIntegerFieldMixin(SafeFieldMixinBase):

    default_cipher_class = cipherutils.IvCipher
    force_text_default = False

class SafeIntegerField(SafeIntegerFieldMixin, models.IntegerField):
    pass
