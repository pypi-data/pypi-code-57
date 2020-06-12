from see137.parameters import Parameter
from see137.parameters.fields import CurrencyFields, ExchangeFields
from jamboree.utils.core import consistent_hash

class PortfolioParameter(Parameter):
    def __init__(self, currency:CurrencyFields, exchange:ExchangeFields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency_fields = currency
        self.exchange_fields = exchange
        # We'd split this between currency, exchange details, and risk details
    
    @property
    def initial(self):
        return self.currency_fields.initial
    
    @property
    def base(self):
        return self.currency_fields.base
    
    @property
    def exchange(self):
        return self.exchange_fields.name
    
    @property
    def slippage(self):
        return self.exchange_fields.slippage
