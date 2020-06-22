"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from http import HTTPStatus
from typing import List
from datetime import datetime
from katena_chain_sdk_py.api.client import Client
from katena_chain_sdk_py.entity.api.tx_result import SendTxResult
from katena_chain_sdk_py.entity.api.tx_result import TxResult, TxResultSchema
from katena_chain_sdk_py.entity.api.tx_result import TxResults, TxResultsSchema
from katena_chain_sdk_py.entity.api.tx_result import SendTxResultSchema
from katena_chain_sdk_py.entity.tx import Tx, TxSchema
from katena_chain_sdk_py.entity.tx_data import TxDataSchema
from katena_chain_sdk_py.entity.tx_signer import TxSigner
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.entity.tx_data_state import TxDataState, TxDataStateSchema
from katena_chain_sdk_py.exceptions.api_exception import ApiExceptionSchema
from katena_chain_sdk_py.entity.account.keys import KeyV1Schema, KeyV1
from katena_chain_sdk_py.utils.common import get_pagination_query_params


class Handler:
    # Handler provides helper methods to send and retrieve tx without directly interacting with the HTTP Client.
    LAST_PATH = "last"
    STATE_PATH = "state"
    TXS_PATH = "txs"
    CERTIFICATES_PATH = "certificates"
    SECRETS_PATH = "secrets"
    COMPANIES_PATH = "companies"
    KEYS_PATH = "keys"

    def __init__(self, api_url: str):
        self.api_client = Client(api_url)
        self.tx_schema = TxSchema()
        self.send_tx_result_schema = SendTxResultSchema()
        self.tx_result_schema = TxResultSchema()
        self.tx_results_schema = TxResultsSchema()
        self.api_exception_schema = ApiExceptionSchema()
        self.key_v1_schema = KeyV1Schema()
        self.tx_data_schema = TxDataSchema()
        self.tx_data_state_schema = TxDataStateSchema()

    def retrieve_certificate_txs(self, fqid: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API to return all txs related to a certificate fqid.
        query_params = get_pagination_query_params(page, tx_per_page)
        response = self.api_client.get("{}/{}".format(self.CERTIFICATES_PATH, fqid), query_params)
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_results_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_last_certificate_tx(self, fqid: str) -> TxResult:
        # Fetches the API to return the last tx related to a certificate fqid.
        response = self.api_client.get("{}/{}/{}".format(self.CERTIFICATES_PATH, fqid, self.LAST_PATH))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_result_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_secret_txs(self, fqid: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API to return all txs related to a secret fqid.
        query_params = get_pagination_query_params(page, tx_per_page)
        response = self.api_client.get("{}/{}".format(self.SECRETS_PATH, fqid), query_params)
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_results_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_last_secret_tx(self, fqid: str) -> TxResult:
        # Fetches the API to return the last tx related to a secret fqid.
        response = self.api_client.get("{}/{}/{}".format(self.SECRETS_PATH, fqid, self.LAST_PATH))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_result_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_key_txs(self, fqid: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API to return all txs related to a key fqid.
        query_params = get_pagination_query_params(page, tx_per_page)
        response = self.api_client.get("{}/{}".format(self.KEYS_PATH, fqid), query_params)
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_results_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_last_key_tx(self, fqid: str) -> TxResult:
        # Fetches the API to return the last tx related to a key fqid.
        response = self.api_client.get("{}/{}/{}".format(self.KEYS_PATH, fqid, self.LAST_PATH))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_result_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_tx(self, hash: str) -> TxResult:
        # Fetches the API to return any tx by its hash.
        response = self.api_client.get("{}/{}".format(self.TXS_PATH, hash))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_result_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_certificate(self, fqid: str) -> TxData:
        # Fetches the API and returns a certificate from the state.
        response = self.api_client.get("{}/{}/{}".format(self.STATE_PATH, self.CERTIFICATES_PATH, fqid))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_data_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_secret(self, fqid: str) -> TxData:
        # Fetches the API and returns a secret from the state.
        response = self.api_client.get("{}/{}/{}".format(self.STATE_PATH, self.SECRETS_PATH, fqid))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.tx_data_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_key(self, fqid: str) -> KeyV1:
        # Fetches the API and returns a key from the state.
        response = self.api_client.get("{}/{}/{}".format(self.STATE_PATH, self.KEYS_PATH, fqid))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.key_v1_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def retrieve_company_keys(self, company_bcid: str, page, tx_per_page: int) -> List[KeyV1]:
        # Fetches the API and returns a list of keys for a company from the state.
        query_params = get_pagination_query_params(page, tx_per_page)
        response = self.api_client.get(
            "{}/{}/{}/{}".format(self.STATE_PATH, self.COMPANIES_PATH, company_bcid, self.KEYS_PATH), query_params)
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.OK:
            return self.key_v1_schema.loads(json_body, many=True)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def send_tx(self, tx: Tx) -> SendTxResult:
        # Accepts an encoded tx and sends it to the Api to return its status and its hash.
        response = self.api_client.post(self.TXS_PATH, body=self.tx_schema.dumps(tx))
        json_body = response.get_body().decode("utf-8")
        if response.get_status_code() == HTTPStatus.ACCEPTED:
            return self.send_tx_result_schema.loads(json_body)
        else:
            raise self.api_exception_schema.loads(json_body, unknown="EXCLUDE")

    def sign_tx(self, tx_signer: TxSigner, chain_id: str, nonce_time: datetime, tx_data: TxData) -> Tx:
        # Creates a tx data state, signs it and returns a tx ready to be encoded and sent.
        tx_data_state = self.get_tx_data_state(chain_id, nonce_time, tx_data)
        tx_signature = tx_signer.get_private_key().sign(tx_data_state)
        return Tx(nonce_time, tx_data, tx_signer.get_key_id(), tx_signature)

    def get_tx_data_state(self, chain_id: str, nonce_time: datetime, tx_data: TxData) -> bytes:
        # Returns the sorted and marshaled json representation of a TxData ready to be signed.
        tx_data_state = TxDataState(chain_id, nonce_time, tx_data)
        return self.tx_data_state_schema.dumps(tx_data_state).encode("utf-8")
