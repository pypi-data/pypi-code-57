from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.schemas.splits import bucket_schema_exclude, condition_schema_exclude
from splitiorequests.models.splits.rule import Rule


class RuleSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    buckets = fields.List(fields.Nested(bucket_schema_exclude.BucketSchemaExclude), required=True)
    condition = fields.Nested(condition_schema_exclude.ConditionSchemaExclude, required=True)

    @post_load
    def load_rule(self, data, **kwargs):
        return Rule(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
