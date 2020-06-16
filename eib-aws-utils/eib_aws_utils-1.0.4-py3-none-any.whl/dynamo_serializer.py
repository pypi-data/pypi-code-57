"""
    Copyright Engie Impact Sustainability Solution EMEAI 2020.
    All rights reserved.
"""

__author__ = 'Engie Impact Sustainability Solution EMEAI'

import decimal

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
