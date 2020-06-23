"""
    Personalize recommendations manager module
"""
import json
import sdc_helpers.utils as utils
from sdc_helpers.models.client import Client
import boto3
from sdc_engine_helpers.personalize.manager import Manager


class RecommendationsManager(Manager):
    """
        Manages retrieval of Personalize recommendations for a given set of parameters
    """
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
            client_id=client.id,
            item_id=item_id
        )

        results = self.redis_helper.redis_get(key=cache_key)

        if not results:
            campaign_kwargs = {
                'recipe': self.parameters.get('recipe', 'related_items'),
                'event_type': self.parameters.get('eventType', 'all')
            }
            campaign = self.query_helper.get_campaign(
                client_id=client.id,
                service_id=self.service.id,
                engine_slug=self.engine_slug,
                **campaign_kwargs
            )

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
                'client': client.name,
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

    def get_results(self, *, client: Client, campaign_arn: str, default_results: list) -> list:
        """
            Determine the results for this request

            args:
                client (Client): The client requesting the recommendation
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
                    .format(client_name=client.name)
                )

            results = []

        return results
