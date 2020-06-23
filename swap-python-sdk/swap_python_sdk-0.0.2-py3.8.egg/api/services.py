from swap.api.clients import ServiceDiscoveryClient
from swap.api.models import Service
from swap.common.parsers import ServiceDiscoveryResponseParser


client = ServiceDiscoveryClient()


def list_all():
    raw_result = client.get_services()
    parser = ServiceDiscoveryResponseParser()
    service_discovery_response = parser.parse(raw_result).data
    output = []

    for service_discovery_data in service_discovery_response:
        service = Service(service_discovery_data)
        output.append(service)

    return output


def select(name):
    services = list_all()

    for service in services:
        if service.name == name:
            return service

    return None
