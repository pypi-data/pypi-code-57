from .util import get_data_yaml_dict, get_dynamo_table, replace_decimals
from .cdc_parser import CDCParser
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json
import logging

cdc_connection = 'cdc'


class Dynamo:
    def __init__(self):
        self.connections = get_data_yaml_dict(type(self).__name__.lower())

    def get_cdc_data(self, customer_id):
        try:
            c = self.connections[cdc_connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], c['cdc_dynamo_table'])
            items = dynamo_table.scan(FilterExpression=Attr(c['cdc_customer_id_attr']).eq(customer_id))['Items']
            return replace_decimals(items[0]) if len(items) > 0 else None
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_cdc_data")
            return None

    def get_cdc_features(self, customer_id):
        try:
            c = self.connections[cdc_connection]
            item = self.get_cdc_data(customer_id)
            return {'data': item, 'features': CDCParser(item[c['cdc_json_attr']]).get_features()} \
                if item is not None and c['cdc_json_attr'] in item else None
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_cdc_features")
            return None

    def insert(self, connection, table, data_dict):
        try:
            c = self.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            dynamo_table.put_item(Item=json.loads(json.dumps(data_dict), parse_float=Decimal))
            return True
        except Exception as e:
            logging.exception("exception thrown in Dynamo.insert")
            return False

    def get_items_by_key(self, connection, table, pk_attr, pk_value):
        try:
            c = self.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.query(KeyConditionExpression=Key(pk_attr).eq(pk_value))['Items'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_items_by_key")
            return None

    def get_item_by_pk(self, connection, table, pk_attr, pk_value):
        try:
            c = self.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.get_item(Key={pk_attr: pk_value})['Item'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item_by_pk")
            return None

    def get_items(self, connection, table, attr, value):
        try:
            c = self.connections[connection]
            dynamo_table = get_dynamo_table(c['access_key'], c['secret_access_key'], c['region'], table)
            return replace_decimals(dynamo_table.scan(FilterExpression=Attr(attr).eq(value))['Items'])
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_items")
            return None

    def get_item(self, connection, table, attr, value):
        try:
            return self.get_items(connection, table, attr, value)[0]
        except Exception as e:
            logging.exception("exception thrown in Dynamo.get_item")
            return None

    def get_item_by_last_date(self, connection, table, attr, value, date_attr):
        pass

