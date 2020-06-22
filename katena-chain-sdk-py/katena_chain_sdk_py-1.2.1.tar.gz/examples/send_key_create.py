"""
Copyright (c) 2020, TransChain.

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
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64, generate_new_private_key_ed25519
from examples.common.settings import Settings
from katena_chain_sdk_py.entity.account.common import DEFAULT_ROLE_ID


def main():
    # Alice wants to create a key for its company

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

    # Information Alice want to send
    key_id = Settings.key_id
    new_private_key = generate_new_private_key_ed25519()
    new_public_key = new_private_key.get_public_key()

    # Choose role between DEFAULT_ROLE_ID or COMPANY_ADMIN_ROLE_ID
    role = DEFAULT_ROLE_ID

    try:
        # Send a version 1 of a key create on Katena
        tx_result = transactor.send_key_create_v1_tx(key_id, new_public_key, role)

        print("Result :")
        println_json(tx_result, SendTxResultSchema)
    except (ApiException, ClientException) as e:
        print(e)


main()
