from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.models.splits.bucket import Bucket


class BucketSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    treatment = fields.Str(required=True)
    size = fields.Int(required=True)

    @post_load
    def load_bucket(self, data, **kwargs):
        return Bucket(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
