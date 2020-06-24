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


class ServiceProviderHeader:
    def __init__(
        self, service_provider_uuid, service_offer_uuid, service_request_uuid,
        service_provider_signature
    ):
        self.service_provider_uuid = service_provider_uuid
        self.service_offer_uuid = service_offer_uuid
        self.service_request_uuid = service_request_uuid
        self.service_provider_signature = service_provider_signature


class Vendor:
    def __init__(self, service_provider_name, service_provider_uuid, service_provider_signature):
        self.service_provider_name = service_provider_name
        self.service_provider_uuid = service_provider_uuid
        self.service_provider_signature = service_provider_signature


class DatasetDetailsInputComponent:
    def __init__(self, data_token, dataset_uuid, dataset_type, cdf_metadata=''):
        self.data_token = data_token
        self.dataset_uuid = dataset_uuid
        self.dataset_type = dataset_type
        self.cdf_metadata = cdf_metadata


class DatasetDetailsOutputComponent:
    def __init__(self, file_uri, dataset_uuid, dataset_type):
        self.file_uri = file_uri
        self.dataset_uuid = dataset_uuid
        self.dataset_type = dataset_type


class ExecutionDetailsComponent:
    def __init__(self, exec_request_uuid, exec_process_uuid):
        self.exec_request_uuid = exec_request_uuid
        self.exec_process_uuid = exec_process_uuid


class Service:
    def __init__(self, catalogue_uuid, description, parameters, name):
        self.catalogue_uuid = catalogue_uuid
        self.description = description
        self.parameters = parameters
        self.name = name


class Dataset:
    def __init__(self, input, output):
        self.input = input
        self.output = output


class Icon:
    def __init__(self, base64, url):
        self.base64 = base64
        self.url = url


class ExecutionCompletion:
    def __init__(
        self, standard_header, service_provider_header, execution_details, exec_comp_code,
        exec_comp_text, exec_completion_timestamp, results_dataset
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.execution_details = execution_details
        self.exec_comp_code = exec_comp_code
        self.exec_comp_text = exec_comp_text
        self.exec_completion_timestamp = exec_completion_timestamp
        self.results_dataset = results_dataset


class ExecutionFailure:
    def __init__(
        self, standard_header, service_provider_header, execution_details, exec_fail_code,
        unfulfilled_service_uuid, exec_fail_text
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.execution_details = execution_details
        self.exec_fail_code = exec_fail_code
        self.unfulfilled_service_uuid = unfulfilled_service_uuid
        self.exec_fail_text = exec_fail_text


class ExecutionRequestAccept:
    def __init__(
        self, standard_header, service_provider_header, execution_details,
        exec_start_timestamp
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.execution_details = execution_details
        self.exec_start_timestamp = exec_start_timestamp


class ExecutionRequestCancel:
    def __init__(self, standard_header, service_provider_header, offer_execution_request_to_cancel):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.offer_execution_request_to_cancel = offer_execution_request_to_cancel


class ExecutionRequestDecline:
    def __init__(
        self, standard_header, service_provider_header, execution_details, decline_reason_text,
        exec_decline_timestamp
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.execution_details = execution_details
        self.decline_reason_text = decline_reason_text
        self.exec_decline_timestamp = exec_decline_timestamp


class ExecutionRequest:
    def __init__(
        self, standard_header, service_provider_header, dataset_input_details,
        dataset_output_details, service_offer_description, execution_parameters, service_offer_name
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.dataset_input_details = dataset_input_details
        self.dataset_output_details = dataset_output_details
        self.service_offer_description = service_offer_description
        self.execution_parameters = execution_parameters
        self.service_offer_name = service_offer_name


class OfferExecutionRequest:
    def __init__(
        self, standard_header, service_provider_header, input_data, output_data,
        service_offer_description, execution_parameters, service_offer_name
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.input_data = input_data
        self.output_data = output_data
        self.service_offer_description = service_offer_description
        self.execution_parameters = execution_parameters
        self.service_offer_name = service_offer_name


class ExecutionStatusUpdate:
    def __init__(
        self, standard_header, service_provider_header, execution_details, exec_status_code,
        exec_status_text, exec_update_timestamp
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.execution_details = execution_details
        self.exec_status_code = exec_status_code
        self.exec_status_text = exec_status_text
        self.exec_update_timestamp = exec_update_timestamp


class ServiceOffering:
    def __init__(
        self, standard_header, service_provider_header, input_data,
        output_data, service_offer_description, service_offer_parameters,
        service_offer_name
    ):
        self.standard_header = standard_header
        self.service_provider_header = service_provider_header
        self.input_data = input_data
        self.output_data = output_data
        self.service_offer_description = service_offer_description
        self.service_offer_parameters = service_offer_parameters
        self.service_offer_name = service_offer_name


class ServiceRequest:
    def __init__(
        self, standard_header, input_data, output_data,
        service_catalogue_uuid, permissible_service_provider_uuid
    ):
        self.standard_header = standard_header
        self.input_data = input_data
        self.output_data = output_data
        self.service_catalogue_uuid = service_catalogue_uuid
        self.permissible_service_provider_uuid = permissible_service_provider_uuid


class Message:
    def __init__(self, message_data, message_type, message_raw):
        self.data = message_data
        self.type = message_type
        self.raw = message_raw


class Config:
    def __init__(
        self, project, topic, subscription, catalogue_uuid, dataset_type, icon_base64, icon_url,
        name, service_description, service_provider_name, service_provider_signature,
        service_provider_uuid, parameters
    ):
        self.project = project
        self.topic = topic
        self.subscription = subscription
        self.catalogue_uuid = catalogue_uuid
        self.dataset_type = dataset_type
        self.name = name
        self.service_description = service_description
        self.service_provider_name = service_provider_name
        self.service_provider_signature = service_provider_signature
        self.service_provider_uuid = service_provider_uuid
        self.icon_base64 = icon_base64
        self.icon_url = icon_url
        self.parameters = parameters
