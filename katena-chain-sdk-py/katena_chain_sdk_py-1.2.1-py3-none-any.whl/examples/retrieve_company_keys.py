"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from examples.common.settings import Settings
from katena_chain_sdk_py.entity.account.keys import KeyV1Schema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor


def main():
    # Alice wants to retrieve the keys of its company

    # Common Katena network information
    api_url = Settings.api_url

    # Alice Katena network information
    alice_company_bcid = Settings.Company.bcid

    # Create a Katena API helper
    transactor = Transactor(api_url)

    try:
        # Retrieve the keys from Katena
        keys = transactor.retrieve_company_keys(alice_company_bcid, 1, Settings.tx_per_page)

        print("Keys list :")
        println_json(keys, KeyV1Schema, True)
    except (ApiException, ClientException) as e:
        print(e)


main()
