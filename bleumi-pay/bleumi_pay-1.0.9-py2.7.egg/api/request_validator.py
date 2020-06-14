# coding: utf-8

"""
    Bleumi Pay REST API

    A simple and powerful REST API to integrate ERC-20, Ethereum, xDai, Algorand payments and/or payouts into your business or application  # noqa: E501

    Contact: info@bleumi.com
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

class RequestValidator(object):

    def is_eth_addr(self, addr):
        match = re.match('^0x[a-fA-F0-9]{40}$', addr)
        return ((match != None)) or (addr == 'ETH') or (addr == 'XDAI') or (addr == 'XDAIT')

    def is_rsk_addr(self, addr):
        match = re.match('^0x[a-fA-F0-9]{40}$', addr)
        return ((match != None)) or (addr == 'RBTC')

    def is_algo_addr(self, addr):
        match = re.match('^[A-Z2-7+=*]{58}$', addr)
        return match

    def is_algo_token(self, addr):
        match = re.match('^[0-9]*$', addr)
        return ((match != None)) or (addr == 'ALGO')        

    def is_algo_network(self, chain):
        return ((chain == "alg_mainnet") or (chain == "alg_testnet"))

    def is_rsk_network(self, chain):
        return ((chain == "rsk") or (chain == "rsk_testnet"))

    def check_eth_addr(self, name, input):
        if (self.is_eth_addr(input)):
            return None
        else: 
            return "%s is not a valid Ethereum address" % (name)

    def check_rsk_addr(self, name, input):
        if (self.is_rsk_addr(input)):
            return None
        else: 
            return "%s is not a valid RSK address" % (name)

    def check_algo_addr(self, name, input, is_token=False):
        if is_token:
            if not(self.is_algo_token(input)):
                return "%s is not a valid Algorand token " % (name)
        else:
            if not(self.is_algo_addr(input)):
                return "%s is not a valid Algorand address " % (name)        
        return None

    def check_req_param(self, name, input):
        if input is None:
            return "Missing required parameter '%s'" % (name)
    
    def check_network_addr(self, name, input, chain=None, mandatory=False, is_token=False):
        msg = None
        if mandatory:
            msg = self.check_req_param(name, input)
            if msg is not None:
                return msg
        if input is not None:
            if self.is_algo_network(chain):
                msg = self.check_algo_addr(name, input, is_token)
            if self.is_rsk_network(chain):
                msg = self.check_rsk_addr(name, input)
            else: 
                msg = self.check_eth_addr(name, input)
            if msg is not None:
                return msg
        return msg   

    def validate_refund_payment_request(self, params, chain=None):
        # check if chain is provided 
        msg = self.check_req_param('Chain', chain)   
        if msg is not None:
            return msg
        
        # check if token is valid address in the network    
        msg = self.check_network_addr('Token', params.token, chain, True, True)   
        if msg is not None:
            return msg

    def validate_settle_payment_request(self, params, chain=None):
        # check if chain is provided   
        msg = self.check_req_param('Chain', chain)   
        if msg is not None:
            return msg  

        # check if token is valid address in the network    
        msg = self.check_network_addr('Token', params.token, chain, True, True)   
        if msg is not None:
            return msg

        # check if amount is provided    
        msg = self.check_req_param('Amount', params.amount)   
        if msg is not None:
            return msg    


    def validate_create_checkout_url_request(self, params):
        # check if 'id' is provided
        msg = self.check_req_param('Id', params.id)   
        if msg is not None:
            return msg

        # check if currency is provided 
        msg = self.check_req_param('Currency', params.currency)   
        if msg is not None:
            return msg
        
        # check if amount is provided
        msg = self.check_req_param('Amount', params.amount)   
        if msg is not None:
            return msg

        # check if cancel_url is provided    
        msg = self.check_req_param('CancelUrl', params.cancel_url)   
        if msg is not None:
            return msg

        # check if success_url is provided    
        msg = self.check_req_param('SuccessUrl', params.success_url)   
        if msg is not None:
            return msg

        if params.token is not None:  
            # check if chain is provided    
            msg = self.check_req_param('Chain', params.chain)   
            if msg is not None:
                return msg  

            # check if token is valid address in the network       
            msg = self.check_network_addr('Token', params.token, params.chain, False, True)   
            if msg is not None:
                return msg
            
            # check if transfer_address is valid address in the network    
            if params.transfer_address is not None:  
                msg = self.check_network_addr('TransferAddress', params.transfer_address, params.chain, False, False)   
                if msg is not None:
                    return msg

    def validate_checkout_payment_params(self, params):
        # check if hmac_alg is supplied
        msg = self.check_req_param('HmacAlg', params.hmac_alg)   
        if msg is not None:
            return msg
        
        # check if hmac_input is supplied
        msg = self.check_req_param('HmacInput', params.hmac_input)   
        if msg is not None:
            return msg
        
        # check if hmac_key_id is supplied
        msg = self.check_req_param('HmacKeyId', params.hmac_key_id)   
        if msg is not None:
            return msg
        
        # check if hmac_value is supplied
        msg = self.check_req_param('HmacValue', params.hmac_value)   
        if msg is not None:
            return msg

    def validate_create_payout_request(self, params, chain=None):
        # check if chain is supplied
        msg = self.check_req_param('Chain', chain)   
        if msg is not None:
            return msg  
        
        # check if token is supplied & is valid address for the network
        msg = self.check_network_addr('Token', params.token, chain, True, True)   
        if msg is not None:
            return msg
        
        payouts = params.payouts

        # check if payouts are supplied
        if len(payouts) == 0: 
            return "Payouts not defined."  

        for payout in payouts: 
            msg = self.check_network_addr('TransferAddress', payout.transfer_address, chain, True, False)   
            if msg is not None:
                return msg
            msg = self.check_req_param('Amount', payout.amount)   
            if msg is not None:
                return msg
            if self.is_algo_network(chain):
                msg = self.check_req_param('Authorization', payout.authorization)   
                if msg is not None:
                    return msg