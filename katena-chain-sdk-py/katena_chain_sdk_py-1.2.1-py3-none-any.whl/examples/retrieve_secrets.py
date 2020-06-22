"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from katena_chain_sdk_py.entity.tx_data import TxDataSchema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.entity.api.tx_result import TxResultsSchema, TxResultSchema
from katena_chain_sdk_py.utils.crypto import create_private_key_x25519_from_base64
from examples.common.settings import Settings


def main():
    # Bob wants to read a nacl box secret from Alice to decrypt an off-chain data

    # Common Katena network information
    api_url = Settings.api_url

    # Alice Katena network information
    alice_company_bcid = Settings.Company.bcid

    # Create a Katena API helper
    transactor = Transactor(api_url)

    # Nacl box information
    bob_crypt_key_info = Settings.OffChain.x25519_keys["bob"]
    bob_crypt_private_key = create_private_key_x25519_from_base64(bob_crypt_key_info.private_key_str)

    # Secret id Bob wants to retrieve
    secret_id = Settings.secret_id

    try:
        # Retrieve txs related to the secret fqid
        tx_results = transactor.retrieve_secret_txs(alice_company_bcid, secret_id, 1, Settings.tx_per_page)

        print("Tx list :")
        println_json(tx_results, TxResultsSchema)

        # Retrieve the last tx related to the secret fqid
        tx_result = transactor.retrieve_last_secret_tx(alice_company_bcid, secret_id)

        print("Last tx :")
        println_json(tx_result, TxResultSchema)

        # Retrieve the last state of a secret with that fqid
        secret = transactor.retrieve_secret(alice_company_bcid, secret_id)

        print("Secret :")
        println_json(secret, TxDataSchema)

        # Bob will use its private key and the sender's public key (needs to be Alice's) to decrypt a message
        decrypted_content = bob_crypt_private_key.open(
            secret.get_content(),
            secret.get_sender(),
            secret.get_nonce()
        ).decode("utf-8")

        if decrypted_content == "":
            decrypted_content = "Unable to decrypt"

        print("Decrypted content : {}".format(decrypted_content))
    except (ApiException, ClientException) as e:
        print(e)


main()
