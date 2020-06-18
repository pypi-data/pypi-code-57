"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

from web3 import Web3, Account
from web3._utils.transactions import wait_for_transaction_receipt
from web3._utils.threads import Timeout
from web3.exceptions import TimeExhausted
import json
import os
import datetime
import logging


class BaseConnectionManager(object):

    log = logging.getLogger()

    @staticmethod
    def options_from_config(filename=None):
        """ Options from file config.json """

        if not filename:
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

        with open(filename) as f:
            options = json.load(f)

        return options


class ConnectionManager(BaseConnectionManager):

    log = logging.getLogger()

    network = 'mocTestnet'
    default_account = 0  # index of the account
    index_uri = 0
    accounts = None

    options = BaseConnectionManager.options_from_config()

    def __init__(self,
                 options=None,
                 network='mocTestnet'):

        # options values
        if options:
            if isinstance(options, dict):
                self.options = options
            elif isinstance(options, str):
                self.options = self.options_from_config(filename=options)
            else:
                raise Exception("Not valid option value")

        # network selection
        self.network = network

        # connect to node
        self.web3 = self.connect_node()

        # scan accounts
        self.scan_accounts()

    def connect_node(self, index_uri=0):
        """Connect to the node"""

        network = self.network
        uri = self.options['networks'][network]['uri']
        if isinstance(uri, list):
            current_uri = uri[index_uri]
        elif isinstance(uri, str):
            current_uri = uri
        else:
            raise Exception("Not valid uri")

        self.index_uri = index_uri
        return Web3(Web3.HTTPProvider(current_uri,
                                      request_kwargs={'timeout': self.options['timeout']}))

    def scan_accounts(self):
        """ Accounts from config or enviroment"""

        accounts = list()

        if 'ACCOUNT_PK_SECRET' in os.environ:
            # obtain from enviroment if exist instead
            private_key = os.environ['ACCOUNT_PK_SECRET']

            l_priv = private_key.split(',')
            if len(l_priv) > 1:
                # this is a method:
                # ACCOUNT_PK_SECRET=PK1,PK2,PK3
                for a_priv in l_priv:
                    account = Account().from_key(a_priv)
                    accounts.append(account)
            else:
                # Simple PK: ACCOUNT_PK_SECRET=PK
                account = Account().from_key(private_key)
                accounts.append(account)

            # scan 10 accounts like this:
            # ACCOUNT_PK_SECRET_1, ACCOUNT_PK_SECRET_2 .. ACCOUNT_PK_SECRET_9
            for numb in range(1, 10):
                env_pk = 'ACCOUNT_PK_SECRET_{}'.format(numb)
                if env_pk in os.environ:
                    private_key = os.environ[env_pk]
                    account = Account().from_key(private_key)
                    accounts.append(account)

        else:
            # obtain from config file
            if self.options['networks'][self.network]['accounts']:
                for acc in self.options['networks'][self.network]['accounts']:
                    if acc['private_key']:
                        account = Account().from_key(acc['private_key'])
                        accounts.append(account)

        self.accounts = accounts

    def set_default_account(self, index):
        """ Default index account from config.json accounts """

        self.default_account = index

    def block_timestamp(self, block):
        """ Block timestamp """
        block_timestamp = self.web3.eth.getBlock(block).timestamp
        dt_object = datetime.datetime.fromtimestamp(block_timestamp)
        return dt_object

    @property
    def is_connected(self):
        """ Is connected to the node """
        if not self.web3:
            return False

        return self.web3.isConnected()

    @property
    def gas_price(self):
        """ Gas Price """
        return self.web3.eth.gasPrice

    @property
    def minimum_gas_price(self):
        """ Gas Price """
        return Web3.toInt(hexstr=self.web3.eth.getBlock('latest').minimumGasPrice)

    @property
    def minimum_gas_price_fixed(self):
        """ Gas Price """
        return self.options['gas_price']

    @property
    def block_number(self):
        """ Las block number """
        return self.web3.eth.blockNumber

    def balance(self, address):
        """ Balance of the address """
        return self.web3.eth.getBalance(Web3.toChecksumAddress(address))

    def balance_block_number(self, address, block_number=0):
        """ Balance of the address """
        return self.web3.eth.getBalance(Web3.toChecksumAddress(address), block_number)

    def get_block(self, *args, **kargs):
        """ Get the block"""
        return self.web3.eth.getBlock(*args, **kargs)

    def get_transaction_receipt(self, transaction_hash):
        """ Transaction receipt """
        return self.web3.eth.getTransactionReceipt(transaction_hash)

    def get_transaction_by_hash(self, transaction_hash):
        """ Transaction by hash """
        return self.web3.eth.getTransaction(transaction_hash)

    def fnx_transaction(self, sc, function_, *tx_args,
                        tx_params=None,
                        gas_limit=3500000,
                        default_account=None,
                        nonce_method="pending"):
        """Contract agnostic transaction function with extras"""

        network = self.network
        if not default_account:
            default_account = self.default_account

        fxn_to_call = getattr(sc.functions, function_)
        built_fxn = fxn_to_call(*tx_args)

        gas_estimate = built_fxn.estimateGas()
        self.log.debug("Gas estimate to transact with {}: {}\n".format(function_, gas_estimate))

        if gas_estimate > gas_limit:
            raise Exception("Gas estimated is bigger than gas limit")

        if tx_params:
            if not isinstance(tx_params, dict):
                raise Exception("Tx params need to be dict type")

        self.log.debug("Sending transaction to {} with {} as arguments.\n".format(function_, tx_args))

        from_address = self.accounts[default_account].address
        nonce = self.web3.eth.getTransactionCount(from_address, nonce_method)

        tx_value = 0
        if tx_params:
            if 'value' in tx_params:
                tx_value = tx_params['value']

        gas_price = self.options['gas_price']
        if gas_price <= 0:
            gas_price = self.minimum_gas_price

        transaction_dict = {'chainId': self.options['networks'][network]['chain_id'],
                            'nonce': nonce,
                            'gasPrice': gas_price,
                            'gas': gas_limit,
                            'value': tx_value}

        transaction = built_fxn.buildTransaction(transaction_dict)

        pk = self.accounts[default_account].key
        signed = self.web3.eth.account.signTransaction(transaction,
                                                       private_key=pk)

        transaction_hash = self.web3.eth.sendRawTransaction(
            signed.rawTransaction)

        return transaction_hash

    def fnx_constructor(self, sc, *tx_args,
                        tx_params=None,
                        gas_limit=3500000,
                        default_account=None,
                        nonce_method="pending"):
        """Contract agnostic transaction function with extras"""

        network = self.network
        if not default_account:
            default_account = self.default_account

        built_fxn = sc.constructor(*tx_args)

        gas_estimate = built_fxn.estimateGas()
        self.log.debug("Gas estimate to transact with {}: {}\n".format('Constructor', gas_estimate))

        if gas_estimate > gas_limit:
            raise Exception("Gas estimated is bigger than gas limit")

        if tx_params:
            if not isinstance(tx_params, dict):
                raise Exception("Tx params need to be dict type")

        self.log.debug("Sending transaction to {} with {} as arguments.\n".format('Constructor', tx_args))

        from_address = self.accounts[default_account].address
        pk = self.accounts[default_account].key
        nonce = self.web3.eth.getTransactionCount(from_address, nonce_method)

        tx_value = 0
        if tx_params:
            if 'value' in tx_params:
                tx_value = tx_params['value']

        gas_price = self.options['gas_price']
        if gas_price <= 0:
            gas_price = self.minimum_gas_price

        transaction_dict = {'chainId': self.options['networks'][network]['chain_id'],
                            'nonce': nonce,
                            'gasPrice': gas_price,
                            'gas': gas_limit,
                            'value': tx_value}

        transaction = built_fxn.buildTransaction(transaction_dict)

        signed = self.web3.eth.account.signTransaction(transaction,
                                                       private_key=pk)

        transaction_hash = self.web3.eth.sendRawTransaction(
            signed.rawTransaction)

        return transaction_hash

    def wait_transaction_receipt(self, tx_hash, timeout=180):

        # Wait for the transaction to be mined, and get the transaction receipt
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)

        self.log.debug(
            ("Transaction receipt mined with hash: {hash}\n"
             "on block number {blockNum} "
             "with a total gas usage of {totalGas}").format(
                hash=tx_receipt['transactionHash'].hex(),
                blockNum=tx_receipt['blockNumber'],
                totalGas=tx_receipt['cumulativeGasUsed']
            )
        )

        return tx_receipt

    def wait_for_transaction_receipt(self, tx_hash, timeout=180, poll_latency=0.1):

        try:
            return wait_for_transaction_receipt(self.web3,
                                                tx_hash,
                                                timeout=timeout,
                                                poll_latency=poll_latency)
        except Timeout:
            raise TimeExhausted(
                "Transaction {} is not in the chain, after {} seconds".format(
                    tx_hash,
                    timeout,
                )
            )

    def load_json_contract(self, json_filename, deploy_address=None):
        """ Load the abi from json file """

        network = self.network

        with open(json_filename) as f:
            info_json = json.load(f)
        abi = info_json["abi"]

        # Get from json if we dont know the address
        if not deploy_address:
            deploy_address = info_json["networks"][str(self.options['networks'][network]['chain_id'])]['address']

        sc = self.web3.eth.contract(address=self.web3.toChecksumAddress(deploy_address), abi=abi)

        return sc

    def load_abi_contract_file(self, abi_filename, contract_address):
        """ Load the abi """

        with open(abi_filename) as f:
            abi = json.load(f)

        sc = self.web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)

        return sc

    def load_contract(self, abi, contract_address):
        """ Load contract """

        sc = self.web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)

        return sc

    def load_bytecode_contract_file(self, abi_filename, bin_filename):
        """ Load abi and bin content from files """

        with open(abi_filename) as f:
            content_abi = json.load(f)

        with open(bin_filename) as f:
            content_bin = f.read()

        return self.load_bytecode_contract( content_abi, content_bin)

    def load_bytecode_contract(self, content_abi, content_bin):
        """ Load abi and bin content """

        sc = self.web3.eth.contract(abi=content_abi, bytecode=content_bin)

        return sc, content_abi, content_bin

    def load_bytecode_contract_file_json(self, json_filename, link_library=None):
        """ Get the json content from json compiled """

        with open(json_filename) as f:
            json_content = json.load(f)

        bytecode = json_content["bytecode"]
        if link_library:
            for lib_name, lib_address in link_library:
                bytecode = bytecode.replace(lib_name, lib_address)

        sc = self.web3.eth.contract(abi=json_content["abi"], bytecode=bytecode)

        return sc

    @staticmethod
    def all_events_from(sc, events_functions=None, from_block=0, to_block='latest'):

        if events_functions:
            if not isinstance(events_functions, list):
                raise Exception(
                    'events_functions must be a list of event functions like ["Event Name 1", "Event Name 2"]'
                )
        else:
            events_functions = list()
            for fn_events in sc.events:
                events_functions.append(fn_events.__name__)

        r_events = dict()
        for fn_events in sc.events:

            if fn_events.__name__ in events_functions:
                l_event = list()
                event_filter = fn_events.createFilter(fromBlock=from_block, toBlock=to_block)
                event_entries = event_filter.get_all_entries()
                for event_entry in event_entries:
                    if event_entry['event'] == fn_events.__name__:
                        l_event.append(event_entry)
                r_events[fn_events.__name__] = l_event
        return r_events

    def logs_from(self, sc, events_functions, from_block, to_block, block_steps=2880):

        last_block_number = int(self.block_number)

        if to_block <= 0:
            to_block = last_block_number  # last block number in the node

        current_block = from_block

        l_events = dict()
        while current_block <= to_block:

            step_end = current_block + block_steps
            if step_end > to_block:
                step_end = to_block

            self.log.info("Scanning blocks steps from {0} to {1}".format(current_block, step_end))

            events = self.all_events_from(sc,
                                          events_functions=events_functions,
                                          from_block=current_block,
                                          to_block=step_end)

            # Adjust current blocks to the next step
            current_block = current_block + block_steps

            # add to the list
            for fnx_name in events_functions:
                if fnx_name in events:
                    if events[fnx_name]:
                        if fnx_name not in l_events:
                            l_events[fnx_name] = list()
                        l_events[fnx_name].append(events[fnx_name])

        return l_events


if __name__ == '__main__':
    print("init")
