from flask import Flask
from kws_pipeline.workers.worker import Worker
from kws_pipeline.workers.queue_manager import QueueManager
from kws_pipeline.google_helpers.bucket_manager import BucketStorage

queue_manager = QueueManager("http://localhost:8080/")
storage_manager = BucketStorage("test-bucket-hello-kws")


worker = Worker(queue_manager=queue_manager, storage_manager=storage_manager)


@worker.capability
def say_hello(greetings: str, to: str = "world"):
    """
    Says hello to someone
    """
    return f"{greetings}, {to}"


worker.pipeline("Upper greetings", say_hello, str.upper)
worker.build_router()

app = Flask(__name__)
worker.register(app)

if __name__ == "__main__":
    app.run(port=8081)
