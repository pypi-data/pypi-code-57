#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import libs
from base64 import b64encode


class HarperDbCloud(object):
    def __init__(self, username, password, instance_url):
        self.errors = []
        if not username or not password or not instance_url:
            self.errors.append({
                "code": 0,
                "response": "No instance created. Required fields were not supplied."
            })
        else:
            self.username = username
            self.password = password
            self.instance_url = instance_url

    def get_headers(self):
        basic_token = b64encode(bytes("{0}:{1}".format(self.username, self.password).encode('utf-8'))).decode("utf-8",
                                                                                                              "ignore")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {0}'.format(basic_token)
        }
        return headers

    def get_json_body(self, operation, schema=None, is_sql=False, sql_command=None, table_name=None,
                      hash_attribute=None,
                      records=None, file_path=None):
        json_dict = {}
        if not is_sql:
            if not schema:
                self.errors.append({
                    "code": 0,
                    "response": "No schema name provided."
                })
                return {}
            json_dict = {
                'operation': operation,
                'schema': schema
            }
            if table_name:
                json_dict['table'] = table_name
            if hash_attribute:
                json_dict['hash_attribute'] = hash_attribute
            if records:
                json_dict['records'] = records
            if file_path:
                json_dict['file_path'] = file_path
        else:
            json_dict = {
                'operation': operation,
                'sql': sql_command
            }
        return json_dict

    def create_dev_schema(self, instance_name):
        dev_schema_json = self.get_json_body(operation="create_schema", schema=instance_name)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

    def create_table(self, schema_name, table_name, hash_attribute="id"):
        dev_schema_json = self.get_json_body(operation="create_table", schema=schema_name, table_name=table_name,
                                             hash_attribute=hash_attribute)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

    def insert_record(self, schema_name, table_name, records, hash_attribute="id"):
        dev_schema_json = self.get_json_body(operation="insert", schema=schema_name, table_name=table_name,
                                             records=records, hash_attribute=hash_attribute)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

    def update_record(self, schema_name, table_name, records):
        dev_schema_json = self.get_json_body(operation="update", schema=schema_name, table_name=table_name,
                                             records=records)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

    def insert_via_csv(self, schema_name, table_name, file_path, hash_attribute="id"):
        dev_schema_json = self.get_json_body(operation="csv_file_load", schema=schema_name, table_name=table_name,
                                             file_path=file_path, hash_attribute=hash_attribute)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

    def run_sql_command(self, sql_command):
        dev_schema_json = self.get_json_body(operation="sql", is_sql=True, sql_command=sql_command)
        if dev_schema_json:
            result = libs.browser.data_post(url=self.instance_url, json_data=dev_schema_json,
                                            headers=self.get_headers(),
                                            errors=self.errors)
            if not result[0]:
                self.errors = result[1]
                return None
            else:
                return result[1]
        else:
            return None

























