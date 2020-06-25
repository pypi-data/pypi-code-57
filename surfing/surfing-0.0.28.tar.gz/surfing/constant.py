import inspect

class ReadableEnum(object):
    _code_name_cache = None

    @classmethod
    def init_cache(cls):
        cls._code_name_cache = ({}, {})
        for name in dir(cls):
            attr = getattr(cls, name)
            if name.startswith('_') or inspect.ismethod(attr):
                continue
            # assert attr not in cls._code_name_cache[0], f'failed to register {name}, {attr} is a registed value'
            # assert name not in cls._code_name_cache[1], f'failed to register {attr}, {name} is a registed enum'
            cls._code_name_cache[0][attr] = name
            cls._code_name_cache[1][name] = attr

    @classmethod
    def read(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[0].get(code, code)

    @classmethod
    def parse(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[1].get(code, code)



class ExchangeID(ReadableEnum):
    NOT_AVAILABLE = 0
    SSE = 1
    SZE = 2
    HK = 3
    CFFEX = 4
    DCE = 5
    SHFE = 6
    CZCE = 7

    CRYPTO = 100
    HUOBI = 101
    OKEX = 102
    BINANCE = 103
    BITMEX = 104


class Direction(ReadableEnum):
    NOT_AVAILABLE = 0
    BUY = 1
    SELL = 2


class PosiDirection(ReadableEnum):
    NOT_AVAILABLE = 0
    NET = 1
    LONG = 2
    SHORT = 3


class OrderType(ReadableEnum):
    NOT_AVAILABLE = 0
    PLAIN_ORDER_PREFIX = 1
    BASKET_ORDER_PREFIX = 2
    ALGO_ORDER_PREFIX = 3
    # PLAIN
    PLAIN_ORDER = 10
    LIMIT = 11
    MARKET = 12
    FAK = 13
    FOK = 14
    # BASKET
    BASKET_ORDER = 20
    # ALGO
    ALGO_ORDER = 30
    TWAP = 31


class OffsetFlag(ReadableEnum):
    NOT_AVAILABLE = 0
    OPEN = 1
    CLOSE = 2
    FORCE_CLOSE = 3
    CLOSE_TODAY = 4
    CLOSE_YESTERDAY = 5


class OrderStatus(ReadableEnum):
    NOT_AVAILABLE = 0
    UNKNOWN = 1
    PROPOSED = 10
    RESPONDED = 20
    QUEUEING = 30
    NO_TRADE_QUEUEING = 31
    PART_TRADE_QUEUEING = 32
    PENDING_MAX = 39
    # // if status >= 40, it is not pending
    REJECTED = 40  # // router / gateway / exchange reject
    REJECT_BY_ROUTER = 41
    REJECT_BY_GATEWAY = 42
    REJECT_BY_EXCHANGE = 43
    CANCELLED = 50  # // cancelled, no mater all traded or partly traded
    NO_TRADE_CANCELED = 51
    PART_TRADE_CANCELED = 52
    ALL_TRADED = 60
    # // some other middle status...
    TO_CANCEL = 70


class TradingStyle(ReadableEnum):
    NOT_AVAILABLE = 0
    AGGRESSIVE = 1
    NEUTRAL = 2
    CONSERVATIVE = 3


class BarType(ReadableEnum):
    NOT_AVAILABLE = 0
    MIN_1 = 1
    MIN_3 = 2
    MIN_5 = 3
    MIN_15 = 4
    MIN_30 = 5
    HOUR_1 = 10
    HOUR_2 = 11
    HOUR_4 = 12
    HOUR_6 = 13
    HOUR_12 = 14
    DAY_1 = 20
    WEEK_1 = 30
    MONTH_1 = 40
    YEAR_1 = 50

    _type_secs_cache = None

    @classmethod
    def get_seconds(cls, bar_type):
        if cls._type_secs_cache is None:
            cls._type_secs_cache = {
                cls.MIN_1: 1 * 60,
                cls.MIN_3: 3 * 60,
                cls.MIN_5: 5 * 60,
                cls.MIN_15: 15 * 60,
                cls.MIN_30: 30 * 60,
                cls.HOUR_1: 1 * 60 * 60,
                cls.HOUR_2: 2 * 60 * 60,
                cls.HOUR_4: 4 * 60 * 60,
                cls.HOUR_6: 6 * 60 * 60,
                cls.HOUR_12: 12 * 60 * 60,
                cls.DAY_1: 1 * 24 * 60 * 60,
                cls.WEEK_1: 1 * 7 * 24 * 60 * 60,
                cls.MONTH_1: 1 * 30 * 24 * 60 * 60,  # not accurate
                cls.YEAR_1: 1 * 365 * 24 * 60 * 60,  # not accurate
            }
        return cls._type_secs_cache.get(bar_type, -1)


class AssetType(ReadableEnum):
    NOT_AVAILABLE = 0
    #
    TRADITIONAL_ASSET = 10
    STOCK = 11
    FUTURES = 12
    OPTION = 13
    FUND = 14
    #
    CRYPTO_ASSET = 20
    CRYPTO_SPOT = 21
    CRYPTO_CONTRACT = 22
    CRYPTO_MARGIN = 23
    CRYPTO_PERPETUAL = 24
    CRYPTO_CONTRACT_MARGIN = 25  # 为CRYPTO_COIN_MARGIN_CONTRACT对应的margin
    CRYPTO_COIN_MARGIN_CONTRACT = 26  # 这里特指以币计价的合约,确定了为这类asset需再额外确定对应的margin(体现在posItem里)


class ExecRole(ReadableEnum):
    NOT_AVAILABLE = 0
    MAKER = 1
    TAKER = 2


class MarginMode(ReadableEnum):
    NOT_AVAILABLE = 0
    CROSSED = 1
    FIXED = 2

class LongShort():
    # [long, short] +1 top, -1 bottom, 0 None
    Lt      = [1,   0,  'Longtop']
    Lb      = [-1,  0,  'Longbottom']
    St      = [0,   1,  'Shorttop']
    Sb      = [0,   -1, 'Shortbottom']
    Long    = [1,   0,  'Long']
    Short   = [0,   1,  'Short']
    LtSb    = [1,   -1, 'LongtopShortbottom']
    LbSt    = [-1,  1,  'LongbottomShorttop']

    def find_strategy(self, code):
        self._code_name_cache = ({}, {})
        for name in dir(self):
            attr = getattr(self, name)
            if name.startswith('_') or inspect.ismethod(attr):
                continue
            self._code_name_cache[0][attr[2]] = name
            self._code_name_cache[1][name] = attr
        
        return self._code_name_cache[1][self._code_name_cache[0].get(code, code)]

class ExchangeStatus(ReadableEnum):
    """交易状态指标"""
    OPEN = 0
    SUSPENDED = 1
    LIMITED = 2
    CLOSE = 3