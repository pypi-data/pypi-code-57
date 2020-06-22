"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from katena_chain_sdk_py.entity.api.tx_result import SendTxResultSchema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.entity.tx_signer import TxSigner
from katena_chain_sdk_py.utils.common import concat_fqid
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64
from examples.common.settings import Settings


def main():
    # Alice wants to certify raw off-chain information

    # Common Katena network information
    api_url = Settings.api_url
    chain_id = Settings.chain_id

    # Alice Katena network information
    alice_company_bcid = Settings.Company.bcid
    alice_sign_key_info = Settings.Company.ed25519_keys['alice']
    alice_sign_private_key = create_private_key_ed25519_from_base64(alice_sign_key_info.private_key_str)
    alice_sign_key_id = alice_sign_key_info.id

    # Create Katena API helpers
    tx_signer = TxSigner(concat_fqid(alice_company_bcid, alice_sign_key_id), alice_sign_private_key)
    transactor = Transactor(api_url, chain_id, tx_signer)

    # Off-chain information Alice wants to send
    certificate_id = Settings.certificate_id
    raw_data_signature = "off_chain_data_raw_signature_from_py"

    try:
        # Send a raw certificate, version 1, to Katena
        tx_result = transactor.send_certificate_raw_v1_tx(certificate_id, raw_data_signature.encode('utf-8'))

        print("Result :")
        println_json(tx_result, SendTxResultSchema)
    except (ApiException, ClientException) as e:
        print(e)


main()
