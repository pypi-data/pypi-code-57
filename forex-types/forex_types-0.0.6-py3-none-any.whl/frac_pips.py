from decimal import Decimal


from forex_types.pair import Pair
from forex_types.currency import Currency
from forex_types.price import Price


class FracPips(int):
    """Integer subclass for fractional pips."""

    def to_ratio_price(self, ratio: Decimal) -> Price:
        """Get Price per ratio of frac pips to quote currency unit.

        Args:
            ratio: fractional pip / currency quote unit.
        Returns:
            Price in currency units that have ratio
        """
        return Price(self * ratio)

    def to_quote_price(self, quote: Currency):
        """Get Price object with respect to quote currency.

        Args:
            quote: quote currency fractional pips represent
        Returns:
            Price of self with respect to quote currency.
        """
        return Price(self * quote.rounder)

    def to_pair_price(self, pair: Pair):
        """Get Price object with respect to forex pair.

        Args:
            pair: pair that fractional pips represent.
        Returns:
            Price of self with respect to pair.
        """
        return Price(self * pair.quote.rounder)

    @classmethod
    def from_price(cls, price: Price) -> "FracPips":
        """Get fractional pips from Price object.

        Args:
            price: Price object to find frac pips for.
        """
        return cls(round(price.pips * 10))
