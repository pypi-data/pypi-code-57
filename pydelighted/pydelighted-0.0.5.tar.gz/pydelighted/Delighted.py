import os
import requests
import yaml

from pydelighted.useful import process_data, get_column_names


class Delighted:
    def __init__(self, dbstream, var_env_key, config_file_path, version='v1'):
        self.dbstream = dbstream
        self.var_env_key = var_env_key
        self.url = "https://api.delighted.com/%s/" % version
        self.config_file_path = config_file_path
        self.api_key = os.environ["DELIGHTED_%s_API_KEY" %var_env_key]
        self.endpoints = yaml.load(open(self.config_file_path), Loader=yaml.FullLoader).get('endpoints')
        self.schema_prefix = yaml.load(open(self.config_file_path), Loader=yaml.FullLoader).get("schema_prefix")

    def get_endpoint_data(self, endpoint, params):
        url = self.url + endpoint + '.json'
        return requests.get(url, params=params, auth=(self.api_key, ""))

    def get_date_field(self, endpoint):
        if not endpoint.get('date_fields'):
            return ("created_at", "updated_at")
        return endpoint.get('date_fields')

    def get_table(self, endpoint_key):
        endpoint = self.endpoints.get(endpoint_key)
        if not endpoint.get('table'):
            return endpoint_key + 's'
        return endpoint.get('table')

    def main(self, endpoint_key, batch_size=100, page=1, since=None, until=None):
        params = {"page": page,
                  "per_page": batch_size,
                  "updated_since": since,
                  "updated_until": until,
                  }
        dbstream=self.dbstream
        endpoint = self.endpoints.get(endpoint_key)
        date_fields = self.get_date_field(endpoint)
        table = self.get_table(endpoint_key)

        raw_data = self.get_endpoint_data(endpoint_key, params).json()
        data = process_data(raw_data, date_fields)
        columns = get_column_names(data)
        dbstream.send_with_temp_table( data, columns, 'id', self.schema_prefix, table)
        while raw_data:
            params["page"] = params["page"] + 1
            raw_data = self.get_endpoint_data(endpoint_key, params).json()
            data = process_data(raw_data, date_fields)
            columns = get_column_names(data)
            dbstream.send_with_temp_table(data, columns, 'id', self.schema_prefix, table)
