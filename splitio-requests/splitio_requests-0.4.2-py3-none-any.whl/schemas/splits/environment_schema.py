from marshmallow import Schema, fields, post_load, post_dump
from splitiorequests.models.splits.environment import Environment


class EnvironmentSchema(Schema):
    class Meta:
        ordered = True

    environment_id = fields.Str(data_key='id', required=True)
    name = fields.Str(required=True)

    @post_load
    def load_environment(self, data, **kwargs):
        return Environment(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
