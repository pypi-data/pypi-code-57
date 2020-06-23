import boto3
from botocore.config import Config as BotoClientConfig

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import json

from servicemapper.service_connector import ServiceConnector
from servicemapper.logging_client import LoggingClient
from servicemapper.types import Constants


class Core(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    logger = providers.Singleton(LoggingClient, config=config.logging)


# Boto3 Clients have automatic retry with exponential-holdoff
boto_client_config = BotoClientConfig(
    retries = dict(
        max_attempts = Constants.BOTO3_CLIENT_RETRIES
    )
)

# The Service Mappers must add a service_connector to the Mapper
Mapper = containers.DynamicContainer()
Mapper.service_connector = providers.Factory(ServiceConnector, config=Core.config.service_connector)
Mapper.sqs_client = providers.Singleton(
        boto3.client, 'sqs',
        config=boto_client_config,
        aws_access_key_id=Core.config.aws.access_key_id,
        aws_secret_access_key=Core.config.aws.secret_access_key,
        region_name=Core.config.aws.region_name
    )
Mapper.dynamodb_client = providers.Singleton(
        boto3.client, 'dynamodb',
        config=boto_client_config,
        aws_access_key_id=Core.config.aws.access_key_id,
        aws_secret_access_key=Core.config.aws.secret_access_key,
        region_name=Core.config.aws.region_name
    )