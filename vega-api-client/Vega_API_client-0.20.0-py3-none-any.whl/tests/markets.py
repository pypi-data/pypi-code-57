import os

import vegaapiclient as vac


def main():
    grpc_node = os.getenv("GRPC_NODE")
    assert grpc_node is not None and grpc_node != ""
    vcGRPC = vac.VegaTradingDataClient(vac.API.GRPC, grpc_node)

    rest_node = os.getenv("REST_NODE")
    assert rest_node is not None and rest_node != ""
    vcREST = vac.VegaTradingDataClient(vac.API.REST, rest_node)

    # marketID = "VHSRA2G5MDFKREFJ5TOAGHZBBDGCYS67"

    # marketGRPC = vcGRPC.MarketByID(
    #     vac.grpc.api.trading.MarketByIDRequest(marketID=marketID))
    # print("marketGRPC={}".format(marketGRPC))

    # marketREST = vcREST.MarketByID(marketID)
    # print("marketREST={}".format(marketREST))

    # assert marketGRPC.SerializeToString() == marketREST.SerializeToString()

    marketsGRPC = vcGRPC.Markets(vac.grpc.api.trading.MarketsResponse())
    print("marketsGRPC={}".format(marketsGRPC))

    marketsREST = vcREST.Markets()
    print("marketsREST={}".format(marketsREST))

    assert marketsGRPC.SerializeToString() == marketsREST.SerializeToString()


if __name__ == "__main__":
    main()
