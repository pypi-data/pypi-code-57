class ServiceOffersResponse:
    def __init__(self, chain_links):
        self.chain_links = chain_links

    def add_chain_link(self, chain_link):
        self.chain_links[chain_link.key] = chain_link
        setattr(self, chain_link.key, chain_link)


class ServiceOffersChainLink:
    def __init__(self, message_id, service_catalogue_uuid, service_offers):
        self.message_id = message_id
        self.service_catalogue_uuid = service_catalogue_uuid
        self.service_offers = service_offers

    def add_service_offer(self, service_offer):
        self.service_offers[service_offer.key] = service_offer


class ServiceOffer:
    def __init__(
        self, message_id, publish_time, parameters, app_message_uuid, request_message_uuid,
        originating_message_uuid, service_chain_uuid, service_provider_uuid, service_offer_uuid,
        service_request_uuid, service_provider_signature, service_offer_name,
        service_offer_description, file_uris
    ):
        self.message_id = message_id
        self.publish_time = publish_time
        self.parameters = parameters
        self.app_message_uuid = app_message_uuid
        self.request_message_uuid = request_message_uuid
        self.originating_message_uuid = originating_message_uuid
        self.service_chain_uuid = service_chain_uuid
        self.service_provider_uuid = service_provider_uuid
        self.service_offer_uuid = service_offer_uuid
        self.service_request_uuid = service_request_uuid
        self.service_provider_signature = service_provider_signature
        self.service_offer_name = service_offer_name
        self.service_offer_description = service_offer_description
        self.file_uris = file_uris


class ServiceOfferParameters:
    def __init__(self, properties):
        self.properties = properties

    def add_property(self, property):
        self.properties[property.key] = property


class ServiceOfferProperty:
    def __init__(self, title, type, options):
        self.title = title
        self.type = type
        self.options = options


class ProgressResponse:
    def __init__(self, chain_links):
        self.chain_links = chain_links

    def add_chain_link(self, chain_link):
        self.chain_links[chain_link.key] = chain_link
        setattr(self, chain_link.key, chain_link)


class ProgressResponseChainLink:
    def __init__(self, message_id, service_catalogue_uuid, progress_updates):
        self.message_id = message_id
        self.service_catalogue_uuid = service_catalogue_uuid
        self.progress_updates = progress_updates


class ProgressUpdate:
    def __init__(
        self, standard_header, input_data, output_data, service_catalogue_uuid,
        permissible_service_provider_uuid, service_provider_header, service_offer_description,
        service_offer_parameters, service_offer_name, execution_parameters,
        offer_execution_request_to_cancel, execution_details, exec_start_timestamp,
        decline_reason_text, exec_decline_timestamp, exec_status_code, exec_status_text,
        exec_update_timestamp, exec_comp_text, exec_comp_code, results_dataset,
        exec_completion_timestamp, unfulfilled_service_uuid, exec_fail_text, exec_fail_code,
        notification_type, subject_type_name, subject_name, notification_message_url,
        notification_detail_url, notification_trigger_timestamp, publish_time, message_type,
        message_id, exec_url
    ):
        self.decline_reason_text = decline_reason_text
        self.exec_comp_code = exec_comp_code
        self.exec_comp_text = exec_comp_text
        self.exec_completion_timestamp = exec_completion_timestamp
        self.exec_decline_timestamp = exec_decline_timestamp
        self.exec_fail_code = exec_fail_code
        self.exec_fail_text = exec_fail_text
        self.exec_start_timestamp = exec_start_timestamp
        self.exec_status_code = exec_status_code
        self.exec_status_text = exec_status_text
        self.exec_update_timestamp = exec_update_timestamp
        self.exec_url = exec_url
        self.execution_details = execution_details
        self.execution_parameters = execution_parameters
        self.input_data = input_data
        self.message_id = message_id
        self.message_type = message_type
        self.notification_detail_url = notification_detail_url
        self.notification_message_url = notification_message_url
        self.notification_trigger_timestamp = notification_trigger_timestamp
        self.notification_type = notification_type
        self.offer_execution_request_to_cancel = offer_execution_request_to_cancel
        self.output_data = output_data
        self.permissible_service_provider_uuid = permissible_service_provider_uuid
        self.publish_time = publish_time
        self.results_dataset = results_dataset
        self.service_catalogue_uuid = service_catalogue_uuid
        self.service_offer_description = service_offer_description
        self.service_offer_name = service_offer_name
        self.service_offer_parameters = service_offer_parameters
        self.service_provider_header = service_provider_header
        self.standard_header = standard_header
        self.subject_name = subject_name
        self.subject_type_name = subject_type_name
        self.unfulfilled_service_uuid = unfulfilled_service_uuid


