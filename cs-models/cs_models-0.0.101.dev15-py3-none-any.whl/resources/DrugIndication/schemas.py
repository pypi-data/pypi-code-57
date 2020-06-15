from marshmallow import (
    Schema,
    fields,
    validate,
)


class DrugIndicationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    set_id = fields.String(validate=not_blank, required=True)
    lowercase_indication = fields.String(validate=not_blank, required=True)
    indication = fields.String(validate=not_blank, required=True)
    updated_at = fields.DateTime()


class DrugIndicationQueryParamsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer()
    set_id = fields.String(validate=not_blank)
    lowercase_indication = fields.String(validate=not_blank)
    indication = fields.String(validate=not_blank)


class DrugIndicationPatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    set_id = fields.String(validate=not_blank)
    lowercase_indication = fields.String(validate=not_blank)
    indication = fields.String(validate=not_blank)
