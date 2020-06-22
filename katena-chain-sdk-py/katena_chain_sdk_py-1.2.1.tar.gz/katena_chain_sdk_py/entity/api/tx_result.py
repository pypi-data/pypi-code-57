"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from marshmallow import fields
from typing import List
from katena_chain_sdk_py.serializer.base_schema import BaseSchema
from katena_chain_sdk_py.entity.tx import Tx, TxSchema


class TxStatus:
    """ TxStatus is a tx blockchain status.
    0: OK
    1: PENDING
    >1: ERROR WITH CORRESPONDING CODE
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def get_code(self) -> int:
        return self.code

    def get_message(self) -> str:
        return self.message


class TxStatusSchema(BaseSchema):
    # TxStatusSchema allows to serialize and deserialize a TxStatus.

    __model__ = TxStatus
    code = fields.Int()
    message = fields.Str()


class SendTxResult:
    # SendTxResult is returned by a POST request to retrieve a Tx hash and its status

    def __init__(self, hash: str, status: TxStatus):
        self.hash = hash
        self.status = status

    def get_hash(self) -> str:
        return self.hash

    def get_status(self) -> TxStatus:
        return self.status


class SendTxResultSchema(BaseSchema):
    # SendTxResultSchema allows to serialize and deserialize SendTxResult.

    __model__ = SendTxResult
    hash = fields.Str()
    status = fields.Nested(TxStatusSchema)


class TxResult:
    # TxResult is returned by a GET request to retrieve a Tx with useful information about its processing

    def __init__(self, hash: str, height: int, index: int, tx: Tx, status: TxStatus):
        self.hash = hash
        self.height = height
        self.index = index
        self.status = status
        self.tx = tx

    def get_hash(self) -> str:
        return self.hash

    def get_height(self) -> int:
        return self.height

    def get_index(self) -> int:
        return self.index

    def get_status(self) -> TxStatus:
        return self.status

    def get_tx(self) -> Tx:
        return self.tx


class TxResultSchema(BaseSchema):
    # TxResultsSchema allows to serialize and deserialize TxResult.

    __model__ = TxResult
    hash = fields.Str()
    height = fields.Int()
    index = fields.Int()
    status = fields.Nested(TxStatusSchema)
    tx = fields.Nested(TxSchema)


class TxResults:
    # TxResults is returned by a GET request to retrieve a list of TxResult with the total txs available.

    def __init__(self, txs: List[TxResult], total: int):
        self.txs = txs
        self.total = total

    def get_txs(self) -> List[TxResult]:
        return self.txs

    def get_total(self) -> int:
        return self.total


class TxResultsSchema(BaseSchema):
    # TxResultsSchema allows to serialize and deserialize TxResults.

    __model__ = TxResults
    txs = fields.List(fields.Nested(TxResultSchema))
    total = fields.Int()
