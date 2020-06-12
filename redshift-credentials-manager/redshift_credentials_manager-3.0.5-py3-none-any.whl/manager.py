from datetime import datetime, timezone
from typing import List, Tuple

import boto3


class RedshiftCredentialsManager(object):
    def __init__(self,
                 connector,
                 cluster_id: str,
                 user: str,
                 database_name: str,
                 groups: List[str] = None,
                 duration: int = 3600,
                 region: str = 'us-east-1'):
        self.connector = connector
        self.cluster_id = cluster_id
        self.user = user
        self.database_name = database_name
        self.groups = groups or []
        self.auto_create = True
        self._credential_expiration = datetime.max
        self._connection_info = None
        self._connection = None
        self._redshift_client = boto3.Session(region_name=region)\
            .client("redshift")
        self.duration = duration

    @property
    def connection(self):
        if self._connection and self.credentials_are_valid():
            return self._connection
        return self.connect()

    def credentials_are_valid(self):
        return datetime.now().astimezone(
            timezone.utc) > self._credential_expiration

    def connect(self):
        """
        Passes psycopg2.connect arguments to connect_with_options
        :return: the return type of connect_with_options
        """
        options = self.build_options()
        self._connection = self.connector(**options)
        return self._connection

    def build_options(self):
        """
        Builds options for psycopg2.connect.
        These can be translated to work with other functions.
        :return: connect options
        """
        host, port = self.get_address_port()
        user, password = self.get_user_password()
        return dict(host=host, port=port, user=user, password=password,
                    dbname=self.database_name)

    def get_address_port(self) -> Tuple[str, int]:
        """
        Gets the address and port of the Redshift cluster via AWS.
        :return:
        """
        if self._connection_info:
            return self._connection_info
        response = self._redshift_client.describe_clusters(
            ClusterIdentifier=self.cluster_id)

        try:
            clusters = response['Clusters']
            cluster = clusters[0]
            endpoint = cluster['Endpoint']
            self._connection_info = (endpoint['Address'], endpoint['Port'])
            return self._connection_info
        except IndexError:
            raise Exception(f"Cluster {self.cluster_id} not found")

    def get_user_password(self) -> Tuple[str, str]:
        """
        Calls the GetClusterCredentials
        :return:
        """
        response = self._redshift_client.get_cluster_credentials(
            ClusterIdentifier=self.cluster_id,
            DbUser=self.user,
            DbName=self.database_name,
            DbGroups=self.groups,
            AutoCreate=self.auto_create,
            DurationSeconds=self.duration
        )
        credentials = (response['DbUser'], response['DbPassword'])
        self._credential_expiration = response['Expiration']
        return credentials
