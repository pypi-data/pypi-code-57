"""
    Sagemaker Engine Helpers module used to manage
    and get information on client subscription
"""
import json
from sdc_engine_helpers.engine_query_helper import EngineQueryHelper


class SagemakerEngineHelpers(EngineQueryHelper):
    """Extension on the EngineQueryHelper"""

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

    def get_dataset(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            **kwargs
    ):
        dataset = super().get_dataset(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            **kwargs
        )

        if not dataset:
            raise IndexError(
                (
                    "ClientError: No Dataset matching {} "
                    "found in Engine = '{}' "
                    "for client = '{}'".format(json.dumps(kwargs), engine_slug, client_id)
                )
            )

        return dataset


    def get_item_from_lookup(
            self,
            *,
            client_id: int,
            service_id: int,
            engine: str,
            from_cache: bool = True,
            label: str,
            key: str
    ):
        """
            Get a specific item from lookup

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine (str): Subscription property engine
                from_cache (bool): Retrieve the datasets from cache - Default True
                label (str): Label describing what the dataset is for
                key (str): Dataset ket to lookup

            returns:
                result (dict): The result of the lookup
        """
        dataset_kwargs = {'label': label}

        dataset = self.get_dataset(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine,
            from_cache=from_cache,
            **dataset_kwargs
        )

        return dataset.get("data", {}).get(str(key))

    def get_campaign(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            **kwargs
    ):
        campaign = super().get_campaign(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            from_cache=from_cache,
            **kwargs
        )

        if not campaign:
            raise IndexError(
                (
                    "ClientError: No Campaign matching {} "
                    "found for Engine = '{}' "
                    "And client = '{}' ".format(json.dumps(kwargs), engine_slug, client_id)
                )
            )

        return campaign
