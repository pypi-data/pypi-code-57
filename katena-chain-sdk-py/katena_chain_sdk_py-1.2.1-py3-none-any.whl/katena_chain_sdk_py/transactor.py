"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from typing import List
from datetime import datetime
from katena_chain_sdk_py.api.handler import Handler
from katena_chain_sdk_py.crypto.nacl.public_key import PublicKey as PublicKeyX25519
from katena_chain_sdk_py.crypto.ed25519.public_key import PublicKey as PublicKeyEd25519
from katena_chain_sdk_py.entity.tx_data_interface import TxData
from katena_chain_sdk_py.entity.api.tx_result import SendTxResult, TxResult, TxResults
from katena_chain_sdk_py.entity.certify.certificate import CertificateRawV1, CertificateEd25519V1
from katena_chain_sdk_py.entity.certify.secret import SecretNaclBoxV1
from katena_chain_sdk_py.entity.account.keys import KeyV1, KeyCreateV1, KeyRotateV1, KeyRevokeV1
from katena_chain_sdk_py.entity.tx_signer import TxSigner
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.utils.common import concat_fqid


class Transactor:
    # Transactor provides methods to hide the complexity of Tx creation, Tx signature and API dialog.

    def __init__(self, api_url: str, chain_id: str = "", tx_signer: TxSigner = None):
        self.api_handler = Handler(api_url)
        self.chain_id = chain_id
        self.tx_signer = tx_signer

    def send_certificate_raw_v1_tx(self, id: str, value: bytes) -> SendTxResult:
        # Creates a CertificateRaw (V1) and sends it to the API.
        certificate = CertificateRawV1(id, value)
        return self.send_tx(certificate)

    def send_certificate_ed25519_v1_tx(self, id: str, signer: PublicKeyEd25519, signature: bytes) -> SendTxResult:
        # Creates a CertificateEd25519 (V1) and sends it to the API.
        certificate = CertificateEd25519V1(id, signer, signature)
        return self.send_tx(certificate)

    def send_secret_nacl_box_v1_tx(self, id: str, sender: PublicKeyX25519, nonce: bytes,
                                   content: bytes) -> SendTxResult:
        # Creates a SecretNaclBox (V1) and sends it to the API.
        secret = SecretNaclBoxV1(id, content, nonce, sender)
        return self.send_tx(secret)

    def send_key_create_v1_tx(self, id: str, key: PublicKeyEd25519, role: str) -> SendTxResult:
        # Creates a KeyCreate (V1) and sends it to the API.
        key_create = KeyCreateV1(id, key, role)
        return self.send_tx(key_create)

    def send_key_rotate_v1_tx(self, id: str, key: PublicKeyEd25519) -> SendTxResult:
        # Creates a KeyRotate (V1) and sends it to the API.
        key_create = KeyRotateV1(id, key)
        return self.send_tx(key_create)

    def send_key_revoke_v1_tx(self, id: str) -> SendTxResult:
        # Creates a KeyRevoke (V1) and sends it to the API.
        key_revoke = KeyRevokeV1(id)
        return self.send_tx(key_revoke)

    def send_tx(self, tx_data: TxData) -> SendTxResult:
        # Creates a tx from a tx data and the provided tx signer info and chain id, signs it, encodes it and sends it
        # to the api.
        if self.tx_signer is None or self.tx_signer.get_key_id() == "" or self.tx_signer.get_private_key() is None or self.chain_id == "":
            raise ClientException("impossible to create txs without a tx signer info or chain id")

        tx = self.api_handler.sign_tx(self.tx_signer, self.chain_id, datetime.utcnow(), tx_data)
        return self.api_handler.send_tx(tx)

    def retrieve_certificate_txs(self, company_id, id: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API and returns all txs related to a certificate fqid.
        return self.api_handler.retrieve_certificate_txs(concat_fqid(company_id, id), page, tx_per_page)

    def retrieve_last_certificate_tx(self, company_id, id: str) -> TxResult:
        # Fetches the API and returns the last tx related to a certificate fqid.
        return self.api_handler.retrieve_last_certificate_tx(concat_fqid(company_id, id))

    def retrieve_secret_txs(self, company_id, id: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API and returns all txs related to a secret fqid.
        return self.api_handler.retrieve_secret_txs(concat_fqid(company_id, id), page, tx_per_page)

    def retrieve_last_secret_tx(self, company_id, id: str) -> TxResult:
        # Fetches the API and returns the last tx related to a secret fqid.
        return self.api_handler.retrieve_last_secret_tx(concat_fqid(company_id, id))

    def retrieve_key_txs(self, company_id, id: str, page, tx_per_page: int) -> TxResults:
        # Fetches the API and returns all txs related to a key fqid.
        return self.api_handler.retrieve_key_txs(concat_fqid(company_id, id), page, tx_per_page)

    def retrieve_last_key_tx(self, company_id, id: str) -> TxResult:
        # Fetches the API and returns the last tx related to a key fqid.
        return self.api_handler.retrieve_last_key_tx(concat_fqid(company_id, id))

    def retrieve_tx(self, hash: str) -> TxResult:
        # Fetches the API and return any tx by its hash.
        return self.api_handler.retrieve_tx(hash)

    def retrieve_certificate(self, company_id, id: str) -> TxData:
        # Fetches the API and returns a certificate from the state.
        return self.api_handler.retrieve_certificate(concat_fqid(company_id, id))

    def retrieve_secret(self, company_id, id: str) -> TxData:
        # Fetches the API and returns a secret from the state.
        return self.api_handler.retrieve_secret(concat_fqid(company_id, id))

    def retrieve_key(self, company_id, id: str) -> KeyV1:
        # Fetches the API and returns a key from the state.
        return self.api_handler.retrieve_key(concat_fqid(company_id, id))

    def retrieve_company_keys(self, company_id: str, page, tx_per_page: int) -> List[KeyV1]:
        # Fetches the API and returns a list of keys for a company from the state.
        return self.api_handler.retrieve_company_keys(company_id, page, tx_per_page)
