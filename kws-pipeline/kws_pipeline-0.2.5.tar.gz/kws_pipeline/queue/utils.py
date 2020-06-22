from flask import Flask, Blueprint

from kws_pipeline.queue.abc import (
    JobResourceABC,
    JobListResourceABC,
    BatchListResourceABC,
    BatchResourceABC,
)


def register_resources(app, model, batch_model, task_manager, task_router):
    class JobListResource(JobListResourceABC):
        _model = model
        _task_manager = task_manager
        _task_router = task_router

    class JobResource(JobResourceABC):
        _model = model
        _task_manager = task_manager
        _task_router = task_router

    class BatchListResource(BatchListResourceABC):
        _model = batch_model
        _task_manager = task_manager
        _task_router = task_router

    class BatchResource(BatchResourceABC):
        _model = batch_model
        _task_manager = task_manager
        _task_router = task_router

    JobListResource.register_to_blueprint(app)
    JobResource.register_to_blueprint(app)
    BatchListResource.register_to_blueprint(app)
    BatchResource.register_to_blueprint(app)
    return app


def apply_middlewares(app, *middlewares):
    for middleware in middlewares:
        app.wsgi_app = middleware(app.wsgi_app)

    return app


def create_app(job_model, batch_model, task_manager, task_router, middlewares=tuple(), url_prefix="/queue/"):
    app = Flask(__name__)
    blueprint = Blueprint("QueueManager", __name__, url_prefix=url_prefix)
    blueprint = register_resources(
        blueprint, job_model, batch_model, task_manager, task_router
    )
    app.register_blueprint(blueprint)
    app = apply_middlewares(app, *middlewares)
    return app
