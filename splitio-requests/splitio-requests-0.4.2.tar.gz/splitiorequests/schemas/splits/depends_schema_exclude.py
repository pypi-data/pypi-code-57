from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.models.splits.depends import Depends


class DependsSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    splitName = fields.Str(required=True)
    treatments = fields.List(fields.Str(), required=True)

    @post_load
    def load_depends(self, data, **kwargs):
        return Depends(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
