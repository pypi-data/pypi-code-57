from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.models.splits.condition import Condition
from splitiorequests.schemas.splits.matcher_schema_exclude import MatcherSchemaExclude


class ConditionSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    combiner = fields.Str(required=True)
    matchers = fields.List(fields.Nested(MatcherSchemaExclude), required=True)

    @post_load
    def load_condition(self, data, **kwargs):
        return Condition(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