class StandardHeader:
    def __init__(
        self, app_message_uuid, request_message_uuid, originating_message_uuid, service_chain_uuid,
        message_timestamp, user_token, user_id, service_chain
    ):
        self.app_message_uuid = app_message_uuid
        self.request_message_uuid = request_message_uuid
        self.originating_message_uuid = originating_message_uuid
        self.service_chain_uuid = service_chain_uuid
        self.message_timestamp = message_timestamp
        self.user_token = user_token
        self.user_id = user_id
        self.service_chain = service_chain


class InputData:
    def __init__(self, data_token, dataset_uuid, dataset_type, cdf_metadata):
        self.data_token = data_token
        self.dataset_uuid = dataset_uuid
        self.dataset_type = dataset_type
        self.cdf_metadata = cdf_metadata


class OutputData:
    def __init__(self, file_uri, dataset_uuid, dataset_type):
        self.file_uri = file_uri
        self.dataset_uuid = dataset_uuid
        self.dataset_type = dataset_type


class ServiceProviderHeader:
    def __init__(
        self, service_provider_uuid, service_offer_uuid, service_request_uuid,
        service_provider_signature
    ):
        self.service_provider_uuid = service_provider_uuid
        self.service_offer_uuid = service_offer_uuid
        self.service_request_uuid = service_request_uuid
        self.service_provider_signature = service_provider_signature


class ExecutionDetails:
    def __init__(self, exec_request_uuid, exec_process_uuid):
        self.exec_request_uuid = exec_request_uuid
        self.exec_process_uuid = exec_process_uuid


class ResultsDataset:
    def __init__(self, file_uri, dataset_uuid, dataset_type):
        self.file_uri = file_uri
        self.dataset_uuid = dataset_uuid
        self.dataset_type = dataset_type


class ServiceChainParameters:
    def __init__(self, description_text):
    # def __init__(self, data_path, description_text):
        # self.data_path = data_path
        self.description_text = description_text


class ServiceChain:
    def __init__(
        self, service_chain_uuid, service_offer_uuid, service_provider_uuid,
        service_provider_signature, originating_message_uuid, service_request_uuid, parameters
    ):
        self.service_chain_uuid = service_chain_uuid
        self.service_offer_uuid = service_offer_uuid
        self.service_provider_uuid = service_provider_uuid
        self.service_provider_signature = service_provider_signature
        self.originating_message_uuid = originating_message_uuid
        self.service_request_uuid = service_request_uuid
        self.parameters = parameters


class InputDataset:
    def __init__(
        self, kind, id, self_link, media_link, name, bucket, generation, metageneration,
        content_type, storage_class, size, md5_hash, crc32c, etag, time_created, updated,
        time_storage_class_updated
    ):
        self.kind = kind
        self.id = id
        self.self_link = self_link
        self.media_link = media_link
        self.name = name
        self.bucket = bucket
        self.generation = generation
        self.metageneration = metageneration
        self.content_type = content_type
        self.storage_class = storage_class
        self.size = size
        self.md5_hash = md5_hash
        self.crc32c = crc32c
        self.etag = etag
        self.time_created = time_created
        self.updated = updated
        self.time_storage_class_updated = time_storage_class_updated


