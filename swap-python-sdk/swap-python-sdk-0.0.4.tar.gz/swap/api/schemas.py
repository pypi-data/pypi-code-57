from marshmallow import Schema, fields, post_load, EXCLUDE
from swap.api.models import (
    ExecutionDetails,
    InputData,
    InputDataset,
    InputDatasetsResponse,
    OutputData,
    ProgressResponse,
    ProgressResponseChainLink,
    ProgressUpdate,
    ResultsDataset,
    ServiceChain,
    ServiceChainParameters,
    ServiceOffer,
    ServiceOfferParameters,
    ServiceOfferProperty,
    ServiceOffersChainLink,
    ServiceOffersResponse,
    ServiceProviderHeader,
    ServiceRequestChainLink,
    StandardHeader,
    IngestionProgressResponse,
    DataID,
)


class ServiceOfferPropertySchema(Schema):
    title = fields.Str()
    type = fields.Str()
    options = fields.List(fields.Str())

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOfferProperty(**other)


class ServiceOfferParametersSchema(Schema):
    properties = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceOfferPropertySchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOfferParameters(**other)


class ServiceOfferSchema(Schema):
    message_id = fields.Str()
    publish_time = fields.Str()
    parameters = fields.Nested(ServiceOfferParametersSchema)
    app_message_uuid = fields.Str()
    request_message_uuid = fields.Str()
    originating_message_uuid = fields.Str()
    service_chain_uuid = fields.Str()
    service_provider_uuid = fields.Str()
    service_offer_uuid = fields.Str()
    service_request_uuid = fields.Str()
    service_provider_signature = fields.Str()
    service_offer_name = fields.Str()
    service_offer_description = fields.Str()
    file_uris = fields.List(fields.Str())

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOffer(**other)


class ServiceOffersChainLinkSchema(Schema):
    message_id = fields.Str()
    service_catalogue_uuid = fields.Str()
    service_offers = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceOfferSchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOffersChainLink(**other)


class ServiceOffersResponseSchema(Schema):
    chain_links = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceOffersChainLinkSchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceOffersResponse(**other)


class ServiceChainParametersSchema(Schema):
    # data_path = fields.Str()
    description_text = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceChainParameters(**other)


class ServiceChainSchema(Schema):
    service_chain_uuid = fields.Str()
    service_offer_uuid = fields.Str()
    service_provider_uuid = fields.Str()
    service_provider_signature = fields.Str()
    originating_message_uuid = fields.Str()
    service_request_uuid = fields.Str()
    parameters = fields.Nested(ServiceChainParametersSchema)

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceChain(**other)


class StandardHeaderSchema(Schema):
    app_message_uuid = fields.Str()
    message_timestamp = fields.Str()
    originating_message_uuid = fields.Str()
    request_message_uuid = fields.Str()
    service_chain = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceChainSchema),
        allow_none=True
    )
    service_chain_uuid = fields.Str()
    user_id = fields.Str()
    user_token = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return StandardHeader(**other)


class InputDataSchema(Schema):
    cdf_metadata = fields.Str(allow_none=True)
    data_token = fields.Str(allow_none=True)
    dataset_type = fields.Str(allow_none=True)
    dataset_uuid = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return InputData(**other)


class OutputDataSchema(Schema):
    dataset_type = fields.Str(allow_none=True)
    dataset_uuid = fields.Str(allow_none=True)
    file_uri = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return OutputData(**other)


class ServiceProviderHeaderSchema(Schema):
    service_offer_uuid = fields.Str()
    service_provider_signature = fields.Str()
    service_provider_uuid = fields.Str()
    service_request_uuid = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceProviderHeader(**other)


class ExecutionDetailsSchema(Schema):
    exec_request_uuid = fields.Str(allow_none=True)
    exec_process_uuid = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return ExecutionDetails(**other)


class ResultsDatasetSchema(Schema):
    file_uri = fields.Str(allow_none=True)
    dataset_uuid = fields.Str(allow_none=True)
    dataset_type = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return ResultsDataset(**other)


