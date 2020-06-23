from swap.common.logging import logger
from swap.api.sequences.step_codes import StepCode

class ServiceRequestPreHook:
    def call(self, input):
        return input


class ServiceRequestPostHook:
    def call(self, input):
        return input


class ServiceOffersRequestPreHook:
    def call(self, input):
        return input


class ServiceOffersRequestPostHook:
    def select_first_service_offers(self, input):
        chain_links = input.response.chain_links

        response = {}

        for chain_link_key, chain_link in chain_links.items():
            if not chain_link.service_offers.items():
                logger.info(f'No service offers received yet for service: {chain_link.service_catalogue_uuid}')
                return StepCode.NoServiceOffersReceived
            service_offers = list(chain_link.service_offers.values())
            response[chain_link_key] = service_offers[0]

        output = input
        output.response = response

        return output

    def call(self, input):
        return self.select_first_service_offers(input)


class ServiceExecutionRequestPreHook:
    def call(self, input):
        return input


class ServiceExecutionRequestPostHook:
    def call(self, input):
        return input


class ProgressRequestPreHook:
    def call(self, input):
        return input


class ProgressRequestPostHook:
    def call(self, input):
        return input
