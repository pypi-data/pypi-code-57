from dotenv import load_dotenv, find_dotenv

print(load_dotenv(find_dotenv()))

from flask import Flask

from kws_pipeline.google_helpers.task_manager import GoogleTaskManager
from kws_pipeline.google_helpers.job_model import Job, Batch
from kws_pipeline.google_helpers.middlewares import NDBClientMiddleware
from kws_pipeline.queue.utils import create_app

task_manager = GoogleTaskManager(
    project_id="hello-infra-kws",
    location="europe-west1",
    queue="simulations",
    worker_url="http://localhost:8081",
)

task_router = {
    "say-hello": "/worker/say-hello",
    "upper-greetings": "/worker/upper-greetings",
}

if __name__ == "__main__":
    queue_manager = create_app(
        job_model=Job,
        batch_model=Batch,
        task_manager=task_manager,
        task_router=task_router,
        middlewares=(NDBClientMiddleware,),
    )
    queue_manager.run(port=8080, debug=True)
