from websocket import WebSocketApp, create_connection
from .support import LiveData

from threading import Thread

from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from colorama import Style, Fore

DEFAULT_HISTORIC_DATA_ID = 1000
DEFAULT_MARKET_DATA_ID = 2000


class TDHistoricDataError(LookupError):
    def __str__(self):
        return f"{Style.BRIGHT}{Fore.RED}Something's wrong with the historical data...{Style.RESET_ALL}"


class TDInvalidRequestError(LookupError):
    def __str__(self):
        return f"{Style.BRIGHT}{Fore.RED}Invalid request{Style.RESET_ALL}"


class LiveClient(WebSocketApp):

    def __init__(self, parent_app, url, on_open=None, *args):
        if on_open is None:
            on_open = self.on_open_func
        WebSocketApp.__init__(self, url, on_open=on_open, on_message=self.on_msg_func, *args)
        self.segments = []
        self.max_symbols = 0
        self.remaining_symbols = 0
        self.valid_until = ''
        self.contract_mapping = {}
        self.parent_app = parent_app

    def on_open_func(self):
        print(f"Opening WS...")

    def on_msg_func(self, message):
        msg = json.loads(message)
        if 'message' in msg.keys():
            self.handle_message_data(msg)
        if 'trade' in msg.keys():
            trade = msg['trade']
            self.handle_trade_data(trade)
        elif 'b' in msg.keys():
            pass

    def handle_message_data(self, msg):
        print(f"This ping contains a message = {msg['message']}")
        if msg['message'] == 'TrueData Real Time Data Service':  # Connection success message
            print(f"You can trade on {msg['segments']} | {type(msg['segments'])}")
        if msg['message'] == 'invalid request':
            print('raising request error')
            raise TDInvalidRequestError
        if msg['message'] == 'symbols added':
            self.add_contract_details(msg['symbollist'])
        if msg['message'] == 'symbols removed':
            pass

    def add_contract_details(self, contracts_list):
        for contract in contracts_list:
            contract_details = contract.split(':')
            self.contract_mapping[int(contract_details[1])] = contract_details[0]

    def handle_trade_data(self, trade_tick):
        try:
            symbol = self.contract_mapping[int(trade_tick[0])]
            # print(f'{Style.BRIGHT}{Fore.GREEN} This symbol({symbol}) is tied to req_ids of {self.parent_app.symbol_mkt_id_map[symbol]}...{Style.RESET_ALL}')
            # print(f"{trade_tick} || {type(trade_tick)}")
            for ticker_id in self.parent_app.symbol_mkt_id_map[symbol]:
                self.parent_app.live_data[ticker_id].timestamp = tick_timestamp = datetime.strptime(trade_tick[1], '%Y-%m-%dT%H:%M:%S')  # Old format = '%m/%d/%Y %I:%M:%S %p'
                self.parent_app.live_data[ticker_id].symbol = symbol
                self.parent_app.live_data[ticker_id].symbol_id = int(trade_tick[0])
                self.parent_app.live_data[ticker_id].ltp = float(trade_tick[2])
                self.parent_app.live_data[ticker_id].volume = float(trade_tick[3])
                self.parent_app.live_data[ticker_id].atp = float(trade_tick[4])
                self.parent_app.live_data[ticker_id].oi = float(trade_tick[5])
                self.parent_app.live_data[ticker_id].total_volume = float(trade_tick[6])
                try:
                    self.parent_app.live_data[ticker_id].best_bid_price = float(trade_tick[7])
                    self.parent_app.live_data[ticker_id].best_bid_qty = float(trade_tick[8])
                    self.parent_app.live_data[ticker_id].best_ask_price = float(trade_tick[9])
                    self.parent_app.live_data[ticker_id].best_ask_qty = float(trade_tick[10])
                except IndexError:
                    # Happens when not subscribed to bid-ask data in streaming data
                    pass
                # ltp = self.parent_app.live_data[ticker_id].ltp
        except KeyError:
            print(f'{Style.BRIGHT}{Fore.RED}This symbol is not tied to any req_id...{Style.RESET_ALL}')
        # print(f"{self.contract_mapping[int(trade_tick[0])]} --> {float(trade_tick[2])} @ {trade_tick[1]}")


class HistoricalWebsocket:
    def __init__(self, login_id, password, url, historical_port):
        self.login_id = login_id
        self.password = password
        self.url = url
        self.historical_port = historical_port
        self.hist_socket = create_connection(f"wss://{self.url}:{self.historical_port}?user={self.login_id}&password={self.password}")
        welcome_msg = self.hist_socket.recv()
        print(f"Welcomed with '{json.loads(welcome_msg)['message']}'")
        self.contract_mapping = {}

    def get_hist_bar_data(self, contract, query_time, start_time, bar_size):
        print(f'{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{query_time}"}}')
        self.hist_socket.send(f'{{"method": "gethistory", "interval": "{bar_size}", "symbol": "{contract}", "from": "{start_time}", "to": "{query_time}"}}')
        raw_hist_data = self.hist_socket.recv()
        hist_data = json.loads(raw_hist_data)['data']
        hist_data = self.hist_data_to_dict_list(hist_data, contract)
        return hist_data

    @staticmethod
    def hist_data_to_dict_list(hist_data, contract):  # No need for symbol other than printing
        data_list = []
        count = 0
        for j in hist_data:
            try:  # TODO: Remove HOTFIX because of this data point ['2020-02-13T09:15:00', 31565.05, 31565.05, 31565.05, 31565.05, 160, None]
                data_list.append({'time': datetime.strptime(j[0], '%Y-%m-%dT%H:%M:%S'),
                                  'o': float(j[1]),
                                  'h': float(j[2]),
                                  'l': float(j[3]),
                                  'c': float(j[4]),
                                  'v': int(j[5]),
                                  'oi': int(j[6])})
            except TypeError:
                print(f'{Style.BRIGHT}{Fore.RED} {contract} erred with {j}...{Style.RESET_ALL} \n\t {hist_data[count-2]} \n\t {hist_data[count-1]} \n\t {hist_data[count]} \n\t {hist_data[count+1]} \n\t {hist_data[count+2]}')
                continue
            count = count + 1
        return data_list

    def get_hist_tick_data(self):
        pass


