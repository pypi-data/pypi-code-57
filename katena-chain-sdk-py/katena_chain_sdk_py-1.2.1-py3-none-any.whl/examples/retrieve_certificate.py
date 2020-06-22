"""
Copyright (c) 2019, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

from examples.common.log import println_json
from examples.common.settings import Settings
from katena_chain_sdk_py.entity.tx_data import TxDataSchema
from katena_chain_sdk_py.exceptions.api_exception import ApiException
from katena_chain_sdk_py.exceptions.client_exception import ClientException
from katena_chain_sdk_py.transactor import Transactor
from katena_chain_sdk_py.entity.api.tx_result import TxResultsSchema, TxResultSchema


def main():
    # Alice wants to retrieve txs related to a certificate

    # Common Katena network information
    api_url = Settings.api_url

    # Alice Katena network information
    alice_company_bcid = Settings.Company.bcid

    # Create a Katena API helper
    transactor = Transactor(api_url)

    # Certificate id Alice wants to retrieve
    certificate_id = Settings.certificate_id

    try:
        # Retrieve txs related to the certificate fqid
        tx_results = transactor.retrieve_certificate_txs(alice_company_bcid, certificate_id, 1, Settings.tx_per_page)

        print("Tx list :")
        println_json(tx_results, TxResultsSchema)

        # Retrieve the last tx related to the certificate fqid
        tx_result = transactor.retrieve_last_certificate_tx(alice_company_bcid, certificate_id)

        print("Last tx :")
        println_json(tx_result, TxResultSchema)

        # Retrieve the last state of a certificate with that fqid
        certificate = transactor.retrieve_certificate(alice_company_bcid, certificate_id)

        print("Certificate :")
        println_json(certificate, TxDataSchema)
    except (ApiException, ClientException) as e:
        print(e)


main()
