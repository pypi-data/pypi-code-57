import base64
import json
import sys
from swap.common.logging import logger
from swap.messaging.clients import MessagePublisherClient
from swap.messaging.identities import OfferExecutionRequestIdentity, ServiceRequestIdentity
from swap.messaging.messages.builders import ServiceDiscoveryResponseBuilder, ServiceOfferingBuilder
from swap.messaging.parsers import MessageParser
from swap.messaging import ExecutionFailureMessage, ExecutionRequestAcceptMessage


class Action:
    def __init__(self, config):
        self.config = config
        self.message_parser = MessageParser()
        self.client = MessagePublisherClient(config=config)

    def parse_message(self, message):
        return self.message_parser.parse(message).data


class DefaultMessageAction(Action):
    def call(self, message_type, message, callback):
        logger.debug(f'Executing default message action for {message_type} message')


class IgnoredMessageAction(Action):
    def call(self, message_type, message, callback):
        logger.debug(f'Received a {message_type} message, ignoring')

        if message_type != 'ServiceDiscoveryResponse':
            loaded = json.loads(message.data)
            logger.debug(f'Message: {json.dumps(loaded, indent=2)}')


class ServiceDiscoveryAction(Action):
    def call(self, message_type, message, callback):
        logger.debug('Received a ServiceDiscovery message')

        builder = ServiceDiscoveryResponseBuilder(config=self.config)
        message = builder.build()

        logger.debug(f'Responding with: {message}')

        self.client.publish(message=message.encode(), message_type='ServiceDiscoveryResponse')


class ServiceRequestAction(Action):
    def __init__(self, config):
        super().__init__(config=config)
        self.identity = ServiceRequestIdentity()

    def respond_to(self, message_id, service_request):
        # FIXME Use when CDF integration finalised
        # decoded = base64.b64decode(service_request.input_data.cdf_metadata)
        # print('Base64 CDF metadata:', decoded)

        logger.info('Responding to ServiceRequest')
        builder = ServiceOfferingBuilder(message_id, self.config, service_request)
        message = builder.build()

        logger.debug(f'Responding to ServiceRequest with {message}')

        self.client.publish(message=message.encode(), message_type='ServiceOffering')

    def call(self, message_type, message, callback):
        logger.info('Received a ServiceRequest message')

        loaded = json.loads(message.data)
        logger.debug(f'Message: {json.dumps(loaded, indent=2)}')

        service_request = self.parse_message(message)

        if self.identity.match(service_request, self.config):
            message_id = message.message_id
            self.respond_to(message_id=message_id, service_request=service_request)


class ExecutionRequestCancelAction(Action):
    # Ignore for now
    def call(self, message_type, message, callback):
        logger.debug('Received an ExecutionRequestCancel message. Currently unable to cancel.')


class OfferExecutionRequestAction(Action):
    def __init__(self, config):
        super().__init__(config=config)
        self.identity = OfferExecutionRequestIdentity()

    def execution_parameters(self, offer_execution_request):
        execution_parameters_string = offer_execution_request.execution_parameters

        try:
            decoded = base64.b64decode(execution_parameters_string[2:-1])
            parsed = json.loads(decoded)
            return parsed
        except:
            e = sys.exc_info()
            logger.warn(e)
            return {}

    def respond_with_acceptance(self, message_id, offer_execution_request):
        message = ExecutionRequestAcceptMessage(
            message_id=message_id,
            config=self.config,
            offer_execution_request=offer_execution_request,
            execution_details='',
        )

        message.publish()

    def respond_with_failure(self, message_id, offer_execution_request, error):
        message = ExecutionFailureMessage(
            message_id=message_id,
            config=self.config,
            offer_execution_request=offer_execution_request,
            execution_details='',
            exec_fail_code='1',
            exec_fail_text='Execution failed'
        )

        message.publish()

    def respond_to(self, message_id, offer_execution_request, callback):
        self.respond_with_acceptance(message_id, offer_execution_request)

        parameters = self.execution_parameters(offer_execution_request)

        logger.info("About to call callback")

        try:
            callback.call(
                message_id=message_id,
                offer_execution_request=offer_execution_request,
                parameters=parameters
            )
        except:
            e = sys.exc_info()
            logger.warn(f'Callback failed {e}')

            self.respond_with_failure(
                message_id=message_id,
                offer_execution_request=offer_execution_request,
                error=e
            )

    def call(self, message_type, message, callback):
        logger.info('Received an OfferExecutionRequest message')

        loaded = json.loads(message.data)
        logger.debug(f'Message: {json.dumps(loaded, indent=2)}')

        offer_execution_request = self.parse_message(message)

        if self.identity.match(offer_execution_request, self.config):
            message_id = message.message_id

            self.respond_to(
                message_id=message_id,
                offer_execution_request=offer_execution_request,
                callback=callback
            )
