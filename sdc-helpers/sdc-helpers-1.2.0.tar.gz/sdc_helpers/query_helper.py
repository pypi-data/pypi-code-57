"""
   SDC Query helper module
"""
import os
import json
import boto3
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker, undefer
from sqlalchemy.orm.attributes import flag_modified

import sdc_helpers.utils as utils
import sdc_helpers.decorators as decorators
from sdc_helpers.models.client import Client
from sdc_helpers.models.service import Service
from sdc_helpers.models.subscription import Subscription
from sdc_helpers.redis_helper import RedisHelper


class QueryHelper:
    """
        Query helper class
    """
    # pylint: disable=too-few-public-methods, singleton-comparison, no-member

    session = None
    redis_helper = None

    def __init__(self, **kwargs):
        """
            Init a new QueryHelper obj
            kwargs:
                rds_config (dict) : config arguments for mysql connector
                redis_config (dict) : config arguments for redis connector
        """
        # get rds config
        rds_config = kwargs.get('rds_config', {})
        rds_host = rds_config.get('host', None)
        rds_user = rds_config.get('username', None)
        rds_password = rds_config.get('password', None)
        rds_port = rds_config.get('port', None)
        rds_db = rds_config.get('db', None)

        # get redis config
        redis_config = kwargs.get('redis_config', {})
        redis_host = redis_config.get('host', None)
        redis_port = redis_config.get('port', None)
        redis_db = redis_config.get('db', None)
        # temporary fix - these should be passed at init time
        if rds_host is None:
            rds_host = os.getenv('RDS_HOST', 'localhost')
        # temporary fix - these should be passed at init time
        if rds_user is None:
            rds_user = os.getenv('RDS_USERNAME', 'root')
        # temporary fix - these should be passed at init time
        if rds_password is None:
            rds_password = os.getenv('RDS_PASSWORD')
        # temporary fix - these should be passed at init time
        if rds_port is None:
            rds_port = int(os.getenv('RDS_PORT', '3306'))
        # temporary fix - these should be passed at init time
        if rds_db is None:
            rds_db = os.getenv('RDS_DB_NAME', 'sdc')

        user_password = rds_user
        if rds_password is not None:
            user_password = '{user}:{password}'.format(
                user=rds_user,
                password=rds_password
            )

        engine = create_engine(
            'mysql+pymysql://{user_password}@{host}:{port}/{db}'.format(
                user_password=user_password,
                host=rds_host,
                port=rds_port,
                db=rds_db
            )
        )

        self.session = sessionmaker(bind=engine)()

        # instantiate a redis helper
        self.redis_helper = RedisHelper(host=redis_host, port=redis_port, db=redis_db)

    def __del__(self):
        self.session.close()
        del self.redis_helper

    @decorators.query_exception_handler()
    def get_clients(self) -> list:
        """
            Get all the clients from the database

        return:
            clients (list) : Returns a list of all active Client models from the database

        """
        return self.session.query(Client).filter(
            Client.deleted_at == None
        ).all()

    @decorators.query_exception_handler()
    def get_client(
            self,
            *,
            from_cache: bool = True,
            **kwargs
    ) -> Client:
        """
            Get the specified client from cache or database

            args:
                from_cache (bool): Retrieve the client from cache - Default True
                kwargs (dict):
                    api_key_id (str): The AWS API Gateway API Key Id
                    client_id (int): ID of the client in the database

            return:
                client (Client) : Returns the specified Client model

        """
        api_key_id = kwargs.get('api_key_id')
        client_id = kwargs.get('client_id')

        if not api_key_id and not client_id:
            raise Exception('ClientError: api_key_id or id is required for this function')

        if api_key_id and client_id:
            raise Exception(
                'ClientError: Only one of api_key_id or id should be specified for this function'
            )

        if api_key_id:
            client_redis_key = 'client-{api_key_id}'.format(api_key_id=api_key_id)
        else:
            client_redis_key = 'client-{client_id}'.format(client_id=client_id)

        client_redis = self.redis_helper.redis_get(key=client_redis_key)

        if (
                not from_cache or
                not client_redis
        ):
            if api_key_id:
                client = boto3.client('apigateway')
                api_key = client.get_api_key(apiKey=api_key_id)

                if 'tags' not in api_key or 'client_code' not in api_key['tags']:
                    raise Exception(
                        ('ClientError: client_code not set up for this API key. '
                         'Please contact support'
                        )
                    )

                client = self.session.query(Client).filter(
                    and_(
                        Client.code == utils.dict_query(
                            dictionary=api_key,
                            path='tags.client_code'
                        ),
                        Client.deleted_at == None
                    )
                ).first()
            else:
                client = self.session.query(Client).filter(
                    and_(
                        Client.id == client_id,
                        Client.deleted_at == None
                    )
                ).first()

            if client is not None:
                self.redis_helper.redis_set(
                    key=client_redis_key,
                    value=json.dumps(client.to_dict(), default=str)
                )
        else:
            client_dict = json.loads(client_redis)
            client_dict.update(
                {
                    'read_only': True
                }
            )
            client = Client(**client_dict)

        return client

    @decorators.query_exception_handler()
    def get_services(self) -> list:
        """
            Get all the services from the database

        return:
            services (list) : Returns a list of all active Service models from the database

        """
        return self.session.query(Service).filter(
            Service.deleted_at == None
        ).all()

    @decorators.query_exception_handler()
    def get_service(self, *, slug: str, from_cache: bool = True) -> Service:
        """
            Get the specified client from cache or database

            args:
                slug (str): slug of the service in the database
                from_cache (bool): Retrieve the service from cache - Default True

            return:
                service (Service) : Returns the specified Service model

        """
        service_redis_key = 'service-{slug}'.format(slug=slug)
        service_redis = self.redis_helper.redis_get(key=service_redis_key)

        if (
                not from_cache or
                not service_redis
        ):
            service = self.session.query(Service).filter(
                and_(
                    Service.slug == slug,
                    Service.deleted_at == None
                )
            ).first()

            if service:
                self.redis_helper.redis_set(
                    key=service_redis_key,
                    value=json.dumps(service.to_dict(), default=str)
                )
        else:
            service_dict = json.loads(service_redis)
            service_dict.update(
                {
                    'read_only': True
                }
            )
            service = Service(**service_dict)

        return service

    @decorators.query_exception_handler()
    def get_subscription(
            self,
            *,
            client_id: int,
            service_id: int,
            from_cache: bool = True
    ) -> Subscription:
        """
            Get the specified subscription from cache or database

            args:
                client_id (id): client_id of the subscription in the database
                service_id (id): service_id of the subscription in the database
                from_cache (bool): Retrieve the service from cache - Default True

            return:
                subscription (Subscription) : Returns the specified Subscription model

        """
        subscription_redis_key = (
            'subscription-{client_id}-{service_id}'.format(
                client_id=client_id,
                service_id=service_id
            )
        )
        subscription_redis = self.redis_helper.redis_get(
            key=subscription_redis_key
        )

        if (
                not from_cache or
                not subscription_redis
        ):
            subscription = self.session.query(Subscription).filter(
                and_(
                    Subscription.client_id == client_id,
                    Subscription.service_id == service_id,
                    Subscription.deleted_at == None
                )
            ).first()

            if subscription:
                self.redis_helper.redis_set(
                    key=subscription_redis_key,
                    value=json.dumps(subscription.to_dict(), default=str)
                )
        else:
            subscription_dict = json.loads(subscription_redis)
            subscription_dict.update(
                {
                    'read_only': True
                }
            )
            subscription = Subscription(**subscription_dict)

        return subscription

    @decorators.query_exception_handler()
    def get_subscriptions(self, *, service_id: int) -> list:
        """
            Get all the specified service's subscriptions from the database

            args:
                service_id (id): service_id of the subscription in the database

            return:
                subscriptions (list) : Returns the specified service's Subscription models

        """
        return self.session.query(Subscription).filter(
            and_(
                Subscription.service_id == service_id,
                Subscription.deleted_at == None
            )
        ).options(
            undefer('properties')
        ).all()

    @decorators.query_exception_handler()
    def update_subscription(self, *, subscription: Subscription):
        """
            Commit the Subscription model and flush all subscription Redis keys

            args:
                subscription (Subscription): The Subscription model to update
        """
        if subscription.read_only:
            raise Exception('ServerError: Cannot update a read only model')

        # If properties have only been partially modified,
        # e.g `subscription.properties['node1'][0][node2] = value`,
        # the properties attribute is not marked as dirty and we
        # need to mark it as such to cause an update in the database

        flag_modified(subscription, 'properties')

        self.session.commit()
