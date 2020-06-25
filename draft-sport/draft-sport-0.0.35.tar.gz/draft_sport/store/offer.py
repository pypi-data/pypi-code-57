"""
Draft Sport Python Library
Offer Module
author: hugh@blinkybeach.com
"""
from typing import TypeVar, Type, Any, List, Optional, Dict
from decimal import Decimal
from nozomi import Decodable
from draft_sport.store.price import Price
from draft_sport.store.product import Product
from nozomi import Immutable, Configuration, RequestCredentials
from nozomi import URLParameter, URLParameters, HTTPMethod, ApiRequest
from draft_sport.store.frequency import Frequency

T = TypeVar('T', bound='Offer')


class Offer(Decodable):

    _PATH = '/offer'

    def __init__(
        self,
        public_id: str,
        name: str,
        prices: List[Price],
        products: List[Product],
        frequency: Frequency
    ) -> None:

        self._public_id = public_id
        self._name = name
        self._prices = prices
        self._products = products
        self._frequency = frequency

        return

    public_id: str = Immutable(lambda s: s._public_id)
    name: str = Immutable(lambda s: s._name)
    prices: List[Price] = Immutable(lambda s: s._prices)
    products: List[Product] = Immutable(lambda s: s._products)
    features: List[str] = Immutable(lambda s: s._flatten_features())
    frequency: Frequency = Immutable(lambda s: s._frequency)
    price_map: Dict[str, Decimal] = Immutable(
        lambda s: {p.denomination.iso_4217: str(p.magnitude) for p in s._prices}
    )

    def _flatten_features(self) -> List[str]:
        flat_features: List[str] = list()
        for product in self._products:
            for feature in product.features:
                flat_features.append(feature)
        return flat_features

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            name=data['name'],
            prices=Price.decode_many(data['prices']),
            products=Product.decode_many(data['products']),
            frequency=Frequency(data['frequency'])
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        public_id: str,
        credentials: RequestCredentials,
        configuration: Configuration
    ) -> Optional[T]:

        parameters = URLParameters([URLParameter('offer', public_id)])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            configuration=configuration,
            data=None,
            url_parameters=parameters,
            credentials=credentials
        )

        return cls.optionally_decode(request.response_data)
