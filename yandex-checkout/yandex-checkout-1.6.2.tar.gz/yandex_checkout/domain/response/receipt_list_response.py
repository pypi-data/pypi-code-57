# -*- coding: utf-8 -*-
from yandex_checkout.domain.common.response_object import ResponseObject
from yandex_checkout.domain.response.receipt_response import ReceiptResponse


class ReceiptListResponse(ResponseObject):
    __type = None

    __items = None

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        if isinstance(value, list):
            self.__items = [ReceiptResponse(receipt) for receipt in value]
        else:
            self.__items = value
