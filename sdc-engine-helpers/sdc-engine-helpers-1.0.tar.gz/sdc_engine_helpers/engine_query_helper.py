"""
    Global engine query helper module
"""
import json
from sdc_helpers import decorators
from sdc_helpers.query_helper import QueryHelper
from sqlalchemy import and_
from sqlalchemy.orm import with_expression
from sdc_engine_helpers.models.subscription import Subscription


class EngineQueryHelper(QueryHelper):
    """
        Reusable generic engine query helper
    """
    # pylint: disable=singleton-comparison

    @decorators.query_exception_handler()
    def get_engine_entity(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            entity_key: str,
            from_cache: bool = True
    ):
        """
            Get a specific entity from a specific engine in a subscription

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine_slug (str): Subscription property engine
                entity_key (str): The key of the entity in the engine
                from_cache (bool): Retrieve the entities from cache - Default True

            returns:
                entity_list (list): A list of the requested entity in the specified engine
                engine_index (int): Index of the engine index in properties (None if from cache)
        """
        entities_redis_key = (
            'subscription-{client_id}-{service_id}-{entity_key}-{engine_slug}'.format(
                client_id=client_id,
                service_id=service_id,
                entity_key=entity_key,
                engine_slug=engine_slug
            )
        )
        entities_redis = self.redis_helper.redis_get(key=entities_redis_key)
        engine_index = None

        if (
                not from_cache or
                not entities_redis
        ):
            subscription = self.session.query(Subscription).filter(
                and_(
                    Subscription.client_id == client_id,
                    Subscription.service_id == service_id,
                    Subscription.deleted_at == None
                )
            ).options(
                with_expression(
                    Subscription.engine_index,
                    Subscription.engine_index_expression(
                        engine_slug=engine_slug
                    )
                ),
                with_expression(
                    Subscription.engine_node,
                    Subscription.engine_node_expression(
                        engine_slug=engine_slug,
                        entity_key=entity_key
                    )
                )
            ).first()

            entities = None
            if subscription is not None:
                entities = subscription.engine_node

                if entities:
                    engine_index = int(subscription.engine_index)
                    entities = json.loads(entities)

            self.redis_helper.redis_set(
                key=entities_redis_key,
                value=json.dumps(entities, default=str)
            )
        else:
            entities = json.loads(entities_redis)

        return entities, engine_index

    def get_dataset(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Get a specific dataset for an engine in subscription properties

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine_slug (str): Subscription property engine
                from_cache (bool): Retrieve the datasets from cache - Default True
                kwargs (dict):
                    label (str): The dataset's label

            returns:
                dataset_dict (dict): The requested campaign dictionary, if found
        """
        label = kwargs.get('label', None)

        datasets, _ = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='datasets',
            from_cache=from_cache
        )

        if datasets is not None:
            for dataset in datasets:
                if dataset.get('label') == label:
                    return dataset

        return None

    def get_campaign(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Get a specific campaign for an engine in subscription properties

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine_slug (str): Subscription property engine
                from_cache (bool): Retrieve the campaigns from cache - Default True
                kwargs (dict):
                    arn (str): The campaign's arn
                    recipe (str): The recipe of the campaign e.g related_items
                    event_type (str): Supplied if the campaign only involves certain events e.g
                                      only listing views, but not listing enquiries

            returns:
                campaign_dict (dict): The requested campaign,  if found
        """
        campaigns, _ = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='campaigns',
            from_cache=from_cache
        )

        if campaigns is not None:
            return self.match_arn_or_recipe_event_type(entities=campaigns, **kwargs)

        return None

    def get_solution(
            self,
            *,
            client_id: int,
            service_id: int,
            engine_slug: str,
            from_cache: bool = True,
            **kwargs
    ):
        """
            Get a specific solution for an engine in subscription properties

            args:
                client_id (int): The client id of the subscription
                service_id (int): The service id of the subscription
                engine_slug (str): Subscription property engine
                from_cache (bool): Retrieve the solutions from cache - Default True
                kwargs (dict):
                    arn (str): The campaign's arn
                    recipe (str): The recipe of the solution e.g related_items
                    event_type (str): Supplied if the solution only involves certain events e.g
                                      only listing views, but not listing enquiries

            returns:
                solution_dict (dict): The requested solution dictionary, if found
        """
        solutions, _ = self.get_engine_entity(
            client_id=client_id,
            service_id=service_id,
            engine_slug=engine_slug,
            entity_key='solutions',
            from_cache=from_cache
        )

        if solutions is not None:
            return self.match_arn_or_recipe_event_type(entities=solutions, **kwargs)

        return None

    @staticmethod
    def match_arn_or_recipe_event_type(*, entities: list, **kwargs):
        """
            Match a entity on arn or recipe/event_type

            args:
                entities (list): List of entities being searched
                kwargs (dict):
                    arn (str): The entity's arn
                    recipe (str): The recipe of the entity e.g related_items
                    event_type (str): Supplied if the entity only involves certain events e.g
                                      only listing views, but not listing enquiries

            returns:
                entity_dict (dict/None): The requested entity dictionary, if found
        """
        arn = kwargs.get('arn', None)
        recipe = kwargs.get('recipe', None)
        event_type = kwargs.get('event_type', None)

        for entity in entities:
            if (
                    (
                        arn is not None and entity.get('arn') == arn
                    ) or
                    (
                        entity.get('recipe') == recipe and
                        (event_type is None or entity.get('event_type') == event_type)
                    )
            ):
                return entity

        return None

    @staticmethod
    def update_engine_entity(
            *,
            subscription: Subscription,
            engine_index: int,
            entity_key: str,
            value
    ):
        """
            Update a specific entity in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                entity_key (str): The key of the entity in the engine
                value: The data to set the entity key node to
        """
        subscription.properties['engines'][engine_index][entity_key] = value

    def update_datasets(
            self,
            *,
            subscription: Subscription,
            engine_index: int,
            value
    ):
        """
            Update datasets in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value: The data to set the entity key node to
        """
        self.update_engine_entity(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='datasets',
            value=value
        )

    def update_campaigns(
            self,
            *,
            subscription: Subscription,
            engine_index: int,
            value
    ):
        """
            Update campaigns in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value: The data to set the entity key node to
        """
        self.update_engine_entity(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='campaigns',
            value=value
        )

    def update_solutions(
            self,
            *,
            subscription: Subscription,
            engine_index: int,
            value
    ):
        """
            Update solutions in a specific engine in a subscription

            args:
                subscription (Subscription): The subscription model to update
                engine_index (str): The engine index in the Subscription model properties
                value: The data to set the entity key node to
        """
        self.update_engine_entity(
            subscription=subscription,
            engine_index=engine_index,
            entity_key='solutions',
            value=value
        )

    def flush_subscription_properties_cache(self, subscription: Subscription):
        """
            Match a entity on arn or recipe/event_type

            args:
                subscription (Subscription): The subscription object to flush cache for
        """
        subscription_redis_key_pattern = (
            'subscription-{client_id}-{service_id}*'.format(
                client_id=subscription.client_id,
                service_id=subscription.service_id
            )
        )
        keys = self.redis_helper.redis_keys(
            pattern=subscription_redis_key_pattern
        )

        if len(keys) > 0:
            self.redis_helper.redis_delete(keys=keys)
