"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import decimal
from unittest.mock import patch

import boto3
from boto3.dynamodb import types


class FloatSerializer(types.TypeSerializer):
    """
    This class can be used to patch the default dynamo serializer.
    Example:
        with patch('boto3.dynamodb.types.TypeSerializer', new=FloatSerializer), \
            patch('boto3.dynamodb.types.TypeDeserializer', new=FloatDeserializer):
            dynamodb = boto3.resource("dynamodb")
    """

    # Workaround to serialize float to Decimal
    # Credits: https://github.com/boto/boto3/issues/665#issuecomment-559892366
    def _is_number(self, value):
        if isinstance(value, (int, decimal.Decimal, float)):
            return True
        return False

    def _serialize_n(self, value):
        if isinstance(value, float):
            with decimal.localcontext(types.DYNAMODB_CONTEXT) as context:
                context.traps[decimal.Inexact] = 0
                context.traps[decimal.Rounded] = 0
                number = str(context.create_decimal_from_float(value))
                return number

        number = super(FloatSerializer, self)._serialize_n(value)
        return number

    def _serialize_m(self, value):
        return {str(k): self.serialize(v) for k, v in value.items()}


class FloatDeserializer(types.TypeDeserializer):
    def _deserialize_n(self, value):
        return float(value)


def create_resource_with_float_serializer():
    """
    Return a patched version of the boto3 dynamodb resource.
    This version of the resource will automatically convert float to Decimal and the reverse.

    :return: A DynamoDB resource who use float instead of Decimal.
    :rtype: DynamoDB
    """
    with patch("boto3.dynamodb.types.TypeSerializer", new=FloatSerializer), \
         patch("boto3.dynamodb.types.TypeDeserializer", new=FloatDeserializer):
        return boto3.resource("dynamodb")


def query_all_items(dynamo_resource, table_name, **kwargs):
    """
    Iterate over all the pages in the query result and concatenate them.

    :param dynamo_resource: The DynamoDB resource.
    :type dynamo_resource: DynamoDB
    :param table_name: the table name
    :type table_name: str
    :param kwargs: the query arguments. See Boto3 documentation.
    :return: All items in the table matching the query.
    :rtype: list
    """
    table = dynamo_resource.Table(table_name)
    response = table.query(**kwargs)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.query(**kwargs)
        items.extend(response['Items'])

    return items
