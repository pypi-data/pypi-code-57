"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from marshmallow import fields
from katena_chain_sdk_py.crypto.ed25519.public_key import PublicKey
from katena_chain_sdk_py.entity.certify.common import get_certificate_ed25519_v1_type, get_certificate_raw_v1_type, \
    NAMESPACE, get_certificate_id_key
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.serializer.bytes_field import BytesField
from katena_chain_sdk_py.serializer.crypto_field import KeyField
from katena_chain_sdk_py.utils.common import concat_fqid


class CertificateRawV1(TxData):
    # CertificateRawV1 is the first version of a raw certificate.

    def __init__(self, id: str, value: bytes):
        self.id = id
        self.value = value

    def get_id(self) -> str:
        return self.id

    def get_value(self) -> bytes:
        return self.value

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_certificate_raw_v1_type()

    def get_state_ids(self, signer_company_bcid: str) -> str:
        return dict[get_certificate_id_key():concat_fqid(signer_company_bcid, self.id)]


class CertificateRawV1Schema(BaseSchema):
    # CertificateRawV1Schema allows to serialize and deserialize CertificateRawV1.

    __model__ = CertificateRawV1
    id = fields.Str()
    value = BytesField()


class CertificateEd25519V1(TxData):
    # CertificateEd25519V1 is the first version of an ed25519 certificate.

    def __init__(self, id: str, signer: PublicKey, signature: bytes):
        self.id = id
        self.signature = signature
        self.signer = signer

    def get_id(self) -> str:
        return self.id

    def get_signer(self) -> PublicKey:
        return self.signer

    def get_signature(self) -> bytes:
        return self.signature

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_certificate_ed25519_v1_type()

    def get_state_ids(self, signer_company_bcid: str) -> str:
        return dict[get_certificate_id_key():concat_fqid(signer_company_bcid, self.id)]


class CertificateEd25519V1Schema(BaseSchema):
    # CertificateEd25519V1Schema allows to serialize and deserialize CertificateEd25519V1.

    __model__ = CertificateEd25519V1
    id = fields.Str()
    signature = BytesField()
    signer = KeyField(PublicKey)
