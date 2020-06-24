class Filter:
    def __init__(self):
        self.response = {}


class ServiceDiscoveryDataFilter(Filter):
    def apply(self, response):
        self.response = response

        self.remove_extra_name_field()
        self.correct_dataset_types()
        self.set_empty_parameters_string_to_dict()
        self.wrap_parameters()

        return self.response

    def remove_extra_name_field(self):
        if 'service' not in self.response:
            return

        if 'parameters' not in self.response['service']:
            return

        if 'name' in self.response['service']['parameters']:
            del self.response['service']['parameters']['name']

    def correct_dataset_types(self):
        if 'dataset' not in self.response:
            return

        if 'input' in self.response['dataset']:
            if type(self.response['dataset']['input']) == list:
                value = self.response['dataset']['input'][0]

                self.response['dataset']['input'] = value

        if 'output' in self.response['dataset']:
            if type(self.response['dataset']['output']) == list:
                value = self.response['dataset']['output'][0]

                self.response['dataset']['output'] = value

    def wrap_parameters(self):
        if 'service' not in self.response:
            return

        if 'parameters' not in self.response['service']:
            return

        if 'properties' not in self.response['service']['parameters']:
            value = self.response['service'].pop('parameters')
            self.response['service']['parameters'] = {'properties': value}

    def set_empty_parameters_string_to_dict(self):
        if 'service' not in self.response:
            return

        if 'parameters' not in self.response['service']:
            return

        if self.response['service']['parameters'] == '':
            self.response['service']['parameters'] = {'properties': {}}


class ServiceDiscoveryResponseFilter:
    def apply(self, response):
        service_discovery_data_filter = ServiceDiscoveryDataFilter()

        output = []

        for service_response in response['data']:
            result = service_discovery_data_filter.apply(service_response)
            output.append(result)

        return {'data': output}
