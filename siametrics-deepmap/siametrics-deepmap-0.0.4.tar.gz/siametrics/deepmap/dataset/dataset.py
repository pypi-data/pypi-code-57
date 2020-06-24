from collections import defaultdict
import json
import requests
import pandas as pd

from google.cloud import bigquery

from siametrics.deepmap.util import get_service_account_request_headers
from .param import Parameter


class DatasetDiscoveryService:
    service_url = 'https://dataset-discovery-service-whzo2dewrq-de.a.run.app'

    def __init__(self, g_cred, project_id):
        self.g_cred = g_cred
        self.project_id = project_id

    def make_request(self, data=None):
        data = json.dumps(data or {})

        url = DatasetDiscoveryService.service_url
        headers = get_service_account_request_headers(self.g_cred, url) if self.g_cred else None

        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()

        return resp

    def get_dataset(self, name):
        resp = self.make_request({'name': name})
        metadata = resp.json()
        return Dataset(name, project_id=self.project_id, metadata=metadata, g_cred=self.g_cred)

    def list_datasets(self):
        resp = self.make_request()
        return resp.json()['datasets']


class Dataset:
    def __init__(self, name, project_id, metadata, g_cred):
        self.name = name
        self.project_id = project_id
        self.__g_cred = g_cred

        self.__params = [Parameter.from_param_dict(param) for param in metadata['params']]

        assert metadata['query']['source'].lower() == 'bigquery'
        self.table = metadata['query']['params']['table']

        self.__schema = None
        self.__num_rows = None
        self.__num_bytes = None
        self.__description = None

    def __get_query(self, fields, **kwargs):
        query = {
            'table': self.table,
            'where': [],
        }

        for param in self.__params:
            name = param.name
            if name in kwargs:
                query = param.modify_query(query, kwargs[name])
            elif param.required:
                raise ValueError(f'Please provide required parameters: {param.name}')

        where_clause = ' AND '.join(query['where'])
        fields_string = ', '.join(fields)
        query_string = f"SELECT {fields_string} FROM {query['table']} WHERE {where_clause}"

        return query_string

    def query(self, query):
        cred = self.__g_cred and self.__g_cred.with_scopes(['https://www.googleapis.com/auth/bigquery'])
        df = pd.read_gbq(query, project_id=self.project_id, credentials=cred)
        return df

    def fetch(self, fields=None, **kwargs):
        fields = fields or ['*']
        query = self.__get_query(fields, **kwargs)
        df = self.query(query)
        return df

    @property
    def params(self):
        params = []
        for param in self.__params:
            record = {
                'name': param.name,
                'type': param.type_,
                'description': param.description,
            }
            params.append(record)
        return pd.DataFrame(params)

    @property
    def num_rows(self):
        if not self.__num_rows:
            self.__load_details()
        return self.__num_rows

    @property
    def num_bytes(self):
        if not self.__num_bytes:
            self.__load_details()
        return self.__num_bytes

    @property
    def description(self):
        if self.__description is None:
            self.__load_description()

        return self.__description

    def __load_schema(self, table):
        schema = []
        for s in table.schema:
            record = {
                'name': s.name,
                'type': s.field_type,
                'repeated': s.mode == 'REPEATED',
                'description': s.description,
            }
            schema.append(record)
        self.__schema = pd.DataFrame(schema).set_index('name')

    def __load_details(self):
        cred = self.__g_cred and self.__g_cred.with_scopes(['https://www.googleapis.com/auth/bigquery.readonly'])
        client = bigquery.Client(credentials=cred, project=self.project_id)

        dataset_id, table_id = self.table.split('.')
        dataset_ref = client.dataset(dataset_id, project=self.project_id)
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        self.__load_schema(table)
        self.__num_rows = table.num_rows
        self.__num_bytes = table.num_bytes

    def __get_stats(self, schema):
        select = []
        for name, s in schema.iterrows():
            if not s.repeated:
                select.append(f'MIN({s.name}) AS {s.name}__min')
                select.append(f'MAX({s.name}) AS {s.name}__max')
            select.append(f'COUNT({s.name}) AS {s.name}__count')
        query = 'SELECT ' + ', '.join(select) + f' FROM {self.table}'

        stats = self.query(query)

        aggs = defaultdict(dict)

        for key, value in stats.iloc[0].to_dict().items():
            name, agg = key.split('__')
            aggs[name][agg] = value

        stats = pd.DataFrame(aggs).T.sort_index(axis=1)
        return stats

    def __load_description(self):
        if self.__schema is None:
            self.__load_details()

        stats = self.__get_stats(self.__schema)
        description = pd.concat([self.__schema, stats], axis=1, sort=True)
        self.__description = description