class ProgressUpdateSchema(Schema):
    decline_reason_text = fields.Str(allow_none=True)
    exec_comp_code = fields.Str(allow_none=True)
    exec_comp_text = fields.Str(allow_none=True)
    exec_completion_timestamp = fields.Str(allow_none=True)
    exec_decline_timestamp = fields.Str(allow_none=True)
    exec_fail_code = fields.Str(allow_none=True)
    exec_fail_text = fields.Str(allow_none=True)
    exec_start_timestamp = fields.Str(allow_none=True)
    exec_status_code = fields.Str(allow_none=True)
    exec_status_text = fields.Str(allow_none=True)
    exec_update_timestamp = fields.Str(allow_none=True)
    exec_url = fields.Str(allow_none=True)
    execution_details = fields.Nested(ExecutionDetailsSchema)
    execution_parameters = fields.Str(allow_none=True)
    input_data = fields.List(fields.Nested(InputDataSchema))
    message_id = fields.Str(allow_none=True)
    message_type = fields.Str(allow_none=True)
    notification_detail_url = fields.Str(allow_none=True)
    notification_message_url = fields.Str(allow_none=True)
    notification_trigger_timestamp = fields.Str(allow_none=True)
    notification_type = fields.Str(allow_none=True)
    offer_execution_request_to_cancel = fields.Str(allow_none=True)
    output_data = fields.Nested(OutputDataSchema, allow_none=True)
    permissible_service_provider_uuid = fields.Str(allow_none=True)
    publish_time = fields.Str(allow_none=True)
    results_dataset = fields.Nested(ResultsDatasetSchema, allow_none=True)
    service_catalogue_uuid = fields.Str(allow_none=True)
    service_offer_description = fields.Str(allow_none=True)
    service_offer_name = fields.Str(allow_none=True)
    service_offer_parameters = fields.Str(allow_none=True)
    service_provider_header = fields.Nested(ServiceProviderHeaderSchema)
    standard_header = fields.Nested(StandardHeaderSchema)
    subject_name = fields.Str(allow_none=True)
    subject_type_name = fields.Str(allow_none=True)
    unfulfilled_service_uuid = fields.Str(allow_none=True)

    @post_load
    def deserialise(self, other, **kwargs):
        return ProgressUpdate(**other)


class ProgressResponseChainLinkSchema(Schema):
    message_id = fields.Str()
    service_catalogue_uuid = fields.Str()
    progress_updates = fields.List(fields.Nested(ProgressUpdateSchema))

    @post_load
    def deserialise(self, other, **kwargs):
        return ProgressResponseChainLink(**other)


class ProgressResponseSchema(Schema):
    chain_links = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ProgressResponseChainLinkSchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ProgressResponse(**other)


class InputDatasetSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    kind = fields.Str()
    id = fields.Str()
    self_link = fields.Str()
    media_link = fields.Str()
    name = fields.Str()
    bucket = fields.Str()
    generation = fields.Str()
    metageneration = fields.Str()
    content_type = fields.Str()
    storage_class = fields.Str()
    size = fields.Str()
    md5_hash = fields.Str()
    crc32c = fields.Str()
    etag = fields.Str()
    time_created = fields.Str()
    updated = fields.Str()
    time_storage_class_updated = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return InputDataset(**other)


class InputDatasetsResponseSchema(Schema):
    kind = fields.Str()
    next_page_token = fields.Str()
    items = fields.List(fields.Nested(InputDatasetSchema))

    @post_load
    def deserialise(self, other, **kwargs):
        return InputDatasetsResponse(**other)


class ServiceRequestChainLinkSchema(Schema):
    service = fields.Str()
    datasets = fields.List(fields.Dict())

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceRequestChainLink(**other)


class ServiceRequestSchema(Schema):
    service_chain = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceRequestChainLinkSchema)
    )

    @post_load
    def deserialise(self, other, **kwargs):
        return ServiceRequestSchema(**other)


class ServiceExecutionRequestChainLinkParametersSchema(Schema):
    # data_path = fields.Str()
    description_text = fields.Str()


class ServiceExecutionRequestChainLinkSchema(Schema):
    service_chain_uuid = fields.Str()
    service_offer_uuid = fields.Str()
    service_provider_uuid = fields.Str()
    service_provider_signature = fields.Str()
    originating_message_uuid = fields.Str()
    service_request_uuid = fields.Str()
    parameters = fields.Nested(ServiceExecutionRequestChainLinkParametersSchema)


class ServiceExecutionRequestSchema(Schema):
    service_chain = fields.Dict(
        keys=fields.Str(),
        values=fields.Nested(ServiceExecutionRequestChainLinkSchema)
    )


class SurveySchema(Schema):
    survey_name = fields.Str()
    survey_id = fields.Str()


class CustomMetadataItemSchema(Schema):
    metadata_key = fields.Str()
    metadata_value = fields.Str()


class SeismicFileSchema(Schema):
    crs = fields.Str()
    custom_metadata = fields.List(fields.Nested(CustomMetadataItemSchema))


class SeismicMetadataSchema(Schema):
    survey = fields.Nested(SurveySchema)
    file = fields.Nested(SeismicFileSchema)


class DataURLSchema(Schema):
    data_url = fields.Str()
    data_type = fields.Str()
    seismic_metadata = fields.Nested(SeismicMetadataSchema)


class IngestionRequestSchema(Schema):
    action_type = fields.Str()
    target_system = fields.Str()
    data_urls = fields.List(fields.Nested(DataURLSchema))


class DataIDSchema(Schema):
    url = fields.Str()
    name = fields.Str()
    id = fields.Str()
    status = fields.Str()

    @post_load
    def deserialise(self, other, **kwargs):
        return DataID(**other)


class IngestionProgressResponseSchema(Schema):
    data_ids = fields.List(fields.Nested(DataIDSchema))

    @post_load
    def deserialise(self, other, **kwargs):
        return IngestionProgressResponse(**other)
