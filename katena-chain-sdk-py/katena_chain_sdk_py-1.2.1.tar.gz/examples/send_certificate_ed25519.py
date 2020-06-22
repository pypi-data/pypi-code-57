"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from examples.common.settings import Settings
from katena_chain_sdk_py.entity.api.tx_result import SendTxResultSchema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.entity.tx_signer import TxSigner
from katena_chain_sdk_py.utils.common import concat_fqid
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64


def main():
    # Alice wants to certify an ed25519 signature of an off-chain data

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
    david_sign_key_info = Settings.OffChain.ed25519_keys['david']
    david_sign_private_key = create_private_key_ed25519_from_base64(david_sign_key_info.private_key_str)
    data_signature = david_sign_private_key.sign("off_chain_data_to_sign_from_py".encode("utf-8"))

    try:
        # Send a version 1 of a certificate ed25519 on Katena
        tx_result = transactor.send_certificate_ed25519_v1_tx(certificate_id, alice_sign_private_key.get_public_key(),
                                                              data_signature)

        print("Result :")
        println_json(tx_result, SendTxResultSchema)
    except (ApiException, ClientException) as e:
        print(e)


main()
