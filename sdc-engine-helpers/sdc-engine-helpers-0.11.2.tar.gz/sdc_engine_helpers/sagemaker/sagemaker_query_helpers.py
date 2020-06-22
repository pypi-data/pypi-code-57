"""
    Sagemaker Engine Helpers module used to manage
    and get information on client subscription
"""
import json
from sdc_helpers.query_helper import QueryHelper

class SagemakerEngineHelpers(QueryHelper):
    """Extension on the QueryHelper"""
    def __init__(self, **kwargs):
        # instantiate the same super
        super().__init__(**kwargs)

    @staticmethod
    def build_cache_key(*, service, obj_group, prefix: list = []):
        """
            Builds a key for use with redis cache

            args:
                service (str):
                group_name (str):
            *prefix:
                any number of non-keyword arguments given by the user

            example:
                >> cache_key = SagemakerEngineHelpers.build_cache_key(
                    'recommend', 'lookup', 'prefix1', 'prefix2', 'prefix3')
                >> print(cache_key)
                'recommend-prefix1-prefix2-prefix3-lookup'
        """
        # join prefixes
        if len(prefix) > 0:
            prefixes = "-".join(prefix)

        # build cache key
        cache_key = '{service}-{prefixes}-{obj_group}'.format(
            service=service,
            prefixes=prefixes,
            obj_group=obj_group)

        return cache_key.replace(" ", "-").lower()

    # add overriding functionality
    def get_engines(self, *, client_id: str):
        """
            get engines json, assume reuse

            note:
                - single point of failure with mysql json_extract
                - this could be made even more efficiency\
                    if datasets, campaigns each when to get it their selves
                - but potential for breakages due to string query bugs
        """
        cursor = self.db_conn.cursor()

        sql = (
            'SELECT JSON_EXTRACT(properties, "$.engines") as engines'
            ' FROM `subscriptions` '
            'WHERE `subscriptions`.`client_id` = %s'
                )

        cursor.execute(sql, (client_id, ))

        try:
            engines = cursor.fetchall()[0].get('engines')
            engines = json.loads(engines)

        except ValueError:
            raise Exception(
                        ("ClientError: No Engines found"
                        "for client_id= '{}'".format(client_id))
                    )

        return engines

    def get_engine(self, *, client_id: str, slug: str):
        """
            Get a specific engine from subscription properties
            args:
                properties (dict): Subscription properties for a client
                slug (str): The engine's slug
            returns:
                engine_dict (dict): The requested engine dictionary from the properties if found
        """
        engines = self.get_engines(client_id=client_id)
        for index, engine in enumerate(engines):
            if engine.get('slug') == slug:
                return engine, index

        raise IndexError(
                    ("ClientError: No Engine matching '{}' "
                    "found for the client = '{}'".format(slug, client_id))
                )

    def get_datasets(self, *, client_id: str, engine: str):
        """Get list of all datasets for the engine"""
        # ignore index
        engine, _ = self.get_engine(client_id=client_id, slug=engine)
        # unlikely that datasets = empty([]), but not failing condition
        return engine.get('datasets', [])

    def get_dataset(self, *, client_id: str, engine: str, label: str):
        """
            Get a specific dataset from an engine dictionary
            args:
                engine (dict): Subscription properties engine
                label (str): Label describing what the dataset is for
            returns:
                dataset_dict (dict): The requested dataset dictionary from the engine if found
        """
        datasets = self.get_datasets(client_id=client_id, engine=engine)

        if datasets is not None:
            for dataset in datasets:
                # only return the datasets if the label matches
                if dataset.get('label') == label:
                    return dataset

        raise IndexError(
                        ("ClientError: No Dataset matching '{}' "
                        "found in Engine = '{}' "
                        "for client = '{}'".format(label, engine, client_id))
                )

    def get_item_from_lookup(self, *, client_id: str, engine: str, label: str, key: str):
        """
            Get a specific dataset from an engine dictionary
            args:
                engine (dict): Subscription properties engine
                label (str): Label describing what the dataset is for
            returns:
                dataset_dict (dict): The requested dataset dictionary from the engine if found
        """
        dataset = self.get_dataset(client_id=client_id, engine=engine, label=label)

        return dataset.get("data", {}).get(str(key))

    def get_campaigns(self, *, client_id: str, engine: str):
        """Get list of all datasets for the engine"""
        # ignore index
        engine, _ = self.get_engine(client_id=client_id, slug=engine)
        # unlikely that datasets = empty([]), but not failing condition
        return engine.get('campaigns', [])

    def get_campaign(self, client_id: str, engine: str, recipe: str):
        """
            Get a specific campaign from an engine dictionary
            args:
                engine (dict): Subscription properties engine
                recipe (str): The recipe of the campaign e.g related_items
                event_type (str): Supplied if the campaign only involves certain events e.g
                                only listing views, but not listing enquiries
            returns:
                campaign_dict (dict): The requested campaign dictionary from the engine if found
        """

        # get campaigns
        campaigns = self.get_campaigns(client_id=client_id, engine=engine)
        # get campaign dict
        if campaigns is not None:
            for campaign in campaigns:
                # only return the campaign if the recipe matches
                if campaign.get('recipe') == recipe:
                    return campaign

        raise IndexError(
                    ("ClientError: No Campaign matching '{}' "
                    "found for Engine = '{}' "
                    "And client = '{}' ".format(recipe, engine, client_id))
                )
