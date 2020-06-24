from swap.messaging.actions import (
    DefaultMessageAction,
    ExecutionRequestCancelAction,
    IgnoredMessageAction,
    OfferExecutionRequestAction,
    ServiceDiscoveryAction,
    ServiceRequestAction,
)
from swap.messaging.callbacks import DefaultCallback
from swap.messaging.exceptions import InvalidActionException


class Registry:
    def __init__(self, config):
        self.config = config
        self.actions = {}
        self.callbacks = {}

    def _validate(self, action):
        call_method = getattr(action, 'call', None)

        if not call_method:
            raise InvalidActionException('Action missing call attribute')

        if not callable(call_method):
            raise InvalidActionException('Action call attribute not callable')

    def register_action(self, message_type, action):
        self._validate(action)
        self.actions[message_type] = action

    def register_callback(self, message_type, callback):
        self.callbacks[message_type] = callback

    def action(self, message_type):
        return self.actions.get(message_type, DefaultMessageAction(config=self.config))

    def callback(self, message_type):
        return self.callbacks.get(message_type, DefaultCallback)


class DefaultRegistry(Registry):
    def __init__(self, config):
        self.config = config

        self.actions = {
            'ServiceDiscovery': ServiceDiscoveryAction(config=config),
            'ServiceDiscoveryResponse': IgnoredMessageAction(config=config),
            'ServiceRequest': ServiceRequestAction(config=config),
            'ServiceOffering': IgnoredMessageAction(config=config),
            'ExecutionRequest': IgnoredMessageAction(config=config),
            'ExecutionRequestCancel': ExecutionRequestCancelAction(config=config),
            'ExecutionRequestAccept': IgnoredMessageAction(config=config),
            'ExecutionRequestDecline': IgnoredMessageAction(config=config),
            'ExecutionStatusUpdate': IgnoredMessageAction(config=config),
            'ExecutionCompletion': IgnoredMessageAction(config=config),
            'ExecutionFailure': IgnoredMessageAction(config=config),
            'OfferExecutionRequest': OfferExecutionRequestAction(config=config),
        }

        self.callbacks = {}
