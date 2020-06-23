"""
    Personalize abstract manager module
"""
from sdc_helpers.models.client import Client
from sdc_helpers.redis_helper import RedisHelper
from sdc_engine_helpers.engine_query_helper import EngineQueryHelper

class Manager:
    """
        Abstract manager class to be inherited by various Personalize managers
    """
    service = None
    engine_slug = None
    query_helper = None
    redis_helper = None
    parameters = None

    def __init__(self, **kwargs):
        query_helper_kwargs = dict(filter(lambda item: item[0] == 'rds_config', kwargs.items()))
        redis_helper_kwargs = dict(filter(lambda item: item[0] == 'redis_config', kwargs.items()))
        self.query_helper = EngineQueryHelper(**query_helper_kwargs)
        self.redis_helper = RedisHelper(**redis_helper_kwargs)
        self.service = self.query_helper.get_service(slug=kwargs.pop('service_slug', 'recommend'))
        self.engine_slug = kwargs.pop('engine_slug', 'personalize')
        self.parameters = kwargs

    def __del__(self):
        del self.query_helper
        del self.redis_helper

    def get_client(self) -> Client:
        """
            Determine the client with the supplied parameters

            returns:
                client (Client): The determined client

        """
        client = None

        client_id = self.parameters.get('client_id', None)
        if client_id is not None:
            client = self.query_helper.get_client(client_id=client_id)
        else:
            api_key_id = self.parameters.get('api_key_id', None)
            if api_key_id is not None:
                client = self.query_helper.get_client(api_key_id=api_key_id)

        if client is None:
            raise Exception('ClientError: Could not determine client for this request')

        return client
