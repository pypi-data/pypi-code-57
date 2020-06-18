import json
import time
from uuid import uuid4
from swap.common.models import (
    ServiceDiscoveryData,
    ServiceDiscoveryDataset,
    ServiceDiscoveryIcon,
    ServiceDiscoveryParameters,
    ServiceDiscoveryResponse,
    ServiceDiscoveryService,
    ServiceDiscoveryVendor,
)
from swap.common.schemas import (
    ServiceDiscoveryResponseSchema
)
from swap.messaging.models import (
    ServiceOffering,
    ServiceProviderHeader,
    ExecutionFailure,
    ExecutionRequestAccept,
    ExecutionStatusUpdate,
    ExecutionCompletion,
)
from swap.messaging.schemas import (
    ServiceOfferingSchema,
    ExecutionFailureSchema,
    ExecutionRequestAcceptSchema,
    ExecutionStatusUpdateSchema,
    ExecutionCompletionSchema,
)


class ServiceDiscoveryResponseBuilder:
    def __init__(self, config):
        self.config = config

    def service_discovery_vendor(self):
        return ServiceDiscoveryVendor(
            service_provider_name=self.config.service_provider_name,
            service_provider_uuid=self.config.service_provider_uuid,
            service_provider_signature=self.config.service_provider_signature
        )

    def service_discovery_parameters(self):
        return ServiceDiscoveryParameters(
            properties=self.config.parameters
        )

    def service_discovery_service(self):
        return ServiceDiscoveryService(
            name=self.config.name,
            catalogue_uuid=self.config.catalogue_uuid,
            service_description=self.config.service_description,
            parameters=self.service_discovery_parameters()
        )

    def service_discovery_dataset(self):
        return ServiceDiscoveryDataset(
            input=self.config.dataset_type,
            output=self.config.dataset_type
        )

    def service_discovery_icon(self):
        return ServiceDiscoveryIcon(
            base64=self.config.icon_base64,
            url=self.config.icon_url
        )

    def service_discovery_response_data(self):
        return ServiceDiscoveryData(
            vendor=self.service_discovery_vendor(),
            service=self.service_discovery_service(),
            dataset=self.service_discovery_dataset(),
            icon=self.service_discovery_icon()
        )

    def service_discovery_response(self):
        return ServiceDiscoveryResponse(
            data=[self.service_discovery_response_data()]
        )

    def build(self):
        schema = ServiceDiscoveryResponseSchema()
        output = schema.dump(self.service_discovery_response())

        return json.dumps(output, indent=2)


class ServiceOfferingBuilder:
    def __init__(self, message_id, config, service_request):
        self.config = config
        self.service_request = service_request
        self.message_id = message_id

    def service_provider_header(self):
        return ServiceProviderHeader(
            service_provider_uuid=self.config.service_provider_uuid,
            service_offer_uuid=str(uuid4()),
            service_request_uuid=self.message_id,
            service_provider_signature=self.config.service_provider_signature,
        )

    def build(self):
        self.service_request.standard_header.request_message_uuid = self.message_id
        self.service_request.standard_header.originating_message_uuid = self.message_id

        service_offering = ServiceOffering(
            standard_header=self.service_request.standard_header,
            service_provider_header=self.service_provider_header(),
            input_data=self.service_request.input_data,
            output_data=self.service_request.output_data,
            service_offer_description=self.config.service_description,
            service_offer_parameters=self.config.parameters,
            service_offer_name=self.config.name,
        )

        schema = ServiceOfferingSchema()
        output = schema.dump(service_offering)

        return json.dumps(output, indent=2)


class ExecutionFailureBuilder:
    def __init__(
        self, message_id, offer_execution_request, execution_details={}, exec_fail_code='',
        exec_fail_text=''
    ):
        self.message_id = message_id
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_fail_code = exec_fail_code
        self.exec_fail_text = exec_fail_text

    def build(self):
        unfulfilled_uuid = self.offer_execution_request.service_provider_header.service_offer_uuid

        self.offer_execution_request.standard_header.request_message_uuid = self.message_id

        execution_failure = ExecutionFailure(
            standard_header=self.offer_execution_request.standard_header,
            service_provider_header=self.offer_execution_request.service_provider_header,
            execution_details=self.execution_details,
            exec_fail_code=self.exec_fail_code,
            exec_fail_text=self.exec_fail_text,
            unfulfilled_service_uuid=unfulfilled_uuid,
        )

        schema = ExecutionFailureSchema()
        output = schema.dump(execution_failure)

        return json.dumps(output, indent=2)


class ExecutionRequestAcceptBuilder:
    def __init__(self, message_id, offer_execution_request, execution_details={}):
        self.message_id = message_id
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details

    def build(self):
        self.offer_execution_request.standard_header.request_message_uuid = self.message_id

        execution_request_accept = ExecutionRequestAccept(
            standard_header=self.offer_execution_request.standard_header,
            service_provider_header=self.offer_execution_request.service_provider_header,
            execution_details=self.execution_details,
            exec_start_timestamp=time.time()
        )

        schema = ExecutionRequestAcceptSchema()
        output = schema.dump(execution_request_accept)

        return json.dumps(output, indent=2)


class ExecutionStatusUpdateBuilder:
    def __init__(
        self, message_id, offer_execution_request, execution_details={}, exec_status_code='',
        exec_status_text=''
    ):
        self.message_id = message_id
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_status_code = exec_status_code
        self.exec_status_text = exec_status_text

    def build(self):
        self.offer_execution_request.standard_header.request_message_uuid = self.message_id

        update = ExecutionStatusUpdate(
            standard_header=self.offer_execution_request.standard_header,
            service_provider_header=self.offer_execution_request.service_provider_header,
            execution_details=self.execution_details,
            exec_status_code=self.exec_status_code,
            exec_status_text=self.exec_status_text,
            exec_update_timestamp=time.time()
        )

        schema = ExecutionStatusUpdateSchema()
        output = schema.dump(update)

        return json.dumps(output, indent=2)


class ExecutionCompletionBuilder:
    def __init__(
        self, message_id, offer_execution_request, execution_details={}, exec_comp_code='',
        exec_comp_text=''
    ):
        self.message_id = message_id
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_comp_code = exec_comp_code
        self.exec_comp_text = exec_comp_text

    def build(self):
        self.offer_execution_request.standard_header.request_message_uuid = self.message_id

        update = ExecutionCompletion(
            standard_header=self.offer_execution_request.standard_header,
            service_provider_header=self.offer_execution_request.service_provider_header,
            execution_details=self.execution_details,
            exec_comp_code=self.exec_comp_code,
            exec_comp_text=self.exec_comp_text,
            results_dataset=self.offer_execution_request.output_data,
            exec_completion_timestamp=time.time()
        )

        schema = ExecutionCompletionSchema()
        output = schema.dump(update)

        return json.dumps(output, indent=2)
