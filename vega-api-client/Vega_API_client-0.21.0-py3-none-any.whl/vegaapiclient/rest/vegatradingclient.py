import requests
from google.protobuf.reflection import GeneratedProtocolMessageType

from ..grpc import api

from .convert import convert_obj, errStr
from .unconvert import unconvert_obj


class VegaTradingClient(object):
    """
    The Vega Trading Client talks to a back-end node.
    """

    def __init__(self, url: str) -> None:
        if url is None:
            raise Exception("Missing node URL")
        self.url = url

        self._httpsession = requests.Session()

    def NotifyTraderAccount(
        self, req: GeneratedProtocolMessageType
    ) -> GeneratedProtocolMessageType:
        url = "{}/fountain".format(self.url)
        restreq = unconvert_obj(req)
        r = self._httpsession.post(url, json=restreq)
        if r.status_code != 200:
            raise Exception(errStr(r))
        return convert_obj(r.json(), api.trading.NotifyTraderAccountResponse())

    def PrepareSubmitOrder(
        self, req: GeneratedProtocolMessageType
    ) -> GeneratedProtocolMessageType:
        url = "{}/orders/prepare".format(self.url)
        restreq = unconvert_obj(req)
        r = self._httpsession.post(url, json=restreq)
        if r.status_code != 200:
            raise Exception(errStr(r))
        return convert_obj(r.json(), api.trading.PrepareSubmitOrderResponse())

    # PrepareCancelOrder,CancelOrderRequest,PrepareCancelOrderResponse

    # PrepareAmendOrder,AmendOrderRequest,PrepareAmendOrderResponse

    # Withdraw,WithdrawRequest,WithdrawResponse

    def SubmitTransaction(
        self, req: GeneratedProtocolMessageType
    ) -> GeneratedProtocolMessageType:
        url = "{}/transaction".format(self.url)
        restreq = unconvert_obj(req)
        r = self._httpsession.post(url, json=restreq)
        if r.status_code != 200:
            raise Exception(errStr(r))
        return convert_obj(r.json(), api.trading.SubmitTransactionResponse())
