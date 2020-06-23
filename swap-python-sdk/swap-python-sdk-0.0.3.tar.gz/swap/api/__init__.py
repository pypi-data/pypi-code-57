from swap.api.clients import UBLClient
from swap.api.models import WorkflowServiceChain, CommandInput
from swap.api.sequences.builders import DefaultCommandSequenceBuilder


class Workflow:
    def __init__(self):
        self.service_chain_uuid = None
        self.service_chains = {}
        self.ubl_client = UBLClient()
        self.command_sequence = DefaultCommandSequenceBuilder().build()

    def create_service_chain(self, name):
        self.service_chains[name] = WorkflowServiceChain(datasets=[], services=[])

    def submit(self):
        output = {}

        for key, service_chain in self.service_chains.items():
            command_input = CommandInput(response=None, service_chain=service_chain)
            output[key] = self.command_sequence.call(command_input)

        return output

    def service_chain(self, name):
        return self.service_chains[name]
