import uuid
from typing import Optional
# from see137.exchange import price_gen_func
from see137.utils.trades import TradeType
from see137.utils.ordering import buy_total_cash, get_sale_pct

import crayons as cy

class Trade(object):
    """A trade object for use within trading environments."""

    def __init__(self, symbol: str, trade_type: 'TradeType', amount: float, price: float):
        """
        Arguments:
            symbol: The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc).
            trade_type: The type of trade executed (0 = HOLD, 1=LIMIT_BUY, 2=MARKET_BUY, 3=LIMIT_SELL, 4=MARKET_SELL).
            amount: The amount of the instrument in the trade (shares, satoshis, contracts, etc).
            price: The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD").
            exchange: The exchange we're adding the trade into.
            commission: 
        """
        self._symbol = symbol
        self._trade_type = trade_type
        self._amount = amount
        self._price = price


        # Use these variables to
        self._exchange: Optional[str] = None
        self._episode: Optional[str] = None
        self._commission: Optional[str] = None
        self._userid: Optional[str] = None
        self._islive:bool = False

    def copy(self) -> 'Trade':
        """Return a copy of the current trade object."""
        return Trade(symbol=self._symbol, trade_type=self._trade_type, amount=self._amount, price=self._price)

    
    @property
    def symbol(self) -> str:
        """The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc)."""
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self._symbol = symbol

    @property
    def trade_type(self) -> 'TradeType':
        """The type of trade ("buy", "sell", "hold", etc)."""
        return self._trade_type

    @trade_type.setter
    def trade_type(self, trade_type: 'TradeType'):
        self._trade_type = trade_type

    @property
    def amount(self) -> float:
        """The amount of the instrument in the trade (shares, satoshis, contracts, etc)."""
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        self._amount = amount

    @property
    def price(self) -> float:
        """The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD")."""
        return float(self._price)

    @price.setter
    def price(self, price: float):
        self._price = price

    @property
    def is_hold(self) -> bool:
        """
        Returns:
            Whether the trade type is non-existent (i.e. hold).
        """
        return self._trade_type.is_hold

    @property
    def is_buy(self) -> bool:
        """
        Returns:
            Whether the trade type is a buy offer.
        """
        return self._trade_type.is_buy

    @property
    def is_sell(self) -> bool:
        """
        Returns:
            Whether the trade type is a sell offer.
        """
        return self._trade_type.is_sell
    
    @property
    def exchange(self):
        if self._exchange is None:
            raise AttributeError("Exchange hasn't been set")
        return self._exchange
    
    @exchange.setter
    def exchange(self, _exchange:str):
        self._exchange = _exchange

    @property
    def episode(self):
        if self._episode is None:
            raise AttributeError("Episode hasn't been set")
        return self._episode
    
    @episode.setter
    def episode(self, _episode:str):
        self._episode = _episode
    
    @property
    def userid(self):
        if self._userid is None:
            raise AttributeError("User id not set")
        return self._userid
    
    @userid.setter
    def userid(self, user_id):
        self._userid = user_id

    @property    
    def live(self) -> bool:
        return self._islive

    @live.setter
    def live(self, _live:bool):
        self._live = _live

    def __str__(self) -> str:
        action_name = "BUY"
        if self.is_sell:
            action_name = "SELL"
        elif self.is_hold:
            action_name = "HOLD"
        
        return_string = f"<Trade: {action_name}, symbol:{self.symbol}, amount:{self.amount}, price: {self.price}>"
        return return_string

class DynamicTrade(object):
    """A trade object for use within trading environments."""

    def __init__(self, symbol: str, trade_type: 'TradeType', percentage=0.4, cap=0.5, pct_net_worth=0.3, net_worth=10000):
        """
        Arguments:
            symbol: The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc).
            trade_type: The type of trade executed (0 = HOLD, 1=LIMIT_BUY, 2=MARKET_BUY, 3=LIMIT_SELL, 4=MARKET_SELL).
            amount: The amount of the instrument in the trade (shares, satoshis, contracts, etc).
            price: The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD").
        """
        self._symbol = symbol
        self._trade_type = trade_type
        self._percentage = percentage
        self._net_worth = net_worth
        self._cap_pct = cap
        self._current_pct_net_worth = pct_net_worth
        self._amount = 0.0
        self._price = 0.0000001

    def copy(self) -> 'Trade':
        """Return a copy of the current trade object."""
        return Trade(symbol=self._symbol, trade_type=self._trade_type, price=self._price, amount=self._amount)
    
    def calculate_trade(self) -> 'Trade':
        """Return a copy of the current trade object."""

        self.current_pct = self.amount * self.price
        if self.is_buy:
            total_cash = buy_total_cash(
                percentage=self.percentage, 
                cap_allocation=self.cap_pct, 
                pct_of_networth=(self.current_pct/self.net_worth), 
                net_worth=self.net_worth
            )
            self.amount = ((total_cash/self.price) * 0.9999998)
            
        elif self.is_sell:
            percentage_to_sell = get_sale_pct(
                decision_percentage=self.percentage,
                cap_percentage=self.cap_pct,
                current_percentage=(self.current_pct / self.net_worth)
            )
            # Amount should already be set by now to the number of items
            trade_amount = ((self.amount * percentage_to_sell) * 0.9999998)
            self.amount = trade_amount

        return Trade(symbol=self.symbol, trade_type=self.trade_type, price=self.price, amount=self.amount)

    
    @property
    def symbol(self) -> str:
        """The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc)."""
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self._symbol = symbol

    @property
    def trade_type(self) -> 'TradeType':
        """The type of trade ("buy", "sell", "hold", etc)."""
        return self._trade_type

    @trade_type.setter
    def trade_type(self, trade_type: 'TradeType'):
        self._trade_type = trade_type

    @property
    def amount(self) -> float:
        """The amount of the instrument in the trade (shares, satoshis, contracts, etc)."""
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        self._amount = amount

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, _price:float):
        self._price = _price

    @property
    def is_hold(self) -> bool:
        """
        Returns:
            Whether the trade type is non-existent (i.e. hold).
        """
        return self._trade_type.is_hold

    @property
    def is_buy(self) -> bool:
        """
        Returns:
            Whether the trade type is a buy offer.
        """
        return self._trade_type.is_buy

    @property
    def is_sell(self) -> bool:
        """
        Returns:
            Whether the trade type is a sell offer.
        """
        return self._trade_type.is_sell


    """ Buy and sell properties """

    @property
    def percentage(self):
        return self._percentage
    

    @percentage.setter
    def percentage(self, _pct):
        self._percentage = _pct

    @property
    def cap_pct(self):
        return self._cap_pct


    @cap_pct.setter
    def cap_pct(self, _cap_pct):
        self._cap_pct = _cap_pct
    
    @property
    def current_pct(self):
        """ The currently held percentage of the total value """
        return self._current_pct_net_worth
    

    @current_pct.setter
    def current_pct(self, _pct):
        """ The currently held percentage of the total value """
        self._current_pct_net_worth = _pct
        
    
    @property
    def net_worth(self):
        return self._net_worth
    
    @net_worth.setter
    def net_worth(self, _worth):
        self._net_worth = _worth


    def __str__(self) -> str:
        current_trade = self.calculate_trade()
        return str(current_trade)


if __name__ == "__main__":
    dynamic_trade = DynamicTrade("BTC", TradeType.LIMIT_BUY)
    dynamic_trade.price = 200
    dynamic_trade.cap_pct = 0.35
    dynamic_trade.percentage = 1.0
    trade = dynamic_trade.calculate_trade()
    print(trade)

