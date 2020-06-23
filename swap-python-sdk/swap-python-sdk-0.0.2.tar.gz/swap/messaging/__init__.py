from swap.messaging.clients import MessagePublisherClient
from swap.messaging.messages.builders import (
    ExecutionFailureBuilder,
    ExecutionRequestAcceptBuilder,
    ExecutionStatusUpdateBuilder,
    ExecutionCompletionBuilder
)


class PubSubMessage:
    def __init__(self, config):
        self.message = ''
        self.client = MessagePublisherClient(config=config)

    def publish(self):
        self.client.publish(message=self.message.encode(), message_type=self.message_type)


class ExecutionFailureMessage(PubSubMessage):
    def __init__(
        self, message_id, config, offer_execution_request, execution_details={}, exec_fail_code='',
        exec_fail_text=''
    ):
        super().__init__(config=config)

        self.message_id = message_id
        self.message_type = 'ExecutionFailure'
        self.config = config
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_fail_code = exec_fail_code
        self.exec_fail_text = exec_fail_text

        self.message = self._build()

    def _build(self):
        builder = ExecutionFailureBuilder(
            message_id=self.message_id,
            offer_execution_request=self.offer_execution_request,
            execution_details=self.execution_details,
            exec_fail_code=self.exec_fail_code,
            exec_fail_text=self.exec_fail_text
        )

        return builder.build()


class ExecutionRequestAcceptMessage(PubSubMessage):
    def __init__(self, message_id, config, offer_execution_request, execution_details={}):
        super().__init__(config=config)

        self.message_id = message_id
        self.message_type = 'ExecutionRequestAccept'
        self.config = config
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details

        self.message = self._build()

    def _build(self):
        builder = ExecutionRequestAcceptBuilder(
            message_id=self.message_id,
            offer_execution_request=self.offer_execution_request,
            execution_details=self.execution_details
        )

        return builder.build()


class ExecutionStatusUpdateMessage(PubSubMessage):
    def __init__(
        self, message_id, config, offer_execution_request, execution_details={},
        exec_status_code='', exec_status_text=''
    ):
        super().__init__(config=config)

        self.message_id = message_id
        self.message_type = 'ExecutionStatusUpdate'
        self.config = config
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_status_code = exec_status_code
        self.exec_status_text = exec_status_text

        self.message = self._build()

    def _build(self):
        builder = ExecutionStatusUpdateBuilder(
            message_id=self.message_id,
            offer_execution_request=self.offer_execution_request,
            execution_details=self.execution_details,
            exec_status_code=self.exec_status_code,
            exec_status_text=self.exec_status_text
        )

        return builder.build()


class ExecutionCompletionMessage(PubSubMessage):
    def __init__(
        self, message_id, config, offer_execution_request, execution_details={},
        exec_comp_code='', exec_comp_text=''
    ):
        super().__init__(config=config)

        self.message_id = message_id
        self.message_type = 'ExecutionCompletion'
        self.config = config
        self.offer_execution_request = offer_execution_request
        self.execution_details = execution_details
        self.exec_comp_code = exec_comp_code
        self.exec_comp_text = exec_comp_text

        self.message = self._build()

    def _build(self):
        builder = ExecutionCompletionBuilder(
            message_id=self.message_id,
            offer_execution_request=self.offer_execution_request,
            execution_details=self.execution_details,
            exec_comp_code=self.exec_comp_code,
            exec_comp_text=self.exec_comp_text
        )

        return builder.build()
