"""a set of utilities to run custom python integrations/scripts on the Board Cloud platform
This is an example package and should not be used to build production grade integrations"""

from datetime import datetime
import json
import logging
import requests

IDENTITY_PATH = "/identity/connect/token"
QUERY_PATH = "/public/"

logging.getLogger(__name__).addHandler(logging.NullHandler())

class Client():  # pylint: disable=too-few-public-methods
    """simple client to run queries and processes using the Board APIs.
    See related documentation when creating External Queries in a Board Datamodel"""

    client_id = ""
    client_secret = ""
    token = ""
    endpoint = ""

    def __init__(self, endpoint, client_id, client_secret):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.__get_token()

    def __get_token(self):
        try:
            start_time = datetime.now()
            auth_url = self.endpoint + IDENTITY_PATH
            result = requests.post(
                auth_url,
                data={
                    'grant_type': 'client_credentials',
                    'scope': 'board-api',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                }
            )
            self.token = json.loads(result.text)['access_token']
            elapsed = datetime.now()-start_time
            logging.info(
                "Board API\tHost: %s\tClient ID: %s\tStatus: Authenticated\tElapsed: %s",
                self.endpoint, self.client_id, elapsed
                )
            logging.debug(
                "Board API\tHost: %s\tClient ID: %s\tStatus: Authenticated\tElapsed: %s",
                self.endpoint, self.client_id, elapsed
                )
        except Exception as error:
            logging.error(
                "Board API\tHost: %s\tClient ID: %s\tStatus: Error\tMessage: %s",
                self.endpoint, self.client_id, str(error)
            )
            raise

    def __api_call(self,query):   
        """Return list of entities for specified datamodel"""
        try:
            start_time = datetime.now()
            result = requests.get(
                self.endpoint + query,
                headers={
                    "Authorization":"Bearer " + self.token
                }
            )
            elapsed = datetime.now()-start_time
            logging.info(
                "Board API\tHost: %s\tQuery: %s\tStatus: Executed\tElapsed: %s",
                self.endpoint, query, elapsed
            )
            return json.loads(result.text)
        except Exception as error:
            logging.error(
                "Board API\tHost: %s\tQuery: %s\tStatus: Error\tMessage: %s",
                self.endpoint, query, str(error)
            )
            raise
        pass

    def query(self, datamodel, query_name, query_string):
        """Execute a datamodel external query and returns
        a python dictionary with the data from Board"""
        query = QUERY_PATH + "/" + datamodel + "/query/" + query_name + query_string
        return self.__api_call(query)
    
    def cubes(self, datamodel):
        """Return list of cubes for specified datamodel"""
        query = QUERY_PATH + "/" + datamodel + "/schema/Cubes"
        return self.__api_call(query)

    def entities(self,datamodel):
        """Return list of entities for specified datamodel"""
        query = QUERY_PATH + "/" + datamodel + "/schema/Entities"
        return self.__api_call(query)
    
    def entity(self,datamodel,entity):
        """Return list of entities for specified datamodel"""
        query = QUERY_PATH + "/" + datamodel + "/schema/Entities/" + entity
        return self.__api_call(query)
