import json
from swap.common.schemas import ServiceDiscoveryResponseSchema
from swap.common.filters import ServiceDiscoveryResponseFilter


class Parser:
    def apply_pre_processing(self, response):
        return json.loads(response)

    def apply_filters(self, response):
        return self.filter.apply(response)

    def parse(self, response):
        preprocessed_response = self.apply_pre_processing(response)
        filtered_response = self.apply_filters(preprocessed_response)

        return self.schema.load(filtered_response)


class ServiceDiscoveryResponseParser(Parser):
    def __init__(self):
        self.filter = ServiceDiscoveryResponseFilter()
        self.schema = ServiceDiscoveryResponseSchema()
