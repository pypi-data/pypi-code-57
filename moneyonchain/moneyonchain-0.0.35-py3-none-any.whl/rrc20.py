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
from moneyonchain.moc import MoCState, \
    MoCInrate, \
    MoCExchange, \
    MoCSettlement, \
    MoCConnector, \
    MoC, \
    MoCMedianizer, \
    PriceFeed, \
    MoCHelperLib, \
    MoCBurnout, \
    MoCBProxManager, \
    MoCConverter, \
    FeedFactory
from moneyonchain.token import RiskProToken, StableToken, ReserveToken


STATE_LIQUIDATED = 0
STATE_BPRO_DISCOUNT = 1
STATE_BELOW_COBJ = 2
STATE_ABOVE_COBJ = 3


class RRC20PriceFeed(PriceFeed):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/PriceFeed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/PriceFeed.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18


class RRC20FeedFactory(FeedFactory):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/FeedFactory.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/FeedFactory.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18


class RRC20MoCMedianizer(MoCMedianizer):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCMedianizer.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCMedianizer.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18


class RRC20MoCState(MoCState):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCState.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCState.bin'))

    mode = 'RRC20'
    project = 'RRC20'
    precision = 10 ** 18

    def collateral_reserves(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """RiskProx values and interests holdings"""

        result = self.sc.functions.collateralReserves().call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result


class RRC20MoCInrate(MoCInrate):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCInrate.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCInrate.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'

    def stable_inrate(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate Stable"""

        info = dict()

        result = self.sc.functions.getStableTmax().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['StableTmax'] = result

        result = self.sc.functions.getStablePower().call(
            block_identifier=block_identifier)
        info['StablePower'] = result

        result = self.sc.functions.getStableTmin().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['StableTmin'] = result

        return info

    def riskprox_inrate(self, formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """Parameters inrate riskprox"""

        info = dict()

        result = self.sc.functions.getRiskProxTmax().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['RiskProxTmax'] = result

        result = self.sc.functions.getRiskProxPower().call(
            block_identifier=block_identifier)
        info['RiskProxPower'] = result

        result = self.sc.functions.getRiskProxTmin().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')
        info['RiskProxTmin'] = result

        return info


class RRC20MoCBurnout(MoCBurnout):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCBurnout.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCBurnout.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCBProxManager(MoCBProxManager):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCRiskProxManager.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCRiskProxManager.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCConverter(MoCConverter):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCConverter.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCConverter.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCHelperLib(MoCHelperLib):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCHelperLib.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCHelperLib.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCExchange(MoCExchange):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCExchange.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCSettlement(MoCSettlement):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCSettlement.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCSettlement.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoCConnector(MoCConnector):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCConnector.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoCConnector.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'


class RRC20MoC(MoC):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoC.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_rrc20/MoC.bin'))

    precision = 10 ** 18
    mode = 'RRC20'
    project = 'RRC20'
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

        sc = RRC20MoCInrate(self.connection_manager,
                            contract_address=contract_address)

        return sc

    def load_moc_state_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        sc = RRC20MoCState(self.connection_manager,
                           contract_address=contract_address)

        return sc

    def load_moc_exchange_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCExchange']

        sc = RRC20MoCExchange(self.connection_manager,
                              contract_address=contract_address)

        return sc

    def load_moc_connector_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCConnector']

        sc = RRC20MoCConnector(self.connection_manager,
                               contract_address=contract_address)

        return sc

    def load_moc_settlement_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']

        sc = RRC20MoCSettlement(self.connection_manager,
                                contract_address=contract_address)

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['BProToken']

        sc = RiskProToken(self.connection_manager,
                          contract_address=contract_address)

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['DoCToken']

        sc = StableToken(self.connection_manager,
                         contract_address=contract_address)

        return sc

    def load_reserve_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['ReserveToken']

        sc = ReserveToken(self.connection_manager,
                          contract_address=contract_address)

        return sc

    def spendable_balance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Spendable Balance """

        result = self.sc.functions.getAllowance(account_address).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def reserve_allowance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Reserve allowance """

        result = self.sc_reserve_token.allowance(account_address,
                                                 self.sc.address,
                                                 formatted=formatted,
                                                 block_identifier=block_identifier)

        return result