class InputDatasetsResponse:
    def __init__(self, kind, next_page_token, items):
        self.kind = kind
        self.next_page_token = next_page_token
        self.items = items


class ServiceRequestChainLink:
    def __init__(self, service, datasets):
        self.service = service
        self.datasets = datasets


class ServiceRequest:
    def __init__(self, service_chain):
        self.service_chain = service_chain

    def chain_link_count(self):
        return len(self.service_chain.keys())

    def add_chain_link(self, chain_link):
        index = self.chain_link_count() + 1
        self.service_chain[f'chain_link_{index}'] = chain_link


class ServiceExecutionRequestChainLinkParameters:
    def __init__(self, data_paths, description_text):
        self.data_paths = data_paths
        self.description_text = description_text

    def add_parameter(self, key, value):
        setattr(self, key, value)


class ServiceExecutionRequestChainLink:
    def __init__(
        self, service_chain_uuid, service_offer_uuid, service_provider_uuid,
        service_provider_signature, originating_message_uuid, service_request_uuid, parameters
    ):
        self.service_chain_uuid = service_chain_uuid
        self.service_offer_uuid = service_offer_uuid
        self.service_provider_uuid = service_provider_uuid
        self.service_provider_signature = service_provider_signature
        self.originating_message_uuid = originating_message_uuid
        self.service_request_uuid = service_request_uuid
        self.parameters = parameters


class ServiceExecutionRequest:
    def __init__(self, service_chain):
        self.service_chain = service_chain


class ServiceParameters:
    def __init__(self, params):
        self.params = params.properties.values()
        self.configuration = {}

    def describe(self):
        for parameter in self.params:
            print('PARAMETER_TITLE:', parameter.title)
            print('PARAMETER_TYPE:', parameter.type)
            print('PARAMETER_OPTIONS:', parameter.options)

    def items(self):
        return self.params

    def configure(self, title, value):
        self.configuration[title] = value


class Service:
    def __init__(self, service_discovery_data, chain_link=''):
        self.service = service_discovery_data.service
        self.name = self.service.name
        self.params = ServiceParameters(self.service.parameters)
        self.service_discovery_data = service_discovery_data
        self.chain_link = chain_link


class WorkflowServiceChain:
    def __init__(self, datasets, services):
        self.datasets = datasets
        self.services = services
        self.chain_link_index = 1

    def add_service(self, service):
        service.chain_link = f'chain_link_{self.chain_link_index}'
        self.services.append(service)
        self.chain_link_index += 1

    def add_dataset(self, dataset):
        if dataset.dataset_type != 'GCS' and dataset.dataset_type != 'CDF':
            raise Exception(f'Unknown dataset type: "{dataset.dataset_type}"')
        self.datasets.append(dataset)


class CommandInput:
    def __init__(self, response, service_chain):
        self.response = response
        self.service_chain = service_chain


class IngestionRequest:
    def __init__(self, action_type, target_system, data_urls):
        self.action_type = action_type
        self.target_system = target_system
        self.data_urls = data_urls


class DataURL:
    def __init__(self, data_url, data_type, seismic_metadata):
        self.data_url = data_url
        self.data_type = data_type
        self.seismic_metadata = seismic_metadata


class SeismicMetadata:
    def __init__(self, survey, file):
        self.survey = survey
        self.file = file


class Survey:
    def __init__(self, survey_name, survey_id):
        self.survey_name = survey_name
        self.survey_id = survey_id


class SeismicFile:
    def __init__(self, crs, custom_metadata):
        self.crs = crs
        self.custom_metadata = custom_metadata


class CustomMetadataItem:
    def __init__(self, metadata_key, metadata_value):
        self.metadata_key = metadata_key
        self.metadata_value = metadata_value


class DataID:
    def __init__(self, url, name, id, status):
        self.url = url
        self.name = name
        self.id = id
        self.status = status


class IngestionProgressResponse:
    def __init__(self, data_ids):
        self.data_ids = data_ids
