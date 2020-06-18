import base64
import requests
from typing import Any, Dict

from ..grpc import markets, vega


def errStr(r: requests.Response) -> str:
    return "request failed: HTTP {} {}".format(r.status_code, r.text)


_mappings = {
    "api.MarketByIDResponse.market": markets.Market,
    "api.MarketsDataResponse.marketsData": vega.MarketData,
    "api.MarketsResponse.markets": markets.Market,
    "vega.Future.ethereumEvent": markets.EthereumEvent,
    "vega.Instrument.future": markets.Future,
    "vega.Instrument.metadata": markets.InstrumentMetadata,
    "vega.LogNormalRiskModel.params": markets.LogNormalModelParams,
    "vega.MarginCalculator.scalingFactors": markets.ScalingFactors,
    "vega.Market.continuous": markets.ContinuousTrading,
    "vega.Market.tradableInstrument": markets.TradableInstrument,
    "vega.TradableInstrument.instrument": markets.Instrument,
    "vega.TradableInstrument.logNormalRiskModel": markets.LogNormalRiskModel,
    "vega.TradableInstrument.marginCalculator": markets.MarginCalculator,
}


def convert_complextype(j, r, f):

    if f.full_name in _mappings:
        # print("Setting obj {} ({})".format(f.json_name, f.full_name))
        innerType = _mappings[f.full_name]
        if isinstance(j[f.json_name], list):
            getattr(r, f.json_name).MergeFrom(
                [convert_obj(item, innerType()) for item in j[f.json_name]]
            )
        else:
            inner = innerType()
            convert_obj(j[f.json_name], inner)
            getattr(r, f.json_name).CopyFrom(inner)
        return

    raise Exception("not implemented: {}".format(f.full_name))


def convert_field(j, r, f):
    if f.json_name not in j:
        return

    if f.type == 14:  # enum
        values = [v for v in f.enum_type.values if v.name == j[f.json_name]]
        if len(values) != 1:
            raise Exception(
                "Found not 1 matching enum value, but {}".format(len(values))
            )
        setattr(r, f.json_name, values[0].number)
    elif f.type == 12:  # bytes
        # print("bytes {}: {}".format(f.json_name, j[f.json_name]))
        setattr(r, f.json_name, base64.b64decode(j[f.json_name]))
    elif f.type == 11:  # object
        convert_complextype(j, r, f)
    elif f.type == 9:  # string
        if isinstance(j[f.json_name], list):
            # print("list {}: {}".format(f.json_name, j[f.json_name]))
            getattr(r, f.json_name).MergeFrom(j[f.json_name])
        elif isinstance(j[f.json_name], str):
            # print("str {}: {}".format(f.json_name, j[f.json_name]))
            setattr(r, f.json_name, j[f.json_name])
        else:
            raise Exception("not implemented: type 9, but not string or list")
    elif f.type == 8:  # bool
        # print("bool {}: {}".format(f.json_name, j[f.json_name]))
        setattr(r, f.json_name, bool(j[f.json_name]))
    elif f.type == 4:  # int
        # print("int {}: {}".format(f.json_name, j[f.json_name]))
        setattr(r, f.json_name, int(j[f.json_name]))
    elif f.type == 3:  # timestamp
        # print("timestamp {}: {}".format(f.json_name, j[f.json_name]))
        setattr(r, f.json_name, int(j[f.json_name]))
    elif f.type == 1:  # float
        # print("float {}: {}".format(f.json_name, j[f.json_name]))
        setattr(r, f.json_name, float(j[f.json_name]))
    else:
        raise Exception(
            "type {} not implemented for {}".format(f.type, f.full_name)
        )


def convert_obj(j: Dict[str, Any], r):  # empty response object
    """
    Convert a dict (from requests.Response.json()) into a gRPC object.
    """
    for f in r.DESCRIPTOR.fields:
        convert_field(j, r, f)

    return r
