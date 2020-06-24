import abc
import dependency_injector.providers as providers
import logging

from servicemapper.ioc import Core, Mapper
from servicemapper.service_connector import ServiceConnector

class ExampleServiceConnector(ServiceConnector):
    def __init__(self, name):
        assert name
        self.name = name
 
    def about(self):
        print(f"ExampleServiceConnector.about: name={self.name}")

    def connect(self):
        raise NotImplementedError()

def initialize_containers():
    Core.config.override(
        {
            'database': {
                'dsn': ':memory:'
            },
            'aws': {
                'access_key_id': 'KEY',
                'secret_access_key': 'SECRET',
                'region_name': 'REGION_NAME'
            },
            'auth': {
                'token_ttl': 3600
            },
            'logging': {
                'name': 'example-service-mapper',
                'level': logging.DEBUG
            }
        }
    )
    # Override the Service Connector for this service
    Mapper.service_connector = providers.Factory(
        ExampleServiceConnector,
        name="Example Service Name"
    )

if __name__ == "__main__":
    # Initialize the containers
    initialize_containers()

    # Get the Core logger
    logger = Core.logger()
    logger.debug('This is a DEBUG message')
    logger.info('This is an INFO message')
    logger.error('This is an ERROR message')
    logger.fatal('This is a FATAL message')

    # Get and use the Service Connector
    service_connector = Mapper.service_connector()
    service_connector.about()
