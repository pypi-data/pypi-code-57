"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from marshmallow import fields
from katena_chain_sdk_py.crypto.nacl.public_key import PublicKey
from katena_chain_sdk_py.entity.certify.common import get_secret_nacl_box_v1_type, NAMESPACE, get_secret_id_key
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.serializer.bytes_field import BytesField
from katena_chain_sdk_py.serializer.crypto_field import KeyField
from katena_chain_sdk_py.utils.common import concat_fqid


class SecretNaclBoxV1(TxData):
    # SecretNaclBoxV1 is the first version of a NaCl box secret.

    def __init__(self, id: str, content: bytes, nonce: bytes, sender: PublicKey):
        self.id = id
        self.content = content
        self.nonce = nonce
        self.sender = sender

    def get_id(self) -> str:
        return self.id

    def get_content(self) -> bytes:
        return self.content

    def get_nonce(self) -> bytes:
        return self.nonce

    def get_sender(self) -> PublicKey:
        return self.sender

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_secret_nacl_box_v1_type()

    def get_state_ids(self, signer_company_bcid: str) -> str:
        return dict[get_secret_id_key():concat_fqid(signer_company_bcid, self.id)]


class SecretNaclBoxV1Schema(BaseSchema):
    # SecretNaclBoxV1Schema allows to serialize and deserialize SecretNaclBoxV1.

    __model__ = SecretNaclBoxV1
    content = BytesField()
    id = fields.Str()
    nonce = BytesField()
    sender = KeyField(PublicKey)
