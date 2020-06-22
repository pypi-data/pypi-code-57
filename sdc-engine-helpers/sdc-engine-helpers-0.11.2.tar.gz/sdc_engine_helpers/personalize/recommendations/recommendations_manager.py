"""
    Personalize recommendations manager module
"""
import json
import boto3
import sdc_helpers.utils as utils
from sdc_helpers.query_helper import QueryHelper
from sdc_helpers.redis_helper import RedisHelper
import sdc_engine_helpers.helpers as helpers

class RecommendationsManager:
    """
        Manages retrieval of Personalize recommendations for a given set of parameters
    """
    service = None
    query_helper = None
    redis_helper = None
    parameters = None

    def __init__(self, **kwargs):
        self.query_helper = QueryHelper()
        self.redis_helper = RedisHelper()
        self.service = self.query_helper.get_service(slug='recommend')
        self.parameters = kwargs

    def __del__(self):
        del self.query_helper
        del self.redis_helper

    def get_recommendations(self):
        """
            Get the recommendations for the specified parameters

            returns:
                results (dict): Results from the Personalize invocation
        """
        client = self.get_client()

        item_id = self.parameters.get('itemId')

        if not item_id:
            raise Exception('ClientError: `itemId` is required')

        cache_key = 'recommend-{client_id}-{item_id}'.format(
            client_id=client['id'],
            item_id=item_id
        )

        results = self.redis_helper.redis_get(key=cache_key)

        if not results:
            campaign = self.get_campaign(client)

            if not campaign:
                raise Exception('ServerError: Could not determine campaign for this client')

            campaign_arn = campaign['arn']
            default_results = campaign.get('default_results', [])

            results = self.get_results(
                client=client,
                campaign_arn=campaign_arn,
                default_results=default_results
            )

            self.redis_helper.redis_set(
                key=cache_key,
                value=json.dumps(results),
                expiry=7200
            )
        else:
            results = json.loads(results)

        domain = utils.dict_query(
            dictionary=self.parameters,
            path='context.domain'
        )

        session_hash = utils.dict_query(
            dictionary=self.parameters,
            path='context.sessionHash'
        )

        trigger_log = {
            'trigger': {
                'client': client['name'],
                'type': 'recommendations',
                'data': {
                    'domain': domain,
                    'item_id': item_id,
                    'session_hash': session_hash,
                    'results': results
                }
            }
        }

        print(json.dumps(trigger_log))

        return results

    def get_client(self) -> dict:
        """
            Determine the client with the supplied parameters

            returns:
                client (dict): The determined client

        """
        client = None

        client_id = self.parameters.get('client_id', None)
        if client_id is not None:
            client = self.query_helper.get_client(client_id=client_id)

        api_key_id = self.parameters.get('api_key_id', None)
        if api_key_id is not None:
            client = self.query_helper.get_client(api_key_id=api_key_id)

        if client is None:
            raise Exception('ClientError: Could not determine client for this request')

        return client

    def get_campaign(self, client: dict):
        """
            Determine the campaign with the supplied parameters

            args:
                client (dict): The determined client

            returns:
                campaign (dict): Campaign from the database if found

        """
        recipe = self.parameters.get('recipe', 'related_items')
        event_type = self.parameters.get('eventType', 'all')

        subscription_properties = self.query_helper.get_subscription_properties(
            client_id=client['id'],
            service_id=self.service['id']
        )

        if subscription_properties is not None:
            engine = helpers.get_engine(
                properties=subscription_properties,
                slug='personalize'
            )

            if engine is not None:
                return helpers.get_campaign(
                    engine=engine,
                    recipe=recipe,
                    event_type=event_type
                )

        return None

    def get_results(self, *, client: dict, campaign_arn: str, default_results: list) -> list:
        """
            Determine the results for this request

            args:
                client (object): The client requesting the recommendation
                campaign_arn (str): The AWS Personalize campaign ARN
                default_results (list): The campaign's default results. If the recommendations
                                        are similar to the default results, an empty results
                                        list is returned as the default results are returned
                                        for an an item that does not exist in the solution the
                                        campaign is referencing

            returns:
                results (list): Results from the Personalize invocation

        """
        item_id = self.parameters.get('itemId')
        num_results = self.parameters.get('numResults', 25)

        results = []

        try:
            personalize_runtime = boto3.client('personalize-runtime')

            response = personalize_runtime.get_recommendations(
                campaignArn=campaign_arn,
                itemId=item_id,
                numResults=num_results
            )
        except Exception as ex:
            raise Exception('ServerError: {exception}'.format(exception=str(ex)))

        for item in response['itemList']:
            results.append(item['itemId'])

        # Check if the results are the same or similar to the default results
        # and return empty array if so
        intersection = set(default_results).intersection(results)

        if (
                len(results) == len(intersection) or
                len(intersection) / len(results) >= 0.8
        ):
            if len(results) != len(intersection):
                print(
                    'Results for {client_name} are similar but not the same to the default results '
                    'which probably means default results are out of sync. Saving default results'
                    .format(client_name=client['name'])
                )

            results = []

        return results
