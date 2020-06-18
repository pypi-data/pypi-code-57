"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging

from web3.types import BlockIdentifier
from web3 import Web3
from moneyonchain.contract import Contract


class Governed(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/Governed.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        network = connection_manager.network
        if not contract_address:
            raise ValueError("You need to pass contract address")

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def governor(self, block_identifier: BlockIdentifier = 'latest'):
        """Contract address output"""

        result = self.sc.functions.governor().call(
            block_identifier=block_identifier)

        return result

    def initialize(self, governor,
                   gas_limit=3500000,
                   wait_timeout=240,
                   default_account=None,
                   wait_receipt=True):
        """Initialize"""

        governor_address = Web3.toChecksumAddress(governor)

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'initialize',
                                                          governor_address,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                          timeout=wait_timeout)

            self.log.info("Successfully initialized in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                tx_receipt['blockNumber'],
                Web3.toHex(tx_receipt['transactionHash']),
                tx_receipt['gasUsed'],
                tx_receipt['from']))

        return tx_hash, tx_receipt


class RDOCGoverned(Governed):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/Governed.bin'))

    mode = 'RDoC'
    precision = 10 ** 18
