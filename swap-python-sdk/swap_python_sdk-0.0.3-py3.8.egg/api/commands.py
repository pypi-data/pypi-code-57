import json
from swap.api.clients import UBLClient, IngestionClient
from swap.api.models import ServiceRequest, ServiceRequestChainLink
from swap.api.parsers import ServiceOffersResponseParser, ProgressResponseParser
from swap.api.requests.builders import ServiceExecutionRequestBuilder
from swap.api.schemas import (
    ServiceRequestSchema, ServiceExecutionRequestSchema, IngestionProgressResponseSchema
)
from swap.api.state import ProgressStateMachine
from swap.common.logging import logger
from time import sleep
from swap.api.sequences.step_codes import StepCode


class Command:
    def __init__(self):
        self.ubl_client = UBLClient()


class ServiceRequestCommand(Command):
    def build_service_request(self, input):
        service_request = ServiceRequest(service_chain={})

        for service in input.service_chain.services:
            dataset_identifiers = []
            
            for dataset in input.service_chain.datasets:
                dataset_identifier = dataset.name

                if hasattr(dataset, 'url'):
                    dataset_identifier = dataset.url
            
                dataset_identifiers.append(dataset_identifier)

            service_request.add_chain_link(
                ServiceRequestChainLink(
                    datasets=dataset_identifiers,
                    service=service.name
                )
            )

        return service_request

    def request_body(self, input):
        service_request = self.build_service_request(input)
        schema = ServiceRequestSchema()
        request = schema.dump(service_request)

        logger.debug(f'Built ServiceRequest body: {request}')

        return request

    def submit(self, input):
        request_body = self.request_body(input)
        raw_result = self.ubl_client.post('requests', data=request_body)        

        try:
            result_as_json = json.loads(raw_result)
        except:
            raise Exception(f'Failed to load result as json {raw_result}. request_body: {request_body}')

        return result_as_json

    def call(self, input):
        logger.debug('Calling ServiceRequestCommand')
        response = self.submit(input)
        output = input
        output.response = response

        return output


class ServiceOffersRequestCommand(Command):
    def __init__(self):
        self.current_retries = 0
        self.max_retries = 5
        self.sleep_time = 2

        super().__init__()

    def deserialise_response(self, response):
        parser = ServiceOffersResponseParser()
        return parser.parse(response)

    def submit(self, service_chain_uuid):
        if self.current_retries <= self.max_retries:
            url = f'serviceoffers?service_chain_uuid={service_chain_uuid}'
            response = self.ubl_client.get(url)

            logger.debug(f'Raw ServiceOffersResponse: {response}')

            if 'No ServiceRequests received yet' in response:
                logger.debug('Retrying')
                self.current_retries += 1
                sleep(self.sleep_time)

                return self.submit(service_chain_uuid)

            return self.deserialise_response(response)
        else:
            raise Exception(f'Max retries of {self.max_retries} exceeded')

    def call(self, input):
        logger.debug('Calling ServiceOffersRequestCommand')

        service_chain_uuid = input.response['service_chain_uuid']

        logger.info(f'Service chain UUID: {service_chain_uuid}')

        response = self.submit(service_chain_uuid)

        if response == StepCode.NoServiceOffersReceived:
            return StepCode.NoServiceOffersReceived

        output = input
        output.response = response
        return output


class ServiceExecutionRequestCommand(Command):
    def add_parameters(self, request_body_dict, input):
        for chain_link_key, chain_link in request_body_dict['service_chain'].items():
            srvc = next(x for x in input.service_chain.services if x.chain_link == chain_link_key)

            for key, value in srvc.params.configuration.items():
                request_body_dict['service_chain'][chain_link_key]['parameters'][key] = value

        return request_body_dict

    def build_request_body(self, input):
        service_execution_request_builder = ServiceExecutionRequestBuilder()
        service_execution_request = service_execution_request_builder.build(input)

        schema = ServiceExecutionRequestSchema()
        request_body_dict = schema.dump(service_execution_request)

        request_body_dict_with_parameters = self.add_parameters(request_body_dict, input)

        return request_body_dict_with_parameters['service_chain']

    def submit(self, input):
        url = '/serviceexecutions'
        request_body = self.build_request_body(input)
        logger.debug(f'ServiceExecutionRequest body: {request_body}')
        raw_response = self.ubl_client.post(url, data=request_body)

        return json.loads(raw_response)

    def call(self, input):
        logger.debug('Calling ServiceExecutionRequestCommand')
        response = self.submit(input)

        logger.debug(response)

        output = input
        output.response = response
        return output


class ProgressRequestCommand(Command):
    def __init__(self):
        self.parser = ProgressResponseParser()

        super().__init__()

    def submit(self, service_chain_uuid):
        url = f'/progress?service_chain_uuid={service_chain_uuid}'
        response = self.ubl_client.get(url)
        return response

    def service_chain_keys(self, service_chain_uuid):
        response = self.submit(service_chain_uuid)
        parsed_response = self.parser.parse(response)

        return parsed_response.chain_links.keys()

    def call(self, input):
        logger.debug('Calling ProgressRequestCommand')

        service_chain_uuid = input.response['Execution_sent']

        logger.debug(f'Progress update service chain UUID: {service_chain_uuid}')

        output = {}

        for key in self.service_chain_keys(service_chain_uuid):
            state_machine = ProgressStateMachine(
                service_chain_uuid=service_chain_uuid, chain_link=key
            )

            result = state_machine.run()
            output[key] = result

        return output


class IngestionProgressCommand:
    def __init__(self):
        self.client = IngestionClient()

    def submit(self, id):
        result = self.client.get_ingestion_progress(id=id)
        schema = IngestionProgressResponseSchema()
        return schema.load(result)

    def call(self, id):
        result = self.submit(id=id)


# "NONE",
# "QUEUED",
# "IN_PROGRESS",
# "SUCCESS",
# FAILED",
# TIMEOUT"
