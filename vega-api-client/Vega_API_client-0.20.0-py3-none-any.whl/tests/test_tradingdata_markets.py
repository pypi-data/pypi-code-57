from google.protobuf.empty_pb2 import Empty

import vegaapiclient as vac

from .fixtures import tradingdataGRPC, tradingdataREST  # noqa: F401


def test_MarketByID(tradingdataGRPC, tradingdataREST):  # noqa: F811
    markets = tradingdataGRPC.Markets(Empty()).markets
    assert len(markets) > 0
    marketID = markets[0].id

    req = vac.api.trading.MarketByIDRequest(marketID=marketID)
    marketGRPC = tradingdataGRPC.MarketByID(req)
    marketREST = tradingdataREST.MarketByID(req)

    assert marketGRPC.SerializeToString() == marketREST.SerializeToString()


def test_Markets(tradingdataGRPC, tradingdataREST):  # noqa: F811
    marketsGRPC = tradingdataGRPC.Markets(Empty())
    marketsREST = tradingdataREST.Markets(Empty())
    assert marketsGRPC.SerializeToString() == marketsREST.SerializeToString()
