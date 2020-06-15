from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE
from splitiorequests.models.splits.split import Split
from splitiorequests.schemas.splits import tag_schema_exclude, traffic_type_schema_exclude


class SplitSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    description = fields.Str(missing=None)
    trafficType = fields.Nested(traffic_type_schema_exclude.TrafficTypeSchemaExclude)
    creationTime = fields.Integer()
    tags = fields.List(fields.Nested(tag_schema_exclude.TagSchemaExclude), missing=None)

    @post_load
    def load_split(self, data, **kwargs):
        return Split(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if key != 'tags' and key != 'description' and data[key] is None):
            del new_data[field_key]
        return dict(new_data)
