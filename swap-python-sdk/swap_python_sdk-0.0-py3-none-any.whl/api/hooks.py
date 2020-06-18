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
