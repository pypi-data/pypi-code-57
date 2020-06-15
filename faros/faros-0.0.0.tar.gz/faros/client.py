"""Faros API client"""

import json
from graphqlclient import GraphQLClient
from faros.exceptions import FarosGraphQLException

DEFAULT_API_URL = "https://api.faros.ai/v1"


class FarosClient:
    """Base client for Faros API"""

    def __init__(self, token, api_url=None):
        """
        Initializes the Faros Client. Using this directly is not encouraged.
        Users should generally use the class methods to initialize the client.

        :param str token: Faros token to authenticate with into the api
        :param str api_url: Faros service url to run api calls on

        :returns: Faros Client
        :rtype: FarosClient
        """

        self._api_url = api_url if api_url else DEFAULT_API_URL
        self._graphql_client = GraphQLClient(f"{self._api_url}/graphql")
        self._graphql_client.inject_token(f"Bearer {token}")

    @classmethod
    def from_event(cls, event, api_url=None):
        """
        Factory method to instantiate Faros Client from event object passed
        to the app handler

        :param dict event: object with properties
        :param str api_url: Faros service api url to query against

        :returns: instance of the Faros client
        :rtype: FarosClient
        """
        return cls(event["farosToken"], api_url)

    def graphql_query(self, query):
        """
        Queries the Faros GraphQL api

        :param query: GraphQL query
        :return: the GraphQL results
        :rtype: json
        """

        response = json.loads(self._graphql_client.execute(query))
        if response.get("errors"):
            raise FarosGraphQLException(json.dumps(response["errors"]))
        return response["data"]
