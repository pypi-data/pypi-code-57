# from servicemapper.service_connector import ServiceConnector
import dependency_injector.providers as providers
import logging
from servicemapper.ioc import Core, Mapper
from servicemapper.mapper_worker import MapperWorker
from servicemapper.service_connector import ServiceConnector

# Service-Specific configuration
Core.config.override({
    'logging': {
        'name': 'sample-service-mapper',
        'level': logging.DEBUG
    },
    # Parameters specific to my ServiceConnector implementation
    'service_connector': {
        'key': 'value1'
    }
})
logger = Core.logger()

# ServiceConnector Implementation
# TODO: Template-ize this for use with the Yeoman Generator
class SampleServiceConnector(ServiceConnector):
    def __init__(self, config):
        pass

    def about(self):
        pass

    def connect(self):
        pass

Mapper.service_connector = providers.Factory(
        SampleServiceConnector,
        name="SeampleServiceConnector"
    )

worker = MapperWorker()


def handler(event, context):
    logger.info(f"event: {event}")
    logger.info(f"context: {context}")
    return

if __name__ == "__main__":
    event = {
        "source": "some event source"
    }
    context = {
        "context_key_1": "context_value_1"
    }
    handler(event=event, context=context)