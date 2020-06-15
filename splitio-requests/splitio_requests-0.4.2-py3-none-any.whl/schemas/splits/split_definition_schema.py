from marshmallow import Schema, fields, post_dump, post_load
from splitiorequests.models.splits.split_definition import SplitDefinition
from splitiorequests.schemas.splits import traffic_type_schema, rule_schema, treatment_schema, default_rule_schema, \
    environment_schema


class SplitDefinitionSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str()
    environment = fields.Nested(environment_schema.EnvironmentSchema)
    trafficType = fields.Nested(traffic_type_schema.TrafficTypeSchema)
    killed = fields.Bool()
    treatments = fields.List(fields.Nested(treatment_schema.TreatmentSchema), required=True)
    defaultTreatment = fields.Str(required=True)
    baselineTreatment = fields.Str()
    trafficAllocation = fields.Int()
    rules = fields.List(fields.Nested(rule_schema.RuleSchema))
    defaultRule = fields.List(fields.Nested(default_rule_schema.DefaultRuleSchema), required=True)
    creationTime = fields.Int()
    lastUpdateTime = fields.Int()
    comment = fields.Str()

    @post_load
    def load_split_definition(self, data, **kwargs):
        return SplitDefinition(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return dict(new_data)
