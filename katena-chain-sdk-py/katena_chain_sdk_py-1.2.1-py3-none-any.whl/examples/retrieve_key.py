"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from examples.common.settings import Settings
from katena_chain_sdk_py.entity.account.keys import KeyV1Schema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.entity.api.tx_result import TxResultsSchema, TxResultSchema


def main():
    # Alice wants to retrieve a key and its related txs

    # Common Katena network information
    api_url = Settings.api_url

    # Alice Katena network information
    alice_company_bcid = Settings.Company.bcid

    # Create a Katena API helper
    transactor = Transactor(api_url)

    # Key id Alice wants to retrieve
    key_id = Settings.key_id

    try:
        #  Retrieve txs related to the key fqid
        tx_results = transactor.retrieve_key_txs(alice_company_bcid, key_id, 1, Settings.tx_per_page)

        print("Tx list :")
        println_json(tx_results, TxResultsSchema)

        # Retrieve the last tx related to the key fqid
        tx_result = transactor.retrieve_last_key_tx(alice_company_bcid, key_id)

        print("Last tx :")
        println_json(tx_result, TxResultSchema)

        # Retrieve the last state of a key with that fqid
        key = transactor.retrieve_key(alice_company_bcid, key_id)

        print("Key :")
        println_json(key, KeyV1Schema)
    except (ApiException, ClientException) as e:
        print(e)


main()
