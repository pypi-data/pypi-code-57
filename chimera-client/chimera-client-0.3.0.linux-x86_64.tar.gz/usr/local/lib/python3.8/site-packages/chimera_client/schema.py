"""
Module to get schemas from `Chimera's` registry.
"""
import requests
from chimera_client.environ import Environment


class Schema:
    """
    Class to get schemas from `Chimera`'s registry.
    """

    def getSchema(self, channel: str) -> str:
        """
        Gets the schema from a given channel.
        """
        env = Environment()
        r = requests.get(env.chimeraRegistryUrl + '/schema/' +
                         env.chimeraNamespace + '/' + channel)
        if r.status_code != 200:
            raise Exception('[GET SCHEMA] Unable to retrieve schema.')

        # Convert body from byte to string
        return r.content.decode('utf-8')
