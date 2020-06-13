"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import logging
import os
from web3 import Web3
from web3.types import BlockIdentifier
from moneyonchain.contract import Contract


class CoinPairPrice(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CoinPairPrice.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/CoinPairPrice.bin'))

    mode = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['CoinPairPrice']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def price(self, formatted: bool = True,
              block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.functions.peek().call(
            block_identifier=block_identifier)

        if not result[1]:
            raise Exception("No source value price")

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price
