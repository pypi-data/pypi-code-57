from marshmallow import Schema, fields


class JobSchema(Schema):
    task_id = fields.Str()
    uuid = fields.Str()
    status = fields.Str()
    result_path = fields.Str()
    batch_id = fields.Str()


class BatchSchema(Schema):
    batch_id = fields.Str()
    progress = fields.Float()
    result_url = fields.Str()
    finished = fields.Boolean()
    jobs_done = fields.List(fields.Nested(JobSchema))
    jobs_pending = fields.List(fields.Nested(JobSchema))
