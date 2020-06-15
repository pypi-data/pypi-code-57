from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE
from splitiorequests.schemas.splits import between_schema_exclude, depends_schema_exclude
from splitiorequests.models.splits.matcher import Matcher


class MatcherSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    matcher_type = fields.Str(required=True, data_key='type')
    negate = fields.Bool()
    attribute = fields.Str()
    string = fields.Str()
    depends = fields.Nested(depends_schema_exclude.DependsSchemaExclude)
    strings = fields.List(fields.Str())
    date = fields.Int()
    between = fields.Nested(between_schema_exclude.BetweenSchemaExclude)
    number = fields.Int()
    bool = fields.Bool()

    @post_load
    def load_matcher(self, data, **kwargs):
        return Matcher(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return dict(new_data)
