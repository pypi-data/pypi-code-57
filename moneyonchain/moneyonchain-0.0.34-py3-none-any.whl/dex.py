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
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import Contract
from moneyonchain.admin import ProxyAdmin


class MoCDecentralizedExchange(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.bin'))

    mode = 'DEX'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['dex']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.connection_manager)
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def token_pairs(self, block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        result = self.sc.functions.getTokenPairs().call(
            block_identifier=block_identifier)

        return result

    def token_pairs_status(self, base_address, secondary_address,
                           block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        base_address = Web3.toChecksumAddress(base_address)
        secondary_address = Web3.toChecksumAddress(secondary_address)

        result = self.sc.functions.getTokenPairStatus(base_address,
                                                      secondary_address).call(
            block_identifier=block_identifier)

        if result:
            d_status = dict()
            d_status['emergentPrice'] = result[0]
            d_status['lastBuyMatchId'] = result[1]
            d_status['lastBuyMatchAmount'] = result[2]
            d_status['lastSellMatchId'] = result[3]
            d_status['tickNumber'] = result[4]
            d_status['nextTickBlock'] = result[5]
            d_status['lastTickBlock'] = result[6]
            d_status['lastClosingPrice'] = result[7]
            d_status['disabled'] = result[8]
            d_status['EMAPrice'] = result[9]
            d_status['smoothingFactor'] = result[10]

            return d_status

        return result

    def next_tick(self, pair, block_identifier: BlockIdentifier = 'latest'):
        """ Next tick """

        result = self.sc.functions.getNextTick(pair[0], pair[1]).call(
            block_identifier=block_identifier)

        return result

    def run_tick_for_pair(self, pair,
                          gas_limit=3500000,
                          wait_timeout=240,
                          matching_steps=70,
                          default_account=None,
                          wait_receipt=True):
        """Run tick for pair """

        tx_hash = None
        tx_receipt = None

        block_number = self.connection_manager.block_number
        self.log.info('About to run tick for pair {0}'.format(pair))
        next_tick_info = self.next_tick(pair)
        block_of_next_tick = next_tick_info[1]

        self.log.info('BlockOfNextTick {0}, currentBlockNumber {1}'.format(
            block_of_next_tick, block_number))
        self.log.info('Is tick runnable? {0}'.format(
            block_of_next_tick <= block_number))
        if block_of_next_tick <= block_number:

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'matchOrders',
                                                              pair[0],
                                                              pair[1],
                                                              matching_steps,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            self.log.info(
                'Transaction hash of tick run {0}'.format(tx_hash.hex()))

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info(
                    "Tick runned correctly in Block  [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                        tx_receipt['blockNumber'],
                        Web3.toHex(tx_receipt['transactionHash']),
                        tx_receipt['gasUsed'],
                        tx_receipt['from']))

        else:
            self.log.info('Block of next tick has not been reached\n\n')

        return tx_hash, tx_receipt

    def run_orders_expiration_for_pair(self, pair, is_buy_order,
                                       hint=0,
                                       order_id=0,
                                       gas_limit=3500000,
                                       wait_timeout=240,
                                       matching_steps=70,
                                       default_account=None,
                                       wait_receipt=True):
        """Run order expiration """

        tx_hash = None
        tx_receipt = None

        block_number = self.connection_manager.block_number

        self.log.info('About to expire {0} orders for pair {1} in blockNumber {2}'.format('buy' if is_buy_order else 'sell',
                                                                                          pair, block_number))

        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'processExpired',
                                                          pair[0],
                                                          pair[1],
                                                          is_buy_order,
                                                          hint,
                                                          order_id,
                                                          matching_steps,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        self.log.info(
            'Transaction hash of {0} orders expiration {1}'.format('buy' if is_buy_order else 'sell',
                                                                   tx_hash.hex()))

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                          timeout=wait_timeout)

            self.log.info(
                "Orders expiration job finished in block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                    tx_receipt['blockNumber'],
                    Web3.toHex(tx_receipt['transactionHash']),
                    tx_receipt['gasUsed'],
                    tx_receipt['from']))

        return tx_hash, tx_receipt
