from marshmallow import Schema, fields, post_dump, post_load
from splitiorequests.models.splits.treatment import Treatment


class TreatmentSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str(required=True)
    description = fields.Str()
    keys = fields.List(fields.Str())
    segments = fields.List(fields.Str())
    configurations = fields.Str()

    @post_load
    def load_treatment(self, data, **kwargs):
        return Treatment(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return dict(new_data)
