from datetime import date, datetime, timedelta
import time

import ccxt
import pandas as pd
from stockstats import StockDataFrame


class CryptoMomentumTradingClient:
    def __init__(self, config: dict) -> None:
        # Authenticate user
        if 'auth' not in config or config['auth'] != 'tKcrPehIdAx4m3Svsan2teiU68CEvnWE':
            raise Exception('Permission denied (auth token invalid or missing)')
        # Access FTX cryptocurrency exchange
        self.exchange = ccxt.ftx({
            'apiKey': config['apiKey'],
            'secret': config['apiSecret'],
            'headers': {
                'FTX-SUBACCOUNT': config['subAccountName'],
            },
        })
        # Verify login was successful
        self.exchange.check_required_credentials()
        self.config = config
        self.crypto_symbol = config['cryptoSymbol']
        self.ma_lookback = config['maLookBack']
        self.ema_lookback = config['emaLookBack']
        self.atr_lookback = config['atrLookBack']
        self.equity_currency = config['equityCurrency']

    def retrieve_trading_data(self) -> pd.DataFrame:
        longest_lookback = 4 * max([self.ma_lookback, self.ema_lookback, self.atr_lookback + 1])
        # First day of lookback
        start_point = int(time.time() - longest_lookback * 86400) * 1000
        trading_data = self.exchange.fetch_ohlcv(symbol=self.crypto_symbol, timeframe=self.config['dataTimeFrame'], since=start_point)
        df = pd.DataFrame(trading_data)
        df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
        return df

    @staticmethod
    def get_indicator(trading_sdf: StockDataFrame, key: str) -> float:
        # Compute most recent indicator through stock data frame
        return trading_sdf[key].loc[len(trading_sdf) - 1]

    def stop_was_triggered(self) -> bool:
        # Method for fetching recent stop orders, unique to FTX
        order_info = self.exchange.private_get_conditional_orders_history({'market': self.crypto_symbol, 'limit': 1})
        if order_info['success']:
            if len(order_info['result']) > 0:
                last_stop_order = order_info['result'][0]
                if last_stop_order['triggeredAt']:
                    # Determine if stop was triggered in last trading day
                    formatted_time_string = ''.join(last_stop_order['triggeredAt'].rsplit(':', 1))
                    stop_date = datetime.strptime(formatted_time_string, '%Y-%m-%dT%H:%M:%S.%f%z')
                    return stop_date.date() in [date.today(), date.today() - timedelta(days=1)]
            return False
        raise Exception('request failed to retrieve stop order history')

    def search_current_position(self) -> dict:
        # Method for fetching current positions, unique to FTX
        current_positions = self.exchange.private_get_positions()
        if current_positions['success']:
            for position in current_positions['result']:
                if position['size'] > 0:
                    return position
            return {}
        raise Exception('request failed to retrieve account positions')

    def fetch_account_balance(self) -> float:
        balance_info = self.exchange.fetch_balance()
        if balance_info['info']['success']:
            if self.equity_currency in balance_info['total']:
                return balance_info['total'][self.equity_currency]
            raise Exception('account balance does not have a total in {}'.format(self.equity_currency))
        raise Exception('request failed to retrieve account balance')

    def recalibrate_position(self, ma: float, ema: float, atr: float, price: float):
        # Terminate positioning if stop was triggered in last trading day
        if self.config['waitIfStopLoss'] and self.stop_was_triggered():
            return
        # Flag to signal when repositioning should occur
        should_reposition = False
        # Determine if position needs to be reversed
        current = self.search_current_position()
        if current:
            # Reverse entire position amount
            order_amount = current['size']
            # Current position is long and MA > EMA
            if current['side'] == 'buy' and ma > ema:
                self.exchange.create_order(self.crypto_symbol, 'market', 'sell', order_amount)
                should_reposition = True
            # Current position is short and EMA > MA
            elif current['side'] == 'sell' and ema > ma:
                self.exchange.create_order(self.crypto_symbol, 'market', 'buy', order_amount)
                should_reposition = True
        # Position is being reversed or no position exists
        if not current or should_reposition:
            # Cancel pending stop orders
            cancel_params = {
                'conditionalOrdersOnly': True,
            }
            self.exchange.cancel_all_orders(self.crypto_symbol, params=cancel_params)
            # Size new position
            account_balance = self.fetch_account_balance()
            max_amount = (self.config['equityAmount'] * self.config['accountLeverage'] * account_balance) / price
            risk_adjusted_amount = (account_balance * self.config['riskMultiplier']) / (atr * 2)
            new_amount = risk_adjusted_amount if risk_adjusted_amount <= max_amount else max_amount
            # Trigger price and reduce-only options for FTX stop order
            stop_params = {
                'reduceOnly': True,
            }
            # Short position when MA > EMA
            if ma > ema:
                stop_params['triggerPrice'] = price + atr * 2
                self.exchange.create_order(self.crypto_symbol, 'market', 'sell', new_amount)
                self.exchange.create_order(self.crypto_symbol, 'stop', 'buy', new_amount, params=stop_params)
            # Long position when EMA > MA
            elif ema > ma:
                stop_params['triggerPrice'] = price - atr * 2
                self.exchange.create_order(self.crypto_symbol, 'market', 'buy', new_amount)
                self.exchange.create_order(self.crypto_symbol, 'stop', 'sell', new_amount, params=stop_params)

    def execute(self):
        trading_df = self.retrieve_trading_data()
        trading_sdf = StockDataFrame.retype(trading_df)
        ma_key = 'close_' + str(self.ma_lookback) + '_sma'
        ma = self.get_indicator(trading_sdf, ma_key)
        ema_key = 'close_' + str(self.ema_lookback) + '_ema'
        ema = self.get_indicator(trading_sdf, ema_key)
        atr_key = 'atr_' + str(self.atr_lookback)
        atr = self.get_indicator(trading_sdf, atr_key)
        price = trading_df['close'].loc[len(trading_df) - 1]
        self.recalibrate_position(ma, ema, atr, price)
