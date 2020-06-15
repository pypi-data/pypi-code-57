from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE
from splitiorequests.models.splits.traffic_type import TrafficType


class TrafficTypeSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    traffic_id = fields.Str(required=True, data_key='id')
    name = fields.Str(required=True)

    @post_load
    def load_traffic_type(self, data, **kwargs):
        return TrafficType(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
