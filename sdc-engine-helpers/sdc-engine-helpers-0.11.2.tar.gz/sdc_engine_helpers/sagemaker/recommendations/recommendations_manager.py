"""
    Sagemaker recommendations manager module
"""
import json
import boto3
import sdc_helpers.utils as utils
from sdc_helpers.redis_helper import RedisHelper
from sdc_engine_helpers.sagemaker.sagemaker_query_helpers import \
    SagemakerEngineHelpers

class RecommendationsManager:
    """
        Manages retrieval of Sagemaker recommendations for a given set of parameters
    """
    client = {}
    engine = None

    def __init__(self, **kwargs):
        """
            kwargs:
                service_slug (str): slug of service to use
                rds_config (dict): config for mysql database
                redis_config (dict): config for redis cache database
                item_ids (str): name of item id lookup in mysql db
                item_codes (str): name of item code lookup in mysql db
        """
        # get rds config
        rds_config = kwargs.get('rds_config', {})
        if not isinstance(rds_config, dict):
            raise TypeError('Only dict is supported for rds_config')

        # get redis config
        redis_config = kwargs.get('redis_config', {})
        if not isinstance(redis_config, dict):
            raise TypeError('Only dict is supported for redis_config')

        # instantiate query helpers
        self.query_helper = SagemakerEngineHelpers(
            rds_config=rds_config,
            redis_config=redis_config)

        self.redis_helper = RedisHelper(**redis_config)
        # service slug is the same for all engines
        service_slug = kwargs.pop('service_slug', 'recommend')

        # get name of lookups
        self.item_id_identifier = kwargs.pop('item_id_identifier', 'item_ids')
        self.item_code_identifier = kwargs.pop('item_code_identifier', 'item_codes')

        # load service details from service table
        self.service = self.query_helper.get_service(slug=service_slug)

    def __del__(self):
        """
            Close connections on delete
        """
        del self.query_helper
        del self.redis_helper

    def get_recommendations(
        self, *,
        client_id: str,
        item_id: str, \
        engine: str,
        context: dict = {}, **kwargs):
        """
            Get the recommendations for the specified parameters

            parameters:
                - dictionary of parameter arguments
            returns:
                results (dict): Results from the Sagemaker invocation
        """
        # get client metadata from client_id
        self.client = self.get_client(client_id=client_id)
        self.engine = engine
        # recipe is set by client config
        recipe = kwargs.get('recipe', 'related_items')

        campaign = self.get_campaign(
            client_id=self.client['id'],
            engine=self.engine,
            recipe=recipe)

        if not campaign:
            raise Exception(
                            ('ServerError: Could not determine'
                            ' campaign for this client')
                        )

        # changed campaign_arn to be campaign_name
        endpoint_name = campaign['arn']

        results = self.get_results(
            item_id=item_id,
            endpoint_name=endpoint_name,
            num_results=10)

        domain = utils.dict_query(
            dictionary=context,
            path='domain')

        session_hash = utils.dict_query(
            dictionary=context,
            path='sessionHash')

        # trigger will be written with alphabetical order in mind
        trigger_log = {
                'trigger': {
                        'client': self.client['name'],
                        'type': 'recommendations',
                        'data': {
                            'domain': domain,
                            'item_id': item_id,
                            'session_hash': session_hash,
                            'results': results
                            }
                        }
                    }

        # write to lambda output logs
        print(json.dumps(trigger_log))
        return results

    def get_client(
        self, *,
        client_id: str = None,
        api_key_id: str = None) -> dict:
        """
            Determine the client with the supplied parameters
            Expects either client_id or api_key_id
            args:
                client_id (int): client id to fetch
                api_key_id (int): api_key_id to fetch client_id
            returns:
                client (dict): The determined client

        """
        # Possible double retrieve
        # this is potentially costly
        if client_id is not None:
            # do this first if client_id no None
            client = self.query_helper.get_client(client_id=client_id)
        elif api_key_id is not None:
            # do this if client_id==None
            client = self.query_helper.get_client(api_key_id=api_key_id)
        if client is None:
            raise Exception(
                    ('ClientError: Could not determine '
                    'client for this request')
                    )
        return client

    def get_campaign(
        self, *,
        client_id: str,
        engine: str,
        recipe='related_items') -> dict:
        """
            Determine the campaign with the supplied parameters
            note:
                - Currently: Campaign arn = (Sagemaker Engpoint Name)

            args:
                client_id (int): client id
                engine (str): engine slug
                recipe (str): recipe name

            returns:
                results (dict): Campaign from the database

        """
        campaign = self.query_helper.get_campaign(
            client_id=client_id,
            engine=engine,
            recipe=recipe)

        return campaign

    def encode_item_code(
        self, *,
        item_ids: list,
        from_cache: bool = True):
        """
            Lookup a list of item codes

            args:
                 item_ids (list) : list of item id's
                 from_cache (bool) : Get lookup from cache first
            return:
                item_codes (list) : list of item codes
        """

        item_codes = []

        cache_key = self.query_helper.build_cache_key(
            service=self.service['name'],
            obj_group=self.item_code_identifier,
            prefix=[self.engine, self.client['name']])

        if from_cache:
            # encode item_id -> item_code
            item_codes = self.redis_helper.redis_hmget(
                hashkey=cache_key,
                keys=item_ids)

        for i, item_code in enumerate(item_codes):
            # decode item_ids bytes -> str
            if isinstance(item_code, bytes):
                item_code = item_code.decode("utf-8")

            # check if item_id is none
            if item_code is None:
                # get item_id from database if none
                key = item_ids[i]
                item_code = self.query_helper.get_item_from_lookup(
                    client_id=self.client['id'],
                    engine=self.engine,
                    label=self.item_code_identifier,
                    key=key)

                if item_code is not None:
                    # store in cache
                    self.redis_helper.redis_hmset(hashkey=cache_key, dict_obj={key:item_code})

            item_codes[i] = item_code
        return item_codes

    def decode_item_code(
        self, *,
        item_codes: list,
        from_cache: bool = True):
        """"
            Lookup a list of item codes

            args:
                 item_codes (list) : list of item codes
                 from_cache (bool) : Get lookup from cache first
            return:
                item_ids (list) : list of item id
        """
        item_ids = []

        cache_key = self.query_helper.build_cache_key(
            service=self.service['name'],
            obj_group=self.item_id_identifier,
            prefix=[self.engine, self.client['name']])

        if from_cache:
            # decode item_codes -> item_ids
            item_ids = self.redis_helper.redis_hmget(
                hashkey=cache_key,
                keys=item_codes)
            
        for i, item_id in enumerate(item_ids):
            if isinstance(item_id, bytes):
                # decode item_ids bytes -> str
                item_id = item_id.decode("utf-8")

            # check if item_id is none
            if item_id is None:
                # get item_id from database if none
                key = item_codes[i]
                item_id = self.query_helper.get_item_from_lookup(
                    client_id=self.client['id'],
                    engine=self.engine,
                    label=self.item_id_identifier,
                    key=key)

                if item_id is not None:
                    # store in cache
                    self.redis_helper.redis_hmset(hashkey=cache_key, dict_obj={key:item_id})

            item_ids[i] = item_id

        return item_ids

    def get_results(
        self, *,
        item_id: str,
        endpoint_name: str,
        num_results: int = 10) -> list:
        """
            Determine the results for this request

            args:
                item_id (str): The client requesting the recommendation
                endpoint_name (str): The AWS Sagemaker endpoint_name
                num_results (int) : Number of recommendation results to return

            returns:
                results (list): Sagemaker invocation results

        """
        # lookup item code
        item_code = self.encode_item_code(item_ids=[item_id])
        # test that item_code is valid
        if (item_code == list()) | (item_code[0] is None):
            raise Exception('ClientError: item_id was not found')

        try:
            sagemaker_runtime = boto3.client('sagemaker-runtime')
            # make the recommender ignore self recommendation
            event = {
                'item_code':int(item_code[0]),
                'args':{
                    'n_similar':num_results,
                    'exclude':[int(item_code[0])]}}
            payload = json.dumps(event)

            # get recommendations
            response = sagemaker_runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=payload)

            # decode application/json response
            response_decoded = json.loads(response['Body'].read().decode())

            #extract itemcodes
            recommendations = [r['item_code'] for r in response_decoded]

        except sagemaker_runtime.exceptions.ModelError:
            # insure model errors are returned as 500
            msg = "ServerError: 500 Internal Server Error"
            raise Exception(msg)

        # decode recommendations bytes -> str
        results = self.decode_item_code(item_codes=recommendations)
        # check list of item_ids are not all None
        if all(item_id is None for item_id in results):
            raise Exception(
                            ('ClientError: Unable to decode'
                            ' recommendations to item_id')
                        )

        return results
