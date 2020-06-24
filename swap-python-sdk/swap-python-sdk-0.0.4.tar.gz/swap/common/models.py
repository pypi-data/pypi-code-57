class ServiceDiscoveryVendor:
    def __init__(self, service_provider_name, service_provider_uuid, service_provider_signature):
        self.service_provider_name = service_provider_name
        self.service_provider_uuid = service_provider_uuid
        self.service_provider_signature = service_provider_signature


class ServiceDiscoveryProperty:
    def __init__(self, title, type, options=[]):
        self.title = title
        self.type = type
        self.options = options


class ServiceDiscoveryParameters:
    def __init__(self, properties):
        self.properties = properties


class ServiceDiscoveryService:
    def __init__(self, name, catalogue_uuid, service_description, parameters):
        self.name = name
        self.catalogue_uuid = catalogue_uuid
        self.service_description = service_description
        self.parameters = parameters


class ServiceDiscoveryDataset:
    def __init__(self, input, output):
        self.input = input
        self.output = output


class ServiceDiscoveryIcon:
    def __init__(self, base64, url):
        self.base64 = base64
        self.url = url


class ServiceDiscoveryData:
    def __init__(self, vendor, service, dataset, icon):
        self.vendor = vendor
        self.service = service
        self.dataset = dataset
        self.icon = icon


class ServiceDiscoveryResponse:
    def __init__(self, data):
        self.data = data
