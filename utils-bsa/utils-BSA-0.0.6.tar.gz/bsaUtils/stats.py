import os
import boto3
import json
from decimal import Decimal


dynamodb_resource = boto3.resource("dynamodb")


def add_item_to_table(item, table_name):
    table = dynamodb_resource.Table(table_name)
    try:
        item = json.loads(json.dumps(item), parse_float=Decimal)
        table.put_item(
            Item=item
        )
    except Exception as e:
        print(str(e))
        return False
    return True
