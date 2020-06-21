"""
Module that gets all envorinment variables from the context as to allow chimera communication.
"""
import os

class Environment:
    """
    A class that gets all necessary variables from the context for chimera commuication.
    """

    def __init__(self):
        try:
            self.chimeraNodeID: str = os.environ['CHIMERA_NODE_ID']
            self.chimeraNamespace: str = os.environ['CHIMERA_NAMESPACE']
            self.chimeraRegistryUrl: str = os.environ['CHIMERA_REGISTRY_URL']
            self.outputChannels: str = os.environ['CHIMERA_OUTPUT_CHANNELS']
            self.inputChannels: str = os.environ['CHIMERA_INPUT_CHANNELS']

            self.bootstrapServers: str = os.environ['KAFKA_BOOTSTRAP_SERVERS']
        except KeyError:
            raise EnvironmentError('Check the environment vars.')
