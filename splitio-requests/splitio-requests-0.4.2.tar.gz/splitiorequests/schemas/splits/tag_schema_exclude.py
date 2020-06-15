from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.models.splits.tag import Tag


class TagSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)

    @post_load
    def load_tag(self, data, **kwargs):
        return Tag(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
