import pickle
import json
from abc import ABC, abstractclassmethod, abstractmethod
from typing import Callable, Dict, Iterable, Optional, Type
from uuid import uuid1

from flask import make_response, Response, request, url_for
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import fields
import requests

from .schema import JobSchema, BatchSchema


class ModelABC(object):
    @abstractclassmethod
    def create(cls, **kwargs) -> Response:
        raise NotImplementedError

    @abstractmethod
    def save(self):
        raise NotImplementedError

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

        self.save()
        return self

    @abstractclassmethod
    def get(cls) -> Iterable:
        raise NotImplementedError

    @abstractclassmethod
    def get_by_id(cls, uuid: str):
        raise NotImplementedError

    @abstractclassmethod
    def delete(cls, uuid: str):
        raise NotImplementedError


Model = Type[ModelABC]


class TaskLoggerABC(object):
    @abstractclassmethod
    def save_job(cls, job_data):
        raise NotImplementedError


TaskLogger = Type[TaskLoggerABC]


class TaskManagerABC(object):
    def _create_task(self, uuid, binary_data, handler_uri):
        raise NotImplementedError

    def _enqueue(self, task):
        raise NotImplementedError


TaskManager = Type[TaskManagerABC]


class ResourceABC(MethodResource):
    _default_serializer: Callable = pickle.dumps
    _model: Model = ModelABC
    _task_manager: TaskManager = TaskManagerABC
    _task_router: Dict = dict()

    def _get(self, uuid):
        return self._model.get_by_id(uuid)

    def _create_task(self, binary_data: bytes, handler_uri: str):
        return self._task_manager._create_task(binary_data, handler_uri)

    def _enqueue(self, task: Dict):
        return self._task_manager._enqueue(task)

    @classmethod
    def register_to_blueprint(cls, blueprint):
        return blueprint.add_url_rule(cls.url, view_func=cls.as_view(cls.endpoint_name))


class JobListResourceABC(ResourceABC):
    url = "/"
    endpoint_name = "joblist_resource_api"

    @marshal_with(JobSchema(many=True))
    def get(self):
        return self._model.get()

    @marshal_with(JobSchema)
    @use_kwargs(
        {
            "uuid": fields.Str(),
            "task_type": fields.Str(),
            "json_data": fields.Str(),
            "batch_id": fields.Str(),
        }
    )
    def post(self, task_type, json_data, batch_id=None, uuid=None):
        uuid = uuid or uuid1().hex
        serializer = self._task_router.get("serializer") or self._default_serializer
        data = json.loads(json_data)
        data["uuid"] = uuid
        binary_data = serializer(data)
        task = self._create_task(binary_data, self._task_router.get(task_type))
        response = self._enqueue(task)
        job_data = dict(
            task_id=response.name,
            task_type=task_type,
            status="waiting",
            result_path=None,
            uuid=uuid,
            batch_id=batch_id,
        )
        job = self._model.create(**job_data)

        return job, 201


class JobResourceABC(ResourceABC):
    url = "/<uuid>/"
    endpoint_name = "job_resource_api"

    @marshal_with(JobSchema)
    def get(self, uuid):
        return self._get(uuid)

    @marshal_with(JobSchema)
    @use_kwargs(JobSchema)
    def put(self, uuid, **kwargs):
        job = self._get(uuid)
        if job is None:
            self._model.create(uuid=uuid, **kwargs)

        else:
            job.update(**kwargs)

        return job, 201

    def delete(self, uuid):
        job = self._get(uuid)
        job.delete()
        return {}, 204


class BatchListResourceABC(ResourceABC):
    url = "/batches/"
    endpoint_name = "batchlist_resource_api"

    @marshal_with(BatchSchema(many=True))
    def get(self):
        return self._model.get()

    @marshal_with(BatchSchema)
    @use_kwargs(
        {
            "batch_id": fields.Str(),
            "task_types": fields.List(fields.Str()),
            "json_datas": fields.List(fields.Str()),
            "task_ids": fields.List(fields.Str()),
        }
    )
    def post(self, task_types, json_datas, batch_id=None, task_ids=None):
        batch_uuid = batch_id or uuid1().hex
        task_ids = task_ids or [uuid1().hex] * len(task_types)

        for task_id, task_type, json_data in zip(task_ids, task_types, json_datas):
            r = requests.post(
                request.url_root + url_for("QueueManager.joblist_resource_api"),
                data=dict(
                    uuid=task_id,
                    task_type=task_type,
                    json_data=json_data,
                    batch_id=batch_uuid,
                ),
            )

        batch = self._model.create(batch_id=batch_uuid)
        return batch, 201


class BatchResourceABC(ResourceABC):
    url = "/batches/<uuid>/"
    endpoint_name = "batch_resource_api"

    @marshal_with(BatchSchema)
    def get(self, uuid):
        return self._model.get_and_format_by_id(uuid)

    @marshal_with(BatchSchema)
    @use_kwargs(BatchSchema)
    def put(self, uuid, **kwargs):
        batch = self._get(uuid)
        if batch is None:
            self._model.create(uuid=uuid, **kwargs)

        else:
            batch.update(**kwargs)

        return batch, 201

