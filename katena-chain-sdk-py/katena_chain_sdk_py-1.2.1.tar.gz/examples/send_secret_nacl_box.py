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
from katena_chain_sdk_py.utils.crypto import create_private_key_ed25519_from_base64, \
    create_private_key_x25519_from_base64, create_public_key_x25519_from_base64
from examples.common.settings import Settings


def main():
    # Alice wants to send a nacl box secret to Bob to encrypt an off-chain data

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

    # Nacl box information (Alice encrypt data with its private key + recipient public key)
    alice_crypt_key_info = Settings.OffChain.x25519_keys['alice']
    alice_crypt_private_key = create_private_key_x25519_from_base64(alice_crypt_key_info.private_key_str)
    bob_crypt_key_info = Settings.OffChain.x25519_keys['bob']
    bob_crypt_public_key = create_public_key_x25519_from_base64(bob_crypt_key_info.public_key_str)

    # Off-chain information Alice wants to send to Bob
    secret_id = Settings.secret_id
    content = "off_chain_secret_to_crypt_from_py"

    # Alice uses its private key and Bob's public key to encrypt the message
    encrypted_message, nonce = alice_crypt_private_key.seal(content.encode("utf-8"), bob_crypt_public_key)

    try:
        # Send a version 1 of a secret nacl box on Katena
        tx_result = transactor.send_secret_nacl_box_v1_tx(secret_id, alice_crypt_private_key.get_public_key(), nonce,
                                                          encrypted_message)

        print("Result :")
        println_json(tx_result, SendTxResultSchema)
    except (ApiException, ClientException) as e:
        print(e)


main()
