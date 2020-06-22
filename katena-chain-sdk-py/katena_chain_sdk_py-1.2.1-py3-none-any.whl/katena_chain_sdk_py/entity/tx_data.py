"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

import typing
from marshmallow import types, fields
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.entity.certify.certificate import CertificateRawV1Schema, CertificateEd25519V1Schema
from katena_chain_sdk_py.entity.certify.common import get_certificate_raw_v1_type, get_certificate_ed25519_v1_type, \
    get_secret_nacl_box_v1_type
from katena_chain_sdk_py.entity.certify.secret import SecretNaclBoxV1Schema
from katena_chain_sdk_py.entity.account.keys import KeyCreateV1Schema, KeyRotateV1Schema, KeyRevokeV1Schema
from katena_chain_sdk_py.entity.account.common import get_key_create_v1_type, get_key_rotate_v1_type, \
    get_key_revoke_v1_type


def get_available_types() -> typing.Dict[str, BaseSchema]:
    return {
        get_certificate_raw_v1_type(): CertificateRawV1Schema(),
        get_certificate_ed25519_v1_type(): CertificateEd25519V1Schema(),
        get_secret_nacl_box_v1_type(): SecretNaclBoxV1Schema(),
        get_key_create_v1_type(): KeyCreateV1Schema(),
        get_key_rotate_v1_type(): KeyRotateV1Schema(),
        get_key_revoke_v1_type(): KeyRevokeV1Schema(),
    }


class UnknownTxData(TxData):
    # UnknownTxData is useful to load and dump back a tx data of unknown type.

    def __init__(self, type: str, value: dict):
        self.type = type
        self.value = value

    def get_type(self) -> str:
        return self.type

    def get_value(self) -> dict:
        return self.value

    def get_namespace(self) -> str:
        return ""

    def get_state_ids(self, signer_company_id: str) -> dict:
        return dict()


class UnknownTxDataSchema(BaseSchema):
    # UnknownTxDataSchema allows to serialize and deserialize UnknownTxData.

    __model__ = UnknownTxData
    type = fields.Str()
    value = fields.Raw()


class TxDataSchema(BaseSchema):
    # TxDataSchema allows to serialize and deserialize TxData.

    unknown_tx_data_schema = UnknownTxDataSchema()

    def dump(self, obj: typing.Any, *, many: bool = None) -> dict:
        available_types = get_available_types()
        obj_type = obj.get_type()
        if obj_type in available_types:
            return {
                'type': obj_type,
                'value': available_types[obj_type].dump(obj, many=many)
            }
        return self.unknown_tx_data_schema.dump(obj, many=many)

    def load(
            self,
            data: typing.Mapping,
            *,
            many: bool = None,
            partial: typing.Union[bool, types.StrSequenceOrSet] = None,
            unknown: str = None
    ) -> typing.Any:
        available_types = get_available_types()
        obj_type = data["type"]
        if obj_type in available_types:
            return available_types[obj_type].load(data["value"], many=many, partial=partial, unknown=unknown)
        return self.unknown_tx_data_schema.load(data, many=many, partial=partial, unknown=unknown)
