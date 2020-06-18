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
import datetime
from decimal import Decimal
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import Contract
from moneyonchain.rrc20 import RRC20MoCState, \
    RRC20MoCInrate, \
    RRC20MoCExchange, \
    RRC20MoCSettlement, \
    RRC20MoCConnector, \
    RRC20MoC, \
    RRC20MoCMedianizer, \
    RRC20PriceFeed, \
    RRC20MoCHelperLib, \
    RRC20MoCBurnout, \
    RRC20MoCBProxManager, \
    RRC20MoCConverter, \
    RRC20FeedFactory
from moneyonchain.token import RIFPro, RIFDoC, RIF


STATE_LIQUIDATED = 0
STATE_BPRO_DISCOUNT = 1
STATE_BELOW_COBJ = 2
STATE_ABOVE_COBJ = 3


class RDOCPriceFeed(RRC20PriceFeed):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/PriceFeed.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18


class RDOCFeedFactory(RRC20FeedFactory):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/FeedFactory.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/FeedFactory.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18


class RDOCMoCMedianizer(RRC20MoCMedianizer):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCMedianizer.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18


class RDOCMoCState(RRC20MoCState):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCState.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCState.bin'))

    mode = 'RRC20'
    project = 'RDoC'
    precision = 10 ** 18


class RDOCMoCInrate(RRC20MoCInrate):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCInrate.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCInrate.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCBurnout(RRC20MoCBurnout):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCBurnout.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCBurnout.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCBProxManager(RRC20MoCBProxManager):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCRiskProxManager.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCRiskProxManager.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCConverter(RRC20MoCConverter):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCConverter.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCConverter.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCHelperLib(RRC20MoCHelperLib):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCHelperLib.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCHelperLib.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCExchange(RRC20MoCExchange):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCExchange.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCSettlement(RRC20MoCSettlement):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCSettlement.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCSettlement.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoCConnector(RRC20MoCConnector):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCConnector.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoCConnector.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'


class RDOCMoC(RRC20MoC):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoC.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rdoc/MoC.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RDoC'
    minimum_amount = Decimal(0.00000001)

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None,
                 contract_address_moc_state=None,
                 contract_address_moc_inrate=None,
                 contract_address_moc_exchange=None,
                 contract_address_moc_connector=None,
                 contract_address_moc_settlement=None,
                 contract_address_moc_bpro_token=None,
                 contract_address_moc_doc_token=None,
                 contract_address_reserve_token=None):

        network = connection_manager.network
        if not contract_address:
            # load from connection manager
            contract_address = connection_manager.options['networks'][network]['addresses']['MoC']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # load main contract
        self.load_contract()

        # load contract moc connector
        self.sc_moc_connector = self.load_moc_connector_contract(contract_address_moc_connector)

        # load contract moc state
        self.sc_moc_state = self.load_moc_state_contract(contract_address_moc_state)

        # load contract moc inrate
        self.sc_moc_inrate = self.load_moc_inrate_contract(contract_address_moc_inrate)

        # load contract moc exchange
        self.sc_moc_exchange = self.load_moc_exchange_contract(contract_address_moc_exchange)

        # load contract moc settlement
        self.sc_moc_settlement = self.load_moc_settlement_contract(contract_address_moc_settlement)

        # load contract moc bpro_token
        self.sc_moc_bpro_token = self.load_moc_bpro_token_contract(contract_address_moc_bpro_token)

        # load contract moc doc_token
        self.sc_moc_doc_token = self.load_moc_bpro_token_contract(contract_address_moc_doc_token)

        # load_reserve_token_contract
        self.sc_reserve_token = self.load_reserve_token_contract(contract_address_reserve_token)

    def load_moc_inrate_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        sc = RDOCMoCInrate(self.connection_manager,
                           contract_address=contract_address)

        return sc

    def load_moc_state_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        sc = RDOCMoCState(self.connection_manager,
                          contract_address=contract_address)

        return sc

    def load_moc_exchange_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCExchange']

        sc = RDOCMoCExchange(self.connection_manager,
                             contract_address=contract_address)

        return sc

    def load_moc_connector_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCConnector']

        sc = RDOCMoCConnector(self.connection_manager,
                              contract_address=contract_address)

        return sc

    def load_moc_settlement_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']

        sc = RDOCMoCSettlement(self.connection_manager,
                               contract_address=contract_address)

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['BProToken']

        sc = RIFPro(self.connection_manager,
                    contract_address=contract_address)

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['DoCToken']

        sc = RIFDoC(self.connection_manager,
                    contract_address=contract_address)

        return sc

    def load_reserve_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['ReserveToken']

        sc = RIF(self.connection_manager,
                 contract_address=contract_address)

        return sc
