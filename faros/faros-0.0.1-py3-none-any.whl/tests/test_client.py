import json
import unittest
from faros.client import FarosClient
from faros.exceptions import FarosGraphQLException
from graphqlclient import GraphQLClient
from unittest.mock import patch


class FarosClientTest(unittest.TestCase):
    def test_successful_query(self):
        response = {
            "data": {
                "entityThatExists": {
                    "data": []
                }
            }
        }
        event = {"farosToken": "token"}
        query = """{
                  entityThatExists {
                    data {
                      farosParam1
                      farosParam2
                    }
                  }
                }"""

        with patch.object(
                GraphQLClient, "execute", return_value=json.dumps(response)):
            faros_client = FarosClient.from_event(event)
            self.assertEqual(
                faros_client.graphql_query(query), response["data"])

    def test_query_throws_exception(self):
        response = {
            "data": None,
            "errors": [{"message": "some error."}]
        }
        event = {"farosToken": "token"}
        query = """{
                  entityThatDoesNotExist {
                    data {
                      farosParam1
                      farosParam2
                    }
                  }
                }"""

        faros_client = FarosClient.from_event(event)
        with patch.object(
                GraphQLClient, "execute", return_value=json.dumps(response)):
            with self.assertRaises(FarosGraphQLException) as ex:
                faros_client.graphql_query(query)

            self.assertEqual(json.loads(str(ex.exception)), response["errors"])


if __name__ == '__main__':
    unittest.main()