class TD:
    def __init__(self, login_id, password, url='push.truedata_ws.in', live_port=8080, historical_port=8090, connect_historical=True, *args):
        self.live_websocket = None
        self.historical_websocket = None
        self.login_id = login_id
        self.password = password
        self.url = url
        self.live_port = live_port
        self.historical_port = historical_port
        self.connect_historical = connect_historical
        self.hist_data = {}
        self.live_data = {}
        self.symbol_mkt_id_map = {}
        self.streaming_symbols = {}
        self.connect()

    def connect(self):
        self.live_websocket = LiveClient(self, f"wss://{self.url}:{self.live_port}?user={self.login_id}&password={self.password}")
        t = Thread(target=self.connect_thread, args=())
        t.start()
        if self.connect_historical:
            self.historical_websocket = HistoricalWebsocket(self.login_id, self.password, self.url, self.historical_port)
        print(f'{Fore.GREEN}Connected...{Style.RESET_ALL}')

    def connect_thread(self):
        self.live_websocket.run_forever()

    def disconnect(self):
        self.live_websocket.close()
        print(f"{Fore.GREEN}Disconnected LIVE TrueData...{Style.RESET_ALL}")
        if self.connect_historical:
            self.historical_websocket.hist_socket.close()
            print(f"{Fore.GREEN}Disconnected HISTORICAL TrueData...{Style.RESET_ALL}")

    @staticmethod
    def resolve_contract(contract):
        contract_name = contract.symbol
        if contract.sec_type == 'FUT':
            contract_expiry = datetime.strptime(contract.expiry, '%Y%m%d')
            contract_name = f"{contract_name}{contract_expiry.strftime('%y%b')}FUT"
        elif contract.sec_type == 'OPT':
            contract_expiry = datetime.strptime(contract.expiry, '%Y%m%d')
            expiry_date_str = f"{contract_expiry.strftime('%y%m%d')}"
            contract_name = f"{contract_name}{expiry_date_str}{contract.strike}{contract.right}E"
        # elif contract.sec_type == 'IND':
        #     contract_name = contract.symbol + '-I'
        elif contract.sec_type == 'STK' or contract.sec_type == 'IND':
            pass
        return contract_name.upper()

    @staticmethod
    def truedata_duration_map(regular_format, end_date):
        duration_units = regular_format.split()[1].upper()
        if len(duration_units) > 1:
            raise TDHistoricDataError
        duration_size = int(regular_format.split()[0])
        if duration_units == 'D':
            return (end_date - relativedelta(days=duration_size - 1)).date()
        elif duration_units == 'W':
            return (end_date - relativedelta(weeks=duration_size)).date()
        elif duration_units == 'M':
            return (end_date - relativedelta(months=duration_size)).date()
        elif duration_units == 'Y':
            return (end_date - relativedelta(years=duration_size)).date()

    def get_historic_data(self, contract,
                          ticker_id=DEFAULT_HISTORIC_DATA_ID,
                          query_time=None,
                          duration="1 D",
                          bar_size="1 min"):
        global DEFAULT_HISTORIC_DATA_ID
        if query_time is None:
            query_time = datetime.today()
        start_time = self.truedata_duration_map(duration, query_time)

        if bar_size == 'tick':
            hist_data = self.historical_websocket.get_hist_tick_data(contract, )
        else:
            bar_size = bar_size.replace(' ', '')
            query_time = query_time.strftime('%Y-%m-%d') + 'T23:59:59'
            start_time = start_time.strftime('%Y-%m-%d') + 'T00:00:00'
            print(contract)
            print(query_time)
            print(start_time)
            print(bar_size)
            hist_data = self.historical_websocket.get_hist_bar_data(contract, query_time, start_time, bar_size)
        DEFAULT_HISTORIC_DATA_ID = DEFAULT_HISTORIC_DATA_ID + 1
        self.hist_data[ticker_id] = hist_data
        return hist_data

    def start_live_data(self, resolved_contract, req_id=DEFAULT_MARKET_DATA_ID):
        global DEFAULT_MARKET_DATA_ID
        # self.live_data_contracts[req_id] = resolved_contract
        self.live_data[req_id] = LiveData(resolved_contract)
        try:
            print('Adding to existing')
            self.symbol_mkt_id_map[resolved_contract.upper()].append(req_id)
            print('Adding to existing... SUCCESS')
        except KeyError:
            self.symbol_mkt_id_map[resolved_contract.upper()] = [req_id]
            print('Creating new... SUCCESS')
        self.live_websocket.send(f'{{"method": "addsymbol", "symbols": ["{resolved_contract}"]}}')
        DEFAULT_MARKET_DATA_ID = DEFAULT_MARKET_DATA_ID + 1
        return req_id

    def stop_live_data(self, contract):
        self.live_websocket.send(f'{{"method": "removesymbol", "symbols": ["{contract}"]}}')
