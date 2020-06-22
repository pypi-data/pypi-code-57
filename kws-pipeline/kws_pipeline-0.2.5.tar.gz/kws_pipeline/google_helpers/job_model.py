from google.cloud import ndb
from flask import make_response

from ..queue.abc import ModelABC


class Job(ModelABC, ndb.Model):
    task_id = ndb.StringProperty()
    batch_id = ndb.StringProperty()
    task_type = ndb.StringProperty()
    uuid = ndb.StringProperty()
    status = ndb.StringProperty()
    result_path = ndb.StringProperty()

    def save(self):
        super().put()

    @classmethod
    def create(cls, **kwargs):
        job = cls(**kwargs)
        job.put()
        return job

    @classmethod
    def get(cls):
        r = make_response({"name": "coucou"}, 201)
        return [j for j in cls.query()]

    @classmethod
    def get_by_id(cls, uuid):
        return cls.query().filter(cls.uuid == uuid).get()


class Batch(ModelABC, ndb.Model):
    batch_id = ndb.StringProperty()
    result_url = ndb.StringProperty()

    def save(self):
        super().put()

    @classmethod
    def get(cls):
        print("hello")
        return [b for b in cls.query()]

    @classmethod
    def create(cls, **kwargs):
        batch = cls(**kwargs)
        batch.put()
        return batch

    @classmethod
    def get_by_id(cls, batch_id):
        batch = cls.query().filter(cls.batch_id == batch_id).get()
        return batch

    @classmethod
    def get_and_format_by_id(cls, batch_id):
        batch = cls.query().filter(cls.batch_id == batch_id).get()
        jobs = Job.query().filter(Job.batch_id == batch_id)
        done = [j for j in jobs.filter(Job.status == "done")]
        pending = [j for j in jobs.filter(Job.status != "done")]
        finished = len(pending) == 0

        return {
            "batch_id": batch_id,
            "result_url": batch.result_url,
            "finished": finished,
            "jobs_done": done,
            "jobs_pending": pending,
            "progress": len(done) / (len(pending) + len(done)),
        }

