from marshmallow import Schema, fields, post_load
from swap.messaging.models import (
    Dataset,
    DatasetDetailsInputComponent,
    DatasetDetailsOutputComponent,
    ExecutionCompletion,
    ExecutionDetailsComponent,
    ExecutionFailure,
    ExecutionRequest,
    ExecutionRequestAccept,
    ExecutionRequestCancel,
    ExecutionRequestDecline,
    ExecutionStatusUpdate,
    Icon,
    OfferExecutionRequest,
    Service,
    ServiceOffering,
    ServiceProviderHeader,
    ServiceRequest,
    StandardHeader,
    Vendor,
)


class StandardHeaderSchema(Schema):
    app_message_uuid = fields.Str()
    request_message_uuid = fields.Str()
    originating_message_uuid = fields.Str()
    service_chain_uuid = fields.Str()
    message_timestamp = fields.Str()
    user_token = fields.Str()
    user_id = fields.Str()
    service_chain = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return StandardHeader(**other)


class ServiceProviderHeaderSchema(Schema):
    service_provider_uuid = fields.Str()
    service_offer_uuid = fields.Str()
    service_request_uuid = fields.Str()
    service_provider_signature = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceProviderHeader(**other)


class VendorSchema(Schema):
    service_provider_name = fields.Str()
    service_provider_uuid = fields.Str()
    service_provider_signature = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return Vendor(**other)


class DatasetDetailsInputComponentSchema(Schema):
    class Meta:
        partial = True

    data_token = fields.Str()
    dataset_uuid = fields.Str()
    dataset_type = fields.Str()
    cdf_metadata = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return DatasetDetailsInputComponent(**other)


class DatasetDetailsOutputComponentSchema(Schema):
    file_uri = fields.Str()
    dataset_uuid = fields.Str()
    dataset_type = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return DatasetDetailsOutputComponent(**other)


class ExecutionDetailsComponentSchema(Schema):
    exec_request_uuid = fields.Str()
    exec_process_uuid = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionDetailsComponent(**other)


class ServiceSchema(Schema):
    catalogue_uuid = fields.Str()
    description = fields.Str()
    parameters = fields.Str()
    name = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return Service(**other)


class DatasetSchema(Schema):
    input = fields.Str()
    output = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return Dataset(**other)


class IconSchema(Schema):
    base64 = fields.Str()
    url = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return Icon(**other)


class ExecutionCompletionSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    execution_details = fields.Nested(ExecutionDetailsComponentSchema)
    exec_comp_code = fields.Str()
    exec_comp_text = fields.Str()
    exec_completion_timestamp = fields.Str()
    results_dataset = fields.Nested(DatasetDetailsOutputComponentSchema)

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionCompletion(**other)


class ExecutionFailureSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    execution_details = fields.Nested(ExecutionDetailsComponentSchema)
    exec_fail_code = fields.Str()
    unfulfilled_service_uuid = fields.Str()
    exec_fail_text = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionFailure(**other)


class ExecutionRequestAcceptSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    execution_details = fields.Nested(ExecutionDetailsComponentSchema)
    exec_start_timestamp = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionRequestAccept(**other)


class ExecutionRequestCancelSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    offer_execution_request_to_cancel = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionRequestCancel(**other)


class ExecutionRequestDeclineSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    execution_details = fields.Nested(ExecutionDetailsComponentSchema)
    decline_reason_text = fields.Str()
    exec_decline_timestamp = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionRequestDecline(**other)


class ExecutionRequestSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    dataset_input_details = fields.List(fields.Nested(DatasetDetailsInputComponentSchema))
    dataset_output_details = fields.Nested(DatasetDetailsOutputComponentSchema)
    service_offer_description = fields.Str()
    execution_parameters = fields.Str()
    service_offer_name = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionRequest(**other)


class OfferExecutionRequestSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    input_data = fields.List(fields.Nested(DatasetDetailsInputComponentSchema))
    output_data = fields.Nested(DatasetDetailsOutputComponentSchema)
    service_offer_description = fields.Str()
    execution_parameters = fields.Str()
    service_offer_name = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return OfferExecutionRequest(**other)


class ExecutionStatusUpdateSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    execution_details = fields.Nested(ExecutionDetailsComponentSchema)
    exec_status_code = fields.Str()
    exec_status_text = fields.Str()
    exec_update_timestamp = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionStatusUpdate(**other)


class ServiceOfferingSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    input_data = fields.List(fields.Nested(DatasetDetailsInputComponentSchema))
    output_data = fields.Nested(DatasetDetailsOutputComponentSchema)
    service_offer_description = fields.Str()
    service_offer_parameters = fields.Str()
    service_offer_name = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOffering(**other)


class ServiceRequestSchema(Schema):
    standard_header = fields.Nested(StandardHeaderSchema)
    input_data = fields.List(fields.Nested(DatasetDetailsInputComponentSchema))
    output_data = fields.Nested(DatasetDetailsOutputComponentSchema)
    service_catalogue_uuid = fields.Str()
    permissible_service_provider_uuid = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceRequest(**other)
