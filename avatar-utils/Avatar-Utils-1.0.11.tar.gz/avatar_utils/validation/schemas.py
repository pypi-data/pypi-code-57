from logging import getLogger

from marshmallow import Schema, fields
from marshmallow.validate import Equal
from werkzeug.exceptions import BadRequest  # noqa: PyPackageRequirements

logger = getLogger('sample-service')


class ResponseSchema(Schema):
    headers = fields.Dict(required=True, allow_none=False, default=dict())
    message = fields.Str(required=True, allow_none=True, default='')
    result = fields.Dict(required=True, allow_none=True)
    success = fields.Bool(required=True, allow_none=False)


class RootResponseSchema(Schema):
    name = fields.Str(required=True, allow_none=False)
    version = fields.Str(required=False, allow_none=True, default=None)


class SuccessResponseSchema(ResponseSchema):
    success = fields.Bool(required=True, allow_none=False, validate=Equal(True), default=True)


class ErrorResponseSchema(ResponseSchema):
    success = fields.Bool(required=True, allow_none=False, validate=Equal(False), default=False)
