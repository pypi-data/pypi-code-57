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
from moneyonchain.token import BProToken, DoCToken
from moneyonchain.events import MoCExchangeRiskProMint, \
    MoCExchangeStableTokenMint, \
    MoCExchangeRiskProxMint, \
    MoCExchangeRiskProRedeem, \
    MoCExchangeFreeStableTokenRedeem, \
    MoCExchangeRiskProxRedeem, \
    MoCSettlementRedeemRequestAlter
from moneyonchain.admin import ProxyAdmin


STATE_LIQUIDATED = 0
STATE_BPRO_DISCOUNT = 1
STATE_BELOW_COBJ = 2
STATE_ABOVE_COBJ = 3


class PriceFeed(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeed.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/PriceFeed.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None,
                 contract_address_moc_medianizer=None):

        network = connection_manager.network
        if not contract_address:
            # load from connection manager

            contract_address = connection_manager.options['networks'][network]['addresses']['PriceFeed']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        if not contract_address_moc_medianizer:
            contract_address_moc_medianizer = connection_manager.options['networks'][network]['addresses']['MoCMedianizer']

        self.contract_address_moc_medianizer = contract_address_moc_medianizer

        # finally load the contract
        self.load_contract()

    def post(self,
             p_price,
             block_expiration=300,
             gas_limit=3500000,
             wait_timeout=240,
             default_account=None,
             wait_receipt=True):
        """Post price """

        address_moc_medianizer = Web3.toChecksumAddress(self.contract_address_moc_medianizer)
        last_block = self.connection_manager.get_block('latest')
        expiration = last_block.timestamp + block_expiration

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'post',
                                                          int(p_price),
                                                          int(expiration),
                                                          address_moc_medianizer,
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                          timeout=wait_timeout)

            self.log.info("Successfully post price [{4}] in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                tx_receipt['blockNumber'],
                Web3.toHex(tx_receipt['transactionHash']),
                tx_receipt['gasUsed'],
                tx_receipt['from'],
                p_price))

        return tx_hash, tx_receipt

    def zzz(self, block_identifier: BlockIdentifier = 'latest'):
        """zzz"""

        result = self.sc.functions.zzz().call(
            block_identifier=block_identifier)

        return result

    def peek(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.functions.peek().call(
            block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]


class FeedFactory(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/FeedFactory.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/FeedFactory.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager,
                 contract_address=None,
                 contract_abi=None,
                 contract_bin=None):

        network = connection_manager.network
        if not contract_address:
            # load from connection manager

            contract_address = connection_manager.options['networks'][network]['addresses']['FeedFactory']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()


class MoCMedianizer(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCMedianizer.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCMedianizer']

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

    def peek(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.functions.peek().call(
            block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]

    def compute(self, formatted: bool = True,
                block_identifier: BlockIdentifier = 'latest'):
        """Get price"""

        result = self.sc.functions.compute().call(
            block_identifier=block_identifier)

        price = Web3.toInt(result[0])

        if formatted:
            price = Web3.fromWei(price, 'ether')

        return price, result[1]

    def indexes(self, feeder_address,
                block_identifier: BlockIdentifier = 'latest'):
        """Get index of the price feeder. Result > 0 is an active pricefeeder"""

        feeder_address = Web3.toChecksumAddress(feeder_address)

        result = self.sc.functions.indexes(feeder_address).call(
            block_identifier=block_identifier)

        return Web3.toInt(result)

    def poke(self,
             gas_limit=3500000,
             wait_timeout=240,
             default_account=None,
             wait_receipt=True):
        """Poke """

        tx_receipt = None
        tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                          'poke',
                                                          default_account=default_account,
                                                          gas_limit=gas_limit)

        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                          timeout=wait_timeout)

            self.log.info("Successfully poke in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                tx_receipt['blockNumber'],
                Web3.toHex(tx_receipt['transactionHash']),
                tx_receipt['gasUsed'],
                tx_receipt['from']))

        return tx_hash, tx_receipt


