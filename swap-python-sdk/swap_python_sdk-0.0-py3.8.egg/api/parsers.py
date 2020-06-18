from swap.api.filters import (
    InputDatasetsResponseFilter, ServiceOffersResponseFilter, ProgressResponseFilter
)
from swap.api.schemas import (
    InputDatasetsResponseSchema, ServiceOffersResponseSchema, ProgressResponseSchema
)
from swap.common.parsers import Parser


class InputDatasetsResponseParser(Parser):
    def __init__(self):
        self.filter = InputDatasetsResponseFilter()
        self.schema = InputDatasetsResponseSchema()


class ServiceOffersResponseParser(Parser):
    def __init__(self):
        self.filter = ServiceOffersResponseFilter()
        self.schema = ServiceOffersResponseSchema()


class ProgressResponseParser(Parser):
    def __init__(self):
        self.filter = ProgressResponseFilter()
        self.schema = ProgressResponseSchema()
