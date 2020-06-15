from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE
from splitiorequests.models.splits.split_definition import SplitDefinition
from splitiorequests.schemas.splits import (
    traffic_type_schema_exclude,
    rule_schema_exclude,
    treatment_schema_exclude,
    default_rule_schema_exclude,
    environment_schema_exclude
)


class SplitDefinitionSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str()
    environment = fields.Nested(environment_schema_exclude.EnvironmentSchemaExclude)
    trafficType = fields.Nested(traffic_type_schema_exclude.TrafficTypeSchemaExclude)
    killed = fields.Bool()
    treatments = fields.List(fields.Nested(treatment_schema_exclude.TreatmentSchemaExclude), required=True)
    defaultTreatment = fields.Str(required=True)
    baselineTreatment = fields.Str()
    trafficAllocation = fields.Int()
    rules = fields.List(fields.Nested(rule_schema_exclude.RuleSchemaExclude))
    defaultRule = fields.List(fields.Nested(default_rule_schema_exclude.DefaultRuleSchemaExclude), required=True)
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