class MoCState(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCState.bin'))

    mode = 'MoC'
    project = 'MoC'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCState']

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

    def state(self, block_identifier: BlockIdentifier = 'latest'):
        """State of contract"""

        result = self.sc.functions.state().call(
            block_identifier=block_identifier)

        return result

    def day_block_span(self, block_identifier: BlockIdentifier = 'latest'):
        """State of contract"""

        result = self.sc.functions.dayBlockSpan().call(
            block_identifier=block_identifier)

        return result

    def rbtc_in_system(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """RBTC in system"""

        result = self.sc.functions.rbtcInSystem().call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def cobj(self, formatted: bool = True,
             block_identifier: BlockIdentifier = 'latest'):
        """cobj"""

        result = self.sc.functions.cobj().call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def cobj_X2(self, formatted: bool = True,
                block_identifier: BlockIdentifier = 'latest'):
        """cobj"""

        result = self.sc.functions.getBucketCobj(str.encode('X2')).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_mint_bpro_available(self, formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.functions.maxMintBProAvalaible().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.maxMintRiskProAvalaible().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def absolute_max_doc(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == "MoC":
            result = self.sc.functions.absoluteMaxDoc().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.absoluteMaxStableToken().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bprox(self, bucket,
                  formatted: bool = True,
                  block_identifier: BlockIdentifier = 'latest'):
        """Max BProX"""

        if self.mode == 'MoC':
            result = self.sc.functions.maxBProx(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.maxRiskProx(bucket).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bprox_btc_value(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        result = self.sc.functions.maxBProxBtcValue(str.encode('X2')).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def absolute_max_bpro(self, formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.functions.absoluteMaxBPro().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.absoluteMaxRiskPro().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def free_doc(self, formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """Max mint BPRo available"""

        if self.mode == 'MoC':
            result = self.sc.functions.freeDoc().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.freeStableToken().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def leverage(self, bucket,
                 formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """Leverage"""

        result = self.sc.functions.leverage(bucket).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_discount_rate(self,
                           formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """BPro discount rate"""

        if self.mode == 'MoC':
            result = self.sc.functions.bproSpotDiscountRate().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProSpotDiscountRate().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def max_bpro_with_discount(self,
                               formatted: bool = True,
                               block_identifier: BlockIdentifier = 'latest'):
        """Max BPro with discount"""

        if self.mode == 'MoC':
            result = self.sc.functions.maxBProWithDiscount().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.maxRiskProWithDiscount().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_discount_price(self,
                            formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """BPro discount price"""

        if self.mode == 'MoC':
            result = self.sc.functions.bproDiscountPrice().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProDiscountPrice().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def blocks_to_settlement(self, block_identifier: BlockIdentifier = 'latest'):
        """Blocks to settlement"""

        result = self.sc.functions.blocksToSettlement().call(
            block_identifier=block_identifier)

        return result

    def bitcoin_price(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin price in USD"""

        if self.mode == 'MoC':
            result = self.sc.functions.getBitcoinPrice().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.getReserveTokenPrice().call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_price(self, formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """BPro price in USD"""

        if self.mode == 'MoC':
            result = self.sc.functions.bproUsdPrice().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProUsdPrice().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bpro_tec_price(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """BPro Technical price in RBTC"""

        if self.mode == 'MoC':
            result = self.sc.functions.bproTecPrice().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProTecPrice().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bprox_price(self,
                    bucket=str.encode('X2'),
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """BProX price in RBTC"""

        if self.mode == "MoC":
            result = self.sc.functions.bproxBProPrice(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProxRiskProPrice(bucket).call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def btc2x_tec_price(self,
                        bucket=str.encode('X2'),
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """BTC2X Technical price in RBTC"""

        if self.mode == 'MoC':
            result = self.sc.functions.bucketBProTecPrice(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.bucketRiskProTecPrice(bucket).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitcoin_moving_average(self, formatted: bool = True,
                               block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin Moving Average price in USD"""

        if self.mode == 'MoC':
            result = self.sc.functions.getBitcoinMovingAverage().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.getExponentalMovingAverage().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def get_inrate_bag(self, bucket,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """Get inrate Bag"""

        result = self.sc.functions.getInrateBag(bucket).call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_nbtc(self, bucket,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Bucket NBTC"""

        if self.mode == "MoC":
            result = self.sc.functions.getBucketNBTC(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.getBucketNReserve(bucket).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_ndoc(self, bucket,
                    formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Bucket NDOC"""

        if self.mode == "MoC":
            result = self.sc.functions.getBucketNDoc(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.getBucketNStableToken(bucket).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bucket_nbpro(self, bucket,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """Bucket NBPRO"""

        if self.mode == "MoC":
            result = self.sc.functions.getBucketNBPro(bucket).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.getBucketNRiskPro(bucket).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def days_to_settlement(self, formatted: bool = True,
                           block_identifier: BlockIdentifier = 'latest'):
        """Days to settlement"""

        result = int(self.sc.functions.daysToSettlement().call(
            block_identifier=block_identifier))

        return result

    def coverage(self, bucket,
                 formatted: bool = True,
                 block_identifier: BlockIdentifier = 'latest'):
        """coverage"""

        result = self.sc.functions.coverage(bucket).call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def global_coverage(self, formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """Global coverage"""

        result = self.sc.functions.globalCoverage().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitpro_total_supply(self, formatted: bool = True,
                            block_identifier: BlockIdentifier = 'latest'):
        """Bitpro total supply"""

        if self.mode == 'MoC':
            result = self.sc.functions.bproTotalSupply().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProTotalSupply().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_total_supply(self, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """DOC total supply"""

        if self.mode == 'MoC':
            result = self.sc.functions.docTotalSupply().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.stableTokenTotalSupply().call(
                block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def is_liquidation(self, block_identifier: BlockIdentifier = 'latest'):
        """DOC total supply"""

        result = self.sc.functions.isLiquidationReached().call(
            block_identifier=block_identifier)

        return result

    def is_calculate_ema(self, block_identifier: BlockIdentifier = 'latest'):
        """Is time to calculate ema"""

        result = self.sc.functions.shouldCalculateEma().call(
            block_identifier=block_identifier)

        return result

    def execute_calculate_ema(self,
                              gas_limit=3500000,
                              wait_timeout=240,
                              default_account=None,
                              wait_receipt=True):
        """Execute calculate ema """

        tx_hash = None
        tx_receipt = None
        if self.is_calculate_ema():

            self.log.info("Calling calculateBitcoinMovingAverage ...")

            if self.mode == 'MoC':
                contract_function = 'calculateBitcoinMovingAverage'
            else:
                contract_function = 'calculateReserveTokenMovingAverage'

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              contract_function,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info(
                    "Successfully calculateBitcoinMovingAverage in Block  [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                        tx_receipt['blockNumber'],
                        Web3.toHex(tx_receipt['transactionHash']),
                        tx_receipt['gasUsed'],
                        tx_receipt['from']))

        return tx_hash, tx_receipt


class MoCInrate(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCInrate.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCInrate']

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

    def commision_rate(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """Gets commision rate"""

        result = self.sc.functions.getCommissionRate().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def bitpro_rate(self, formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """Gets the rate for BitPro Holders"""

        result = self.sc.functions.getBitProRate().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def daily_enabled(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.functions.isDailyEnabled().call(
            block_identifier=block_identifier)

        return result

    def daily_inrate(self, formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """returns the amount of BTC to pay in concept of interest"""

        result = self.sc.functions.dailyInrate().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def spot_inrate(self, formatted: bool = True,
                    block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.functions.spotInrate().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def commission_rate(self,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """"""

        result = self.sc.functions.getCommissionRate().call(
            block_identifier=block_identifier)
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def last_daily_pay(self, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """returns the amount of BTC to pay in concept of interest"""

        result = self.sc.functions.lastDailyPayBlock().call(
            block_identifier=block_identifier)

        return result

    def calc_commission_value(self, amount, formatted: bool = True):
        """ Calc commission value amount in ether float"""

        result = self.sc.functions.calcCommissionValue(int(amount * self.precision)).call()
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def calc_mint_interest_value(self, amount, formatted: bool = True, precision: bool = True):
        """ Calc interest value amount in ether float"""

        bucket = str.encode('X2')

        if precision:
            amount = int(amount * self.precision)
        result = self.sc.functions.calcMintInterestValues(bucket, int(amount)).call()
        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def calc_bitpro_holders_interest(self, formatted: bool = True,
                                     block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.functions.calculateBitProHoldersInterest().call(block_identifier=block_identifier)
        else:
            result = self.sc.functions.calculateRiskProHoldersInterest().call(block_identifier=block_identifier)

        if formatted:
            result = [Web3.fromWei(result[0], 'ether'), Web3.fromWei(result[1], 'ether')]

        return result

    def bitpro_interest_address(self, formatted: bool = True,
                                block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.functions.getBitProInterestAddress().call(block_identifier=block_identifier)
        else:
            result = self.sc.functions.getRiskProInterestAddress().call(block_identifier=block_identifier)

        return result

    def is_bitpro_interest_enabled(self, formatted: bool = True,
                                   block_identifier: BlockIdentifier = 'latest'):
        """ Calc bitpro holders interest"""

        if self.mode == 'MoC':
            result = self.sc.functions.isBitProInterestEnabled().call(block_identifier=block_identifier)
        else:
            result = self.sc.functions.isRiskProInterestEnabled().call(block_identifier=block_identifier)

        return result

    def doc_inrate_avg(self, amount, formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):
        """ Calculates an average interest rate between after and before free doc Redemption"""

        if self.mode == 'MoC':
            result = self.sc.functions.docInrateAvg(int(amount * self.precision)).call(block_identifier=block_identifier)
        else:
            result = self.sc.functions.stableTokenInrateAvg(int(amount * self.precision)).call(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def btc2x_inrate_avg(self, amount, on_minting=False, formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):
        """ Calculates an average interest rate between after and before mint/redeem """

        bucket = str.encode('X2')

        if self.mode == 'MoC':
            result = self.sc.functions.btcxInrateAvg(bucket, int(amount * self.precision), on_minting).call(block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProxInrateAvg(bucket, int(amount * self.precision), on_minting).call(block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result


class MoCExchange(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCExchange.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCExchange']

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


class MoCSettlement(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlement.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCSettlement.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCSettlement']

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

    def next_block(self):
        return int(self.sc.functions.nextSettlementBlock().call())

    def is_enabled(self):
        return self.sc.functions.isSettlementEnabled().call()

    def is_ready(self):
        return self.sc.functions.isSettlementReady().call()

    def is_running(self):
        return self.sc.functions.isSettlementRunning().call()

    def redeem_queue_size(self):
        return self.sc.functions.redeemQueueSize().call()

    def block_span(self, block_identifier: BlockIdentifier = 'latest'):
        return self.sc.functions.getBlockSpan().call(block_identifier=block_identifier)


class MoCBurnout(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBurnout.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBurnout.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):
        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCBurnout']

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


class MoCBProxManager(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBProxManager.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCBProxManager.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):
        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCBProxManager']

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


class MoCConverter(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConverter.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConverter.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):
        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCConverter']

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


class MoCHelperLib(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCHelperLib.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCHelperLib.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):
        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCHelperLib']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()


class MoCConnector(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoCConnector.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['MoCConnector']

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

    def contracts_addresses(self):

        d_addresses = dict()
        d_addresses['MoC'] = self.sc.functions.moc().call()
        d_addresses['MoCState'] = self.sc.functions.mocState().call()
        d_addresses['MoCConverter'] = self.sc.functions.mocConverter().call()
        d_addresses['MoCSettlement'] = self.sc.functions.mocSettlement().call()
        d_addresses['MoCExchange'] = self.sc.functions.mocExchange().call()
        d_addresses['MoCInrate'] = self.sc.functions.mocInrate().call()
        d_addresses['MoCBurnout'] = self.sc.functions.mocBurnout().call()
        if self.mode == 'MoC':
            d_addresses['DoCToken'] = self.sc.functions.docToken().call()
            d_addresses['BProToken'] = self.sc.functions.bproToken().call()
            d_addresses['MoCBProxManager'] = self.sc.functions.bproxManager().call()
        else:
            d_addresses['DoCToken'] = self.sc.functions.stableToken().call()
            d_addresses['BProToken'] = self.sc.functions.riskProToken().call()
            d_addresses['MoCBProxManager'] = self.sc.functions.riskProxManager().call()
            d_addresses['ReserveToken'] = self.sc.functions.reserveToken().call()

        return d_addresses


class MoC(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi/MoC.bin'))

    precision = 10 ** 18
    mode = 'MoC'
    project = 'MoC'
    minimum_amount = Decimal(0.00000001)
    receipt_timeout = 240
    poll_latency = 1.0

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
                 contract_address_moc_doc_token=None):

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

        # load contract moc state
        self.sc_moc_state = self.load_moc_state_contract(contract_address_moc_state)

        # load contract moc inrate
        self.sc_moc_inrate = self.load_moc_inrate_contract(contract_address_moc_inrate)

        # load contract moc exchange
        self.sc_moc_exchange = self.load_moc_exchange_contract(contract_address_moc_exchange)

        # load contract moc connector
        self.sc_moc_connector = self.load_moc_connector_contract(contract_address_moc_connector)

        # load contract moc settlement
        self.sc_moc_settlement = self.load_moc_settlement_contract(contract_address_moc_settlement)

        # load contract moc bpro_token
        self.sc_moc_bpro_token = self.load_moc_bpro_token_contract(contract_address_moc_bpro_token)

        # load contract moc doc_token
        self.sc_moc_doc_token = self.load_moc_doc_token_contract(contract_address_moc_doc_token)

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.connection_manager)
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def load_moc_inrate_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCInrate']

        sc = MoCInrate(self.connection_manager,
                       contract_address=contract_address)

        return sc

    def load_moc_state_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCState']

        sc = MoCState(self.connection_manager,
                      contract_address=contract_address)

        return sc

    def load_moc_exchange_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCExchange']

        sc = MoCExchange(self.connection_manager,
                         contract_address=contract_address)

        return sc

    def load_moc_connector_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCConnector']

        sc = MoCConnector(self.connection_manager,
                          contract_address=contract_address)

        return sc

    def load_moc_settlement_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']

        sc = MoCSettlement(self.connection_manager,
                           contract_address=contract_address)

        return sc

    def load_moc_bpro_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['BProToken']

        sc = BProToken(self.connection_manager,
                       contract_address=contract_address)

        return sc

    def load_moc_doc_token_contract(self, contract_address):

        network = self.connection_manager.network
        if not contract_address:
            contract_address = self.connection_manager.options['networks'][network]['addresses']['DoCToken']

        sc = DoCToken(self.connection_manager,
                      contract_address=contract_address)

        return sc

    def connector(self):

        return self.sc.functions.connector().call()

    def connector_addresses(self):

        return self.sc_moc_connector.contracts_addresses()

    def state(self):

        return self.sc_moc_state.state()

    def reserve_precision(self,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Precision """

        result = self.sc.functions.getReservePrecision().call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def sc_precision(self,
                     formatted: bool = True,
                     block_identifier: BlockIdentifier = 'latest'):
        """ Precision """

        result = self.sc.functions.getMocPrecision().call(
            block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def is_bucket_liquidation(self, block_identifier: BlockIdentifier = 'latest'):
        """Is bucket liquidation reached"""

        result = self.sc.functions.isBucketLiquidationReached(str.encode('X2')).call(
            block_identifier=block_identifier)

        return result

    def is_settlement_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is settlement enabled"""

        result = self.sc.functions.isSettlementEnabled().call(
            block_identifier=block_identifier)

        return result

    def is_daily_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is settlement enabled"""

        result = self.sc.functions.isDailyEnabled().call(
            block_identifier=block_identifier)

        return result

    def is_bitpro_interest_enabled(self, block_identifier: BlockIdentifier = 'latest'):
        """Is bitpro_interest enabled"""

        if self.mode == 'MoC':
            result = self.sc.functions.isBitProInterestEnabled().call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.isRiskProInterestEnabled().call(
                block_identifier=block_identifier)

        return result

    def execute_liquidation(self, execution_steps,
                            gas_limit=3500000,
                            wait_timeout=240,
                            default_account=None,
                            wait_receipt=True):
        """Execute liquidation """

        tx_hash = None
        tx_receipt = None
        if self.sc_moc_state.is_liquidation():

            self.log.info("Calling evalLiquidation steps [{0}] ...".format(execution_steps))

            # Only if is liquidation reach
            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'evalLiquidation',
                                                              execution_steps,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info("Successfully forced Liquidation in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                    tx_receipt['blockNumber'],
                    Web3.toHex(tx_receipt['transactionHash']),
                    tx_receipt['gasUsed'],
                    tx_receipt['from']))

        return tx_hash, tx_receipt

    def execute_bucket_liquidation(self,
                                   gas_limit=3500000,
                                   wait_timeout=240,
                                   default_account=None,
                                   wait_receipt=True):
        """Execute bucket liquidation """

        tx_hash = None
        tx_receipt = None
        if self.is_bucket_liquidation() and not self.is_settlement_enabled():

            self.log.info("Calling evalBucketLiquidation...")

            # Only if is liquidation reach
            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'evalBucketLiquidation',
                                                              str.encode('X2'),
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info(
                    "Successfully Bucket X2 Liquidation [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                        tx_receipt['blockNumber'],
                        Web3.toHex(tx_receipt['transactionHash']),
                        tx_receipt['gasUsed'],
                        tx_receipt['from']))

        return tx_hash, tx_receipt

    def execute_run_settlement(self, execution_steps,
                               gas_limit=3500000,
                               wait_timeout=240,
                               default_account=None,
                               wait_receipt=True):
        """Execute run settlement """

        tx_hash = None
        tx_receipt = None
        if self.is_settlement_enabled():

            self.log.info("Calling runSettlement steps [{0}] ...".format(execution_steps))

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'runSettlement',
                                                              execution_steps,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info("Successfully runSettlement in Block [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                    tx_receipt['blockNumber'],
                    Web3.toHex(tx_receipt['transactionHash']),
                    tx_receipt['gasUsed'],
                    tx_receipt['from']))

        return tx_hash, tx_receipt

    def execute_daily_inrate_payment(self,
                                     gas_limit=3500000,
                                     wait_timeout=240,
                                     default_account=None,
                                     wait_receipt=True):
        """Execute daily inrate """

        tx_hash = None
        tx_receipt = None
        if self.is_daily_enabled():

            self.log.info("Calling dailyInratePayment ...")

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              'dailyInratePayment',
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info("Successfully dailyInratePayment in Block  [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                                tx_receipt['blockNumber'],
                                Web3.toHex(tx_receipt['transactionHash']),
                                tx_receipt['gasUsed'],
                                tx_receipt['from']))

        return tx_hash, tx_receipt

    def execute_pay_bitpro_holders(self,
                                   gas_limit=3500000,
                                   wait_timeout=240,
                                   default_account=None,
                                   wait_receipt=True):
        """Execute pay bitpro holders """

        tx_hash = None
        tx_receipt = None
        if self.is_bitpro_interest_enabled():

            self.log.info("Calling payBitProHoldersInterestPayment ...")

            if self.mode == 'MoC':
                contract_function = 'payBitProHoldersInterestPayment'
            else:
                contract_function = 'payRiskProHoldersInterestPayment'

            tx_hash = self.connection_manager.fnx_transaction(self.sc,
                                                              contract_function,
                                                              default_account=default_account,
                                                              gas_limit=gas_limit)

            if wait_receipt:
                # wait to transaction be mined
                tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash,
                                                                              timeout=wait_timeout)

                self.log.info("Successfully payBitProHoldersInterestPayment in Block  [{0}] Hash: [{1}] Gas used: [{2}] From: [{3}]".format(
                                tx_receipt['blockNumber'],
                                Web3.toHex(tx_receipt['transactionHash']),
                                tx_receipt['gasUsed'],
                                tx_receipt['from']))

        return tx_hash, tx_receipt

    def execute_calculate_ema(self,
                              gas_limit=3500000,
                              wait_timeout=240,
                              default_account=None,
                              wait_receipt=True):
        """Execute calculate ema """

        tx_hash, tx_receipt = self.sc_moc_state.execute_calculate_ema(
            gas_limit=gas_limit,
            wait_timeout=wait_timeout,
            default_account=default_account,
            wait_receipt=wait_receipt)

        return tx_hash, tx_receipt

    def max_mint_bpro_available(self):

        return self.sc_moc_state.max_mint_bpro_available()

    def absolute_max_doc(self):

        return self.sc_moc_state.absolute_max_doc()

    def max_bprox_btc_value(self):

        return self.sc_moc_state.max_bprox_btc_value()

    def absolute_max_bpro(self):

        return self.sc_moc_state.absolute_max_bpro()

    def free_doc(self):

        return self.sc_moc_state.free_doc()

    def settlement_info(self, avg_block_time=30.0):

        def convert(seconds):
            min, sec = divmod(seconds, 60)
            hour, min = divmod(min, 60)
            return "%d:%02d:%02d" % (hour, min, sec)

        blocks_to_settlement = self.sc_moc_state.blocks_to_settlement()

        l_sett = list()
        l_sett.append(('Current Block', int(self.connection_manager.block_number)))
        l_sett.append(('Current avg block time (seconds)', 30.0))
        l_sett.append(('Blocks to settlement', blocks_to_settlement))
        l_sett.append(('Days to settlement', self.sc_moc_state.days_to_settlement()))

        remainin_estimated_seconds = avg_block_time * blocks_to_settlement
        estimated_time = datetime.datetime.now() + datetime.timedelta(seconds=remainin_estimated_seconds)

        l_sett.append(('Estimated remaining to settlement', convert(remainin_estimated_seconds)))
        l_sett.append(('Estimated settlement', estimated_time.strftime("%Y-%m-%d %H:%M:%S")))
        l_sett.append(('Next settlement block', self.sc_moc_settlement.next_block()))
        l_sett.append(('Is settlement enabled', self.sc_moc_settlement.is_enabled()))
        l_sett.append(('Is settlement ready', self.sc_moc_settlement.is_ready()))
        l_sett.append(('Is settlement running', self.sc_moc_settlement.is_running()))
        l_sett.append(('Reedem queue size', self.sc_moc_settlement.redeem_queue_size()))
        l_sett.append(('Block Span', self.sc_moc_settlement.block_span()))

        return l_sett

    def bitcoin_price(self, formatted: bool = True,
                      block_identifier: BlockIdentifier = 'latest'):
        """Bitcoin price in USD"""

        result = self.sc_moc_state.bitcoin_price(formatted=formatted,
                                                 block_identifier=block_identifier)

        return result

    def bpro_price(self, formatted: bool = True,
                   block_identifier: BlockIdentifier = 'latest'):
        """BPro price in USD"""

        result = self.sc_moc_state.bpro_price(formatted=formatted,
                                              block_identifier=block_identifier)

        return result

    def btc2x_tec_price(self, formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):
        """BTC2x price in USD"""

        result = self.sc_moc_state.btc2x_tec_price(formatted=formatted,
                                                   block_identifier=block_identifier)

        return result

    def bpro_amount_in_usd(self, amount: Decimal):

        return self.bpro_price() * amount

    def btc2x_amount_in_usd(self, amount: Decimal):

        return self.btc2x_tec_price() * self.bitcoin_price() * amount

    def balance_of(self, default_account=None):

        if not default_account:
            default_account = 0

        return self.connection_manager.balance(
            self.connection_manager.accounts[default_account].address)

    def rbtc_balance_of(self,
                        account_address,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):

        result = self.connection_manager.balance(account_address)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def spendable_balance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Compatibility function see RRC20 """

        result = self.connection_manager.balance(account_address)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def reserve_allowance(self,
                          account_address,
                          formatted: bool = True,
                          block_identifier: BlockIdentifier = 'latest'):
        """ Compatibility function see RRC20 """

        result = self.connection_manager.balance(account_address)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_balance_of(self,
                       account_address,
                       formatted: bool = True,
                       block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_doc_token.balance_of(account_address,
                                                formatted=formatted,
                                                block_identifier=block_identifier)

    def bpro_balance_of(self,
                        account_address,
                        formatted: bool = True,
                        block_identifier: BlockIdentifier = 'latest'):

        return self.sc_moc_bpro_token.balance_of(account_address,
                                                 formatted=formatted,
                                                 block_identifier=block_identifier)

    def bprox_balance_of(self,
                         account_address,
                         formatted: bool = True,
                         block_identifier: BlockIdentifier = 'latest'):

        bucket = str.encode('X2')

        if self.mode == 'MoC':
            result = self.sc.functions.bproxBalanceOf(bucket, account_address).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.riskProxBalanceOf(bucket, account_address).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def doc_amount_to_redeem(self,
                             account_address,
                             formatted: bool = True,
                             block_identifier: BlockIdentifier = 'latest'):

        if self.mode == 'MoC':
            result = self.sc.functions.docAmountToRedeem(account_address).call(
                block_identifier=block_identifier)
        else:
            result = self.sc.functions.stableTokenAmountToRedeem(account_address).call(
                block_identifier=block_identifier)

        if formatted:
            result = Web3.fromWei(result, 'ether')

        return result

    def paused(self,
               block_identifier: BlockIdentifier = 'latest'):
        """is Paused"""

        result = self.sc.functions.paused().call(
            block_identifier=block_identifier)

        return result

    def amount_mint_bpro(self, amount: Decimal):
        """Final amount need it to mint bitpro in RBTC"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        total_amount = amount + commission_value

        return total_amount, commission_value

    def amount_mint_doc(self, amount: Decimal):
        """Final amount need it to mint doc"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        total_amount = amount + commission_value

        return total_amount, commission_value

    def amount_mint_btc2x(self, amount: Decimal):
        """Final amount need it to mint btc2x"""

        commission_value = self.sc_moc_inrate.calc_commission_value(amount)
        interest_value = self.sc_moc_inrate.calc_mint_interest_value(amount)
        total_amount = amount + commission_value + interest_value

        return total_amount, commission_value, interest_value

    def mint_bpro_gas_estimated(self, amount, precision=False):

        if precision:
            amount = amount * self.precision

        if self.mode == 'MoC':
            fxn_to_call = getattr(self.sc.functions, 'mintBPro')
        else:
            fxn_to_call = getattr(self.sc.functions, 'mintRiskPro')

        built_fxn = fxn_to_call(int(amount))
        gas_estimate = built_fxn.estimateGas()

        return gas_estimate

    def mint_doc_gas_estimated(self, amount, precision=False):

        if precision:
            amount = amount * self.precision

        if self.mode == 'MoC':
            fxn_to_call = getattr(self.sc.functions, 'mintDoc')
        else:
            fxn_to_call = getattr(self.sc.functions, 'mintStableToken')

        built_fxn = fxn_to_call(int(amount))
        gas_estimate = built_fxn.estimateGas()

        return gas_estimate

    def mint_bprox_gas_estimated(self, amount, precision=False):

        bucket = str.encode('X2')

        if precision:
            amount = amount * self.precision

        if self.mode == 'MoC':
            fxn_to_call = getattr(self.sc.functions, 'mintBProx')
        else:
            fxn_to_call = getattr(self.sc.functions, 'mintRiskProx')

        built_fxn = fxn_to_call(bucket, int(amount))
        gas_estimate = built_fxn.estimateGas()

        return gas_estimate

    def mint_bpro(self, amount: Decimal, default_account=None, wait_receipt=True):
        """ Mint amount bitpro
        NOTE: amount is in RBTC value
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        total_amount, commission_value = self.amount_mint_bpro(amount)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        max_mint_bpro_available = self.max_mint_bpro_available()
        if total_amount >= max_mint_bpro_available:
            raise Exception("You are trying to mint more than the limit. Mint BPro limit: {0}".format(
                max_mint_bpro_available))

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'mintBPro', int(amount * self.precision),
                                                          tx_params={'value': int(total_amount * self.precision)},
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"RiskProMint": self.sc_moc_exchange.events.RiskProMint().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RiskProMint": MoCExchangeRiskProMint(self.connection_manager,
                                                                       tx_logs["RiskProMint"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def mint_doc(self, amount: Decimal, default_account=None, wait_receipt=True):
        """ Mint amount DOC
        NOTE: amount is in RBTC value
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if self.state() < STATE_ABOVE_COBJ:
            raise Exception("Function cannot be called at this state.")

        absolute_max_doc = self.absolute_max_doc()
        btc_to_doc = amount * self.bitcoin_price()
        if btc_to_doc > absolute_max_doc:
            raise Exception("You are trying to mint more than availables. DOC Avalaible: {0}".format(
                absolute_max_doc))

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        total_amount, commission_value = self.amount_mint_doc(amount)

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'mintDoc', int(amount * self.precision),
                                                          tx_params={'value': int(total_amount * self.precision)},
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"StableTokenMint": self.sc_moc_exchange.events.StableTokenMint().processReceipt(tx_receipt)}
            tx_logs_formatted = {"StableTokenMint": MoCExchangeStableTokenMint(self.connection_manager,
                                                                               tx_logs["StableTokenMint"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def mint_btc2x(self, amount: Decimal, default_account=None, wait_receipt=True):
        """ Mint amount BTC2X
        NOTE: amount is in RBTC value
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        if amount <= self.minimum_amount:
            raise Exception("Amount value to mint too low")

        max_bprox_btc_value = self.max_bprox_btc_value()
        if amount > max_bprox_btc_value:
            raise Exception("You are trying to mint more than availables. BTC2x available: {0}".format(
                max_bprox_btc_value))

        total_amount, commission_value, interest_value = self.amount_mint_btc2x(amount)
        bucket = str.encode('X2')

        if total_amount > self.balance_of(default_account):
            raise Exception("You don't have suficient funds")

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'mintBProx', bucket, int(amount * self.precision),
                                                          tx_params={'value': int(total_amount * self.precision)},
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"RiskProxMint": self.sc_moc_exchange.events.RiskProxMint().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RiskProxMint": MoCExchangeRiskProxMint(self.connection_manager,
                                                                         tx_logs["RiskProxMint"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_bpro(self, amount_token: Decimal, default_account=None, wait_receipt=True):
        """ Reedem BitPro amount of token """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if self.state() < STATE_ABOVE_COBJ:
            raise Exception("Function cannot be called at this state.")

        # get bpro balance
        if not default_account:
            default_account = 0
        account_address = self.connection_manager.accounts[default_account].address
        if amount_token > self.bpro_balance_of(account_address):
            raise Exception("You are trying to redeem more than you have!")

        absolute_max_bpro = self.absolute_max_bpro()
        if amount_token >= absolute_max_bpro:
            raise Exception("You are trying to redeem more than availables. Available: {0}".format(
                absolute_max_bpro))

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'redeemBPro', int(amount_token * self.precision),
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"RiskProRedeem": self.sc_moc_exchange.events.RiskProRedeem().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RiskProRedeem": MoCExchangeRiskProRedeem(
                self.connection_manager,
                tx_logs["RiskProRedeem"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_free_doc(self, amount_token: Decimal, default_account=None, wait_receipt=True):
        """
        Reedem Free DOC amount of token
        Free Doc is Doc you can reedeem outside of settlement.
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.connection_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        free_doc = self.free_doc()
        if amount_token >= free_doc:
            raise Exception("You are trying to redeem more than availables. Available: {0}".format(
                free_doc))

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'redeemFreeDoc',
                                                          int(amount_token * self.precision),
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"FreeStableTokenRedeem": self.sc_moc_exchange.events.FreeStableTokenRedeem().processReceipt(tx_receipt)}
            tx_logs_formatted = {"FreeStableTokenRedeem": MoCExchangeFreeStableTokenRedeem(
                self.connection_manager,
                tx_logs["FreeStableTokenRedeem"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_doc_request(self, amount_token: Decimal, default_account=None, wait_receipt=True):
        """
        Reedem DOC request amount of token
        This is the amount of doc you want to reedem on settlement.
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.connection_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'redeemDocRequest',
                                                          int(amount_token * self.precision),
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"RedeemRequestAlter": self.sc_moc_settlement.events.RedeemRequestAlter().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RedeemRequestAlter": MoCSettlementRedeemRequestAlter(self.connection_manager,
                                                                                       tx_logs["RedeemRequestAlter"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_doc_request_alter(self, amount_token: Decimal, default_account=None, wait_receipt=True):
        """
        Redeeming DOCs on Settlement: alterRedeemRequestAmount

        There is only at most one redeem request per user during a settlement. A new redeem request is created
        if the user invokes it for the first time or updates its value if it already exists.
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot mint on settlement!")

        # get doc balance
        if not default_account:
            default_account = 0
        account_address = self.connection_manager.accounts[default_account].address
        account_balance = self.doc_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! Doc Balance: {0}".format(account_balance))

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'alterRedeemRequestAmount',
                                                          int(amount_token * self.precision),
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {"RedeemRequestAlter": self.sc_moc_settlement.events.RedeemRequestAlter().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RedeemRequestAlter": MoCSettlementRedeemRequestAlter(self.connection_manager,
                                                                                       tx_logs["RedeemRequestAlter"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_btc2x(self, amount_token: Decimal, default_account=None, wait_receipt=True):
        """ Reedem BTC2X amount of token """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        if not self.sc_moc_settlement.is_ready():
            raise Exception("You cannot reedem on settlement!")

        # get bprox balance of
        if not default_account:
            default_account = 0
        account_address = self.connection_manager.accounts[default_account].address
        account_balance = self.bprox_balance_of(account_address)
        if amount_token > account_balance:
            raise Exception("You are trying to redeem more than you have! BTC2X Balance: {0}".format(account_balance))

        bucket = str.encode('X2')

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'redeemBProx', bucket,
                                                          int(amount_token * self.precision),
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_for_transaction_receipt(
                tx_hash,
                timeout=self.receipt_timeout,
                poll_latency=self.poll_latency)
            tx_logs = {
                "RiskProxRedeem": self.sc_moc_exchange.events.RiskProxRedeem().processReceipt(tx_receipt)}
            tx_logs_formatted = {"RiskProxRedeem": MoCExchangeRiskProxRedeem(self.connection_manager,
                                                                             tx_logs["RiskProxRedeem"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def reedeem_all_doc(self, default_account=None, wait_receipt=True):
        """
        Reedem All doc only on liquidation
        """

        if self.paused():
            raise Exception("Contract is paused you cannot operate!")

        tx_hash = self.connection_manager.fnx_transaction(self.sc, 'redeemAllDoc',
                                                          default_account=default_account)

        tx_receipt = None
        tx_logs = None
        tx_logs_formatted = None
        if wait_receipt:
            # wait to transaction be mined
            tx_receipt = self.connection_manager.wait_transaction_receipt(tx_hash)
            #tx_logs = {"FreeStableTokenRedeem": self.sc_moc_exchange.events.FreeStableTokenRedeem().processReceipt(tx_receipt)}
            #tx_logs_formatted = {"FreeStableTokenRedeem": MoCExchangeFreeStableTokenRedeem(
            #    self.connection_manager,
            #    tx_logs["FreeStableTokenRedeem"][0])}

        return tx_hash, tx_receipt, tx_logs, tx_logs_formatted

    def search_block_transaction(self, block):

        network = self.connection_manager.network
        moc_addresses = list()
        moc_addresses.append(
            str.lower(self.connection_manager.options['networks'][network]['addresses']['MoC']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['MoCSettlement']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['MoCExchange']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['BProToken']))
        moc_addresses.append(str.lower(self.connection_manager.options['networks'][network]['addresses']['DoCToken']))

        print(moc_addresses)

        l_transactions = list()
        f_block = self.connection_manager.get_block(block, full_transactions=True)
        for transaction in f_block['transactions']:
            if str.lower(transaction['to']) in moc_addresses or \
                    str.lower(transaction['from']) in moc_addresses:
                l_transactions.append(transaction)

        #transaction_receipt = node_manager.web3.eth.getTransactionReceipt(transaction)

        return l_transactions

