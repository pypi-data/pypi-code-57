from .util import get_data_yaml_dict
from .cdc_parser import CDCParser
from boto3.dynamodb.conditions import Attr
import boto3

cdc_connection = 'cdc'


class Dynamo:
    def __init__(self):
        self.connections = get_data_yaml_dict(type(self).__name__.lower())

    def get_cdc_data(self, customer_id):
        c = self.connections[cdc_connection]
        dynamodb = boto3.resource('dynamodb',
                                 aws_access_key_id=c['access_key'],
                                 aws_secret_access_key=c['secret_access_key'],
                                 region_name=c['region'])
        # Retrieve DynamoDB table resource
        dynamo_table = dynamodb.Table(c['cdc_dynamo_table'])
        return dynamo_table.scan(FilterExpression=Attr(c['cdc_customer_id_attr']).eq(customer_id))['Items'][0]

    def get_cdc_features(self, customer_id):
        c = self.connections[cdc_connection]
        item = self.get_cdc_data(customer_id)

        return {'data': item, 'features': CDCParser(item[c['cdc_json_attr']]).get_features()}
