from swap.api.commands import (
    ProgressRequestCommand,
    ServiceExecutionRequestCommand,
    ServiceOffersRequestCommand,
    ServiceRequestCommand,
)
from swap.api.hooks import (
    ProgressRequestPostHook,
    ProgressRequestPreHook,
    ServiceExecutionRequestPostHook,
    ServiceExecutionRequestPreHook,
    ServiceOffersRequestPostHook,
    ServiceOffersRequestPreHook,
    ServiceRequestPostHook,
    ServiceRequestPreHook,
)
from swap.api.sequences import CommandSequence
from swap.api.steps import CommandStep


class DefaultCommandSequenceBuilder:
    def __init__(self):
        self.command_sequence = CommandSequence()

    def service_request_step(self):
        return CommandStep(
            command=ServiceRequestCommand(),
            pre_hook=ServiceRequestPreHook(),
            post_hook=ServiceRequestPostHook()
        )

    def service_offers_request_step(self):
        return CommandStep(
            command=ServiceOffersRequestCommand(),
            pre_hook=ServiceOffersRequestPreHook(),
            post_hook=ServiceOffersRequestPostHook()
        )

    def service_execution_request_step(self):
        return CommandStep(
            command=ServiceExecutionRequestCommand(),
            pre_hook=ServiceExecutionRequestPreHook(),
            post_hook=ServiceExecutionRequestPostHook()
        )

    def progress_request_step(self):
        return CommandStep(
            command=ProgressRequestCommand(),
            pre_hook=ProgressRequestPreHook(),
            post_hook=ProgressRequestPostHook()
        )

    def build(self):
        self.command_sequence.add_step(
            'ServiceRequest', self.service_request_step()
        )

        self.command_sequence.add_step(
            'ServiceOffersRequest', self.service_offers_request_step()
        )

        self.command_sequence.add_step(
            'ServiceExecutionRequest', self.service_execution_request_step()
        )

        self.command_sequence.add_step(
            'ProgressRequest', self.progress_request_step()
        )

        return self.command_sequence
