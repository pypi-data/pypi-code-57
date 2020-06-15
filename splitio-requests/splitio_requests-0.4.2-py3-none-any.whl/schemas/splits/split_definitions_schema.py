from marshmallow import Schema, fields, post_load, post_dump
from splitiorequests.schemas.splits.split_definition_schema import SplitDefinitionSchema
from splitiorequests.models.splits.split_definitions import SplitDefinitions


class SplitDefinitionsSchema(Schema):
    class Meta:
        ordered = True

    objects = fields.List(fields.Nested(SplitDefinitionSchema), required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    totalCount = fields.Int(required=True)

    @post_load
    def load_split_definitions(self, data, **kwargs):
        return SplitDefinitions(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
