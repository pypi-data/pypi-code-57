import json
import sys
from jsonschema import ValidationError
from swap.common.logging import logger
from swap.common.schemas import ServiceDiscoveryResponseSchema, ServiceDiscoverySchema
from swap.common.validators import ServiceDiscoveryResponseValidator, ServiceDiscoveryValidator
from swap.messaging.models import Message
from swap.messaging.schemas import (
    ExecutionCompletionSchema,
    ExecutionFailureSchema,
    ExecutionRequestAcceptSchema,
    ExecutionRequestCancelSchema,
    ExecutionRequestDeclineSchema,
    ExecutionRequestSchema,
    ExecutionStatusUpdateSchema,
    OfferExecutionRequestSchema,
    ServiceOfferingSchema,
    ServiceRequestSchema
)
from swap.common.validators import (
    ExecutionCompletionValidator,
    ExecutionFailureValidator,
    ExecutionRequestAcceptValidator,
    ExecutionRequestCancelValidator,
    ExecutionRequestDeclineValidator,
    ExecutionRequestValidator,
    ExecutionStatusUpdateValidator,
    OfferExecutionRequestValidator,
    ServiceOfferingValidator,
    ServiceRequestValidator
)


class MessageParser:
    def _find_schema(self, message_type):
        mapping = {
            'ExecutionCompletion': ExecutionCompletionSchema(),
            'ExecutionFailure': ExecutionFailureSchema(),
            'ExecutionRequest': ExecutionRequestSchema(),
            'ExecutionRequestAccept': ExecutionRequestAcceptSchema(),
            'ExecutionRequestCancel': ExecutionRequestCancelSchema(),
            'ExecutionRequestDecline': ExecutionRequestDeclineSchema(),
            'ExecutionStatusUpdate': ExecutionStatusUpdateSchema(),
            'OfferExecutionRequest': OfferExecutionRequestSchema(),
            'ServiceDiscovery': ServiceDiscoverySchema(),
            'ServiceDiscoveryResponse': ServiceDiscoveryResponseSchema(),
            'ServiceOffering': ServiceOfferingSchema(),
            'ServiceRequest': ServiceRequestSchema()
        }

        return mapping.get(message_type)

    def _find_validator(self, message_type):
        mapping = {
            'ServiceDiscoveryResponse': ServiceDiscoveryResponseValidator(),
            'ExecutionCompletion': ExecutionCompletionValidator(),
            'ExecutionFailure': ExecutionFailureValidator(),
            'ExecutionRequest': ExecutionRequestValidator(),
            'ExecutionRequestAccept': ExecutionRequestAcceptValidator(),
            'ExecutionRequestCancel': ExecutionRequestCancelValidator(),
            'ExecutionRequestDecline': ExecutionRequestDeclineValidator(),
            'ExecutionStatusUpdate': ExecutionStatusUpdateValidator(),
            'OfferExecutionRequest': OfferExecutionRequestValidator(),
            'ServiceDiscovery': ServiceDiscoveryValidator(),
            'ServiceOffering': ServiceOfferingValidator(),
            'ServiceRequest': ServiceRequestValidator()
        }

        return mapping.get(message_type)

    def _validate(self, message_type, message_dict):
        validator = self._find_validator(message_type=message_type)
        validator.validate(instance=message_dict)

    def _deserialise(self, message_type, message_raw):
        message_dict = json.loads(message_raw)

        try:
            self._validate(message_type=message_type, message_dict=message_dict)
        except ValidationError as e:
            logger.info(f'Received invalid {message_type} message')
            logger.info(e)

        schema = self._find_schema(message_type=message_type)

        return schema.load(message_dict)

    def parse(self, message):
        message_raw = message.data.decode('utf-8', 'ignore')
        message_type = message.attributes.get('message_type')

        message_data = None

        try:
            message_data = self._deserialise(message_type=message_type, message_raw=message_raw)
        except:
            e = sys.exc_info()
            logger.info(f'Could not deserialise {message_type}')
            logger.info(e)

        return Message(
            message_data=message_data,
            message_raw=message_raw,
            message_type=message_type
        )
