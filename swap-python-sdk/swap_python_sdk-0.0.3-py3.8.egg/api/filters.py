import re
from swap.common.filters import Filter
from swap.common.logging import logger
from swap.api.sequences.step_codes import StepCode

class InputDatasetsResponseFilter(Filter):
    def required_keys(self):
        return [
            'kind', 'id', 'self_link', 'media_link', 'name', 'bucket', 'generation',
            'metageneration', 'content_type', 'storage_class', 'size', 'md5_hash', 'crc32c', 'etag',
            'time_created', 'updated', 'time_storage_class_updated'
        ]

    def keys_to_correct(self):
        return [
            'selfLink', 'mediaLink', 'contentType', 'storageClass', 'md5Hash', 'timeCreated',
            'timeStorageClassUpdated'
        ]

    def correct_next_page_token(self):
        if 'nextPageToken' in self.response:
            next_page_token = self.response.pop('nextPageToken')
            self.response['next_page_token'] = next_page_token

    def correct_case(self):
        for index, item in enumerate(self.response['items']):
            for key in self.required_keys():
                if key not in item:
                    item[key] = ''

            for key in self.keys_to_correct():
                if key not in item:
                    continue

                value = item.pop(key)
                split_key = re.split('(?=[A-Z])', key)
                snake_case_key = '_'.join([x.lower() for x in split_key])

                item[snake_case_key] = value

            self.response['items'][index] = item

    def apply(self, response):
        self.response = response

        self.correct_next_page_token()
        self.correct_case()

        return self.response


class ServiceOffersResponseFilter(Filter):
    def wrap_response(self):
        self.response = {'chain_links': self.response}

    def correct_case(self):
        for chain_link_key, chain_link in self.response.items():
            if not chain_link['service_offers'].items():
                logger.info(f'No service offers received yet for service: {chain_link["service_catalogue_uuid"]}')
                return StepCode.NoServiceOffersReceived
            for service_offer_key, service_offer in chain_link['service_offers'].items():
                if 'messageId' in service_offer:
                    message_id_value = service_offer.pop('messageId')
                    service_offer['message_id'] = message_id_value

                if 'publishTime' in service_offer:
                    publish_time_value = service_offer.pop('publishTime')
                    service_offer['publish_time'] = publish_time_value

                if 'Parameters' in service_offer:
                    del service_offer['Parameters']
                    service_offer['parameters'] = {'properties': {}}

    def apply(self, response):
        self.response = response

        self.correct_case()
        self.wrap_response()

        return self.response


class ProgressResponseFilter(Filter):
    def correct_case_and_type(self):
        for chain_link_key, chain_link in self.response.items():
            for progress_update in chain_link['progress_updates']:
                message_id = progress_update.pop('messageId')
                progress_update['message_id'] = message_id

                publish_time = progress_update.pop('publishTime')
                progress_update['publish_time'] = publish_time

                if type(progress_update['standard_header']['service_chain']) == str:
                    progress_update['standard_header']['service_chain'] = {}

                if type(progress_update['input_data']) == str:
                    progress_update['input_data'] = {
                        'cdf_metadata': 'None',
                        'data_token': 'None',
                        'dataset_type': 'None',
                        'dataset_uuid': 'None'
                    }

                if type(progress_update['output_data']) == str:
                    progress_update['output_data'] = {
                        'dataset_type': 'None',
                        'dataset_uuid': 'None',
                        'file_uri': 'None'
                    }

                if type(progress_update['results_dataset']) == str:
                    progress_update['results_dataset'] = {
                        'file_uri': 'None',
                        'dataset_uuid': 'None',
                        'dataset_type': 'None'
                    }

    def apply(self, response):
        self.response = response

        self.correct_case_and_type()

        return {'chain_links': self.response}
