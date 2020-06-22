"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from marshmallow import fields
from katena_chain_sdk_py.crypto.ed25519.public_key import PublicKey
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.entity.account.common import get_key_id_key, get_key_create_v1_type, get_key_rotate_v1_type, \
    get_key_revoke_v1_type, NAMESPACE
from katena_chain_sdk_py.serializer.crypto_field import KeyField
from katena_chain_sdk_py.utils.common import concat_fqid


class KeyV1:
    # KeyV1 is the version 1 of a key message

    def __init__(self, fqid: str, public_key: PublicKey, is_active: bool, role: str):
        self.fqid = fqid
        self.public_key = public_key
        self.is_active = is_active
        self.role = role

    def get_fqid(self) -> str:
        return self.fqid

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def get_is_active(self) -> bool:
        return self.is_active

    def get_role(self) -> str:
        return self.role


class KeyV1Schema(BaseSchema):
    # KeyV1Schema allows to serialize and deserialize KeyV1.

    __model__ = KeyV1
    fqid = fields.Str()
    public_key = KeyField(PublicKey)
    is_active = fields.Bool()
    role = fields.Str()


class KeyCreateV1(TxData):
    # KeyCreateV1 is the version 1 of a key create message

    def __init__(self, id: str, public_key: PublicKey, role: str):
        self.id = id
        self.public_key = public_key
        self.role = role

    def get_id(self) -> str:
        return self.id

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def get_role(self) -> str:
        return self.role

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_key_create_v1_type()

    def get_state_ids(self, signer_company_id: str) -> dict:
        return dict[get_key_id_key():concat_fqid(signer_company_id, self.id)]


class KeyCreateV1Schema(BaseSchema):
    # KeyCreateV1Schema allows to serialize and deserialize KeyCreateV1.

    __model__ = KeyCreateV1
    id = fields.Str()
    public_key = KeyField(PublicKey)
    role = fields.Str()


class KeyRotateV1(TxData):
    # KeyRotateV1 is the version 1 of a key rotate message

    def __init__(self, id: str, public_key: PublicKey):
        self.id = id
        self.public_key = public_key

    def get_id(self) -> str:
        return self.id

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_key_rotate_v1_type()

    def get_state_ids(self, signer_company_id: str) -> dict:
        return dict[get_key_id_key():concat_fqid(signer_company_id, self.id)]


class KeyRotateV1Schema(BaseSchema):
    # KeyRotateV1Schema allows to serialize and deserialize KeyRotateV1.

    __model__ = KeyRotateV1
    id = fields.Str()
    public_key = KeyField(PublicKey)


class KeyRevokeV1(TxData):
    # KeyRevokeV1 is the version 1 of a key revoke message

    def __init__(self, id: str):
        self.id = id

    def get_id(self) -> str:
        return self.id

    def get_namespace(self) -> str:
        return NAMESPACE

    def get_type(self) -> str:
        return get_key_revoke_v1_type()

    def get_state_ids(self, signer_company_id: str) -> dict:
        return dict[get_key_id_key():concat_fqid(signer_company_id, self.id)]


class KeyRevokeV1Schema(BaseSchema):
    # KeyRevokeV1Schema allows to serialize and deserialize KeyRevokeV1.

    __model__ = KeyRevokeV1
    id = fields.Str()
