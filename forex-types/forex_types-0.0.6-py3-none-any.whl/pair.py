"""Currency pair class. Initialized by string.

Synopsis:
    pair = Pair("eurusd")  # Case insensitive, non letters ignored.
    base = pair.base
    quote = pair.quote
"""

import string

from forex_types.currency import Currency


class Pair:
    EUR_GBP = None
    EUR_AUD = None
    GBP_AUD = None
    EUR_NZD = None
    GBP_NZD = None
    AUD_NZD = None
    EUR_USD = None
    GBP_USD = None
    AUD_USD = None
    NZD_USD = None
    EUR_CAD = None
    GBP_CAD = None
    AUD_CAD = None
    NZD_CAD = None
    USD_CAD = None
    EUR_CHF = None
    GBP_CHF = None
    AUD_CHF = None
    NZD_CHF = None
    USD_CHF = None
    CAD_CHF = None
    EUR_JPY = None
    GBP_JPY = None
    AUD_JPY = None
    NZD_JPY = None
    USD_JPY = None
    CAD_JPY = None
    CHF_JPY = None

    CURRENCIES = {
        "aud": Currency.AUD,
        "cad": Currency.CAD,
        "chf": Currency.CHF,
        "eur": Currency.EUR,
        "gbp": Currency.GBP,
        "jpy": Currency.JPY,
        "nzd": Currency.NZD,
        "usd": Currency.USD,
    }
    LETTERS = {_ for _ in string.ascii_lowercase}

    def __init__(self, name: str):
        letters = [_ for _ in name.lower() if _ in self.LETTERS]
        self.name = "".join(letters)
        if len(self.name) != 6:
            raise ValueError(f"Unknown pair: {self.name}")
        base_name = "".join(letters[:3])
        quote_name = "".join(letters[3:])
        if base_name not in self.CURRENCIES:
            raise ValueError(f"Unknown base in pair: {self.name}")
        if quote_name not in self.CURRENCIES:
            raise ValueError(f"Unknown quote in pair: {self.name}")
        self.base = self.CURRENCIES[base_name]
        self.quote = self.CURRENCIES[quote_name]
        if self.base.precedence >= self.quote.precedence:
            raise ValueError(f"Bad permutation of base and quote in pair: {self.name}")

    @staticmethod
    def from_currency(base: Currency, quote: Currency):
        """Make pair object from two currency objects or strings."""
        return Pair(str(base) + str(quote))

    def __hash__(self):
        return hash((self.base, self.quote))

    def __str__(self):
        """String representation intentionally matches Oanda v20"""
        return f"{self.base}_{self.quote}"

    def __eq__(self, other):
        if not isinstance(other, Pair):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, Pair):
            return NotImplemented
        if self.base < other.base:
            return True
        return self.quote < other.quote

    def camel(self):
        """Return pair name in camel case like: AudUsd"""
        return f"{self.base.name.title()}{self.quote.name.title()}"

    @classmethod
    def iter_pairs(cls):
        base_list = Currency.get_list()  # sorted by precedence.
        quote_list = Currency.get_list()  # e.g. EUR -> JPY
        base_list.pop()  # Last currency will not be a base.
        quote_list.pop(0)  # First currency will not be a quote.
        while base_list:
            base = base_list.pop(0)
            for quote in quote_list:
                yield cls(f"{base}{quote}")
            quote_list.pop(0)


Pair.EUR_GBP = Pair("EUR_GBP")
Pair.EUR_AUD = Pair("EUR_AUD")
Pair.GBP_AUD = Pair("GBP_AUD")
Pair.EUR_NZD = Pair("EUR_NZD")
Pair.GBP_NZD = Pair("GBP_NZD")
Pair.AUD_NZD = Pair("AUD_NZD")
Pair.EUR_USD = Pair("EUR_USD")
Pair.GBP_USD = Pair("GBP_USD")
Pair.AUD_USD = Pair("AUD_USD")
Pair.NZD_USD = Pair("NZD_USD")
Pair.EUR_CAD = Pair("EUR_CAD")
Pair.GBP_CAD = Pair("GBP_CAD")
Pair.AUD_CAD = Pair("AUD_CAD")
Pair.NZD_CAD = Pair("NZD_CAD")
Pair.USD_CAD = Pair("USD_CAD")
Pair.EUR_CHF = Pair("EUR_CHF")
Pair.GBP_CHF = Pair("GBP_CHF")
Pair.AUD_CHF = Pair("AUD_CHF")
Pair.NZD_CHF = Pair("NZD_CHF")
Pair.USD_CHF = Pair("USD_CHF")
Pair.CAD_CHF = Pair("CAD_CHF")
Pair.EUR_JPY = Pair("EUR_JPY")
Pair.GBP_JPY = Pair("GBP_JPY")
Pair.AUD_JPY = Pair("AUD_JPY")
Pair.NZD_JPY = Pair("NZD_JPY")
Pair.USD_JPY = Pair("USD_JPY")
Pair.CAD_JPY = Pair("CAD_JPY")
Pair.CHF_JPY = Pair("CHF_JPY")
