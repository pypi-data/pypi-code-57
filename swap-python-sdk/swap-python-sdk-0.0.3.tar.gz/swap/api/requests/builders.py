from swap.api.models import (
    ServiceExecutionRequest,
    ServiceExecutionRequestChainLink,
    ServiceExecutionRequestChainLinkParameters,
    IngestionRequest,
    DataURL,
    SeismicMetadata,
    Survey,
    SeismicFile,
    CustomMetadataItem,
)
from swap.api.schemas import IngestionRequestSchema
from swap.common.utils import CaseConverter


class ServiceExecutionRequestBuilder:
    def build(self, input):
        service_chain = {}
        data_paths = []

        for dataset in input.service_chain.datasets:
            data_paths.append(dataset.name)

        for chain_link_key, service_offer in input.response.items():
            chain_link_parameters = ServiceExecutionRequestChainLinkParameters(
                data_paths=data_paths,
                description_text=''
            )

            service_execution_request_chain_link = ServiceExecutionRequestChainLink(
                service_chain_uuid=service_offer.service_chain_uuid,
                service_offer_uuid=service_offer.service_offer_uuid,
                service_provider_uuid=service_offer.service_provider_uuid,
                service_provider_signature=service_offer.service_provider_signature,
                originating_message_uuid=service_offer.originating_message_uuid,
                service_request_uuid=service_offer.service_request_uuid,
                parameters=chain_link_parameters
            )

            service_chain[chain_link_key] = service_execution_request_chain_link

        service_execution_request = ServiceExecutionRequest(
            service_chain=service_chain
        )

        return service_execution_request


class TriggerIngestionRequestBuilder:
    def build_custom_metadata(self):
        return [CustomMetadataItem(**item) for item in self.custom_metadata]

    def build_file(self):
        return SeismicFile(
            crs=self.crs,
            custom_metadata=self.build_custom_metadata()
        )

    def build_survey(self):
        return Survey(
            survey_id=self.survey_id,
            survey_name=''
        )

    def build_seismic_metadata(self):
        return SeismicMetadata(
            survey=self.build_survey(),
            file=self.build_file()
        )

    def build_data_url(self):
        return DataURL(
            data_url=self.data_url,
            data_type='SEISMIC',
            seismic_metadata=self.build_seismic_metadata()
        )

    def build(self, data_url, survey_id, crs, custom_metadata=[]):
        self.data_url = data_url
        self.survey_id = survey_id
        self.crs = crs
        self.custom_metadata = custom_metadata

        ingestion_request = IngestionRequest(
            action_type='TRIGGER_INGESTION',
            target_system='CDF',
            data_urls=[self.build_data_url()]
        )

        schema = IngestionRequestSchema()
        result = dict(schema.dump(ingestion_request))

        converter = CaseConverter()
        return converter.convert_to_camel_case(result)
