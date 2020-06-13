import json
import logging
import time

from typing import Dict, Tuple, List

from machinery.broker.redis import RedisBroker
from machinery.backend.mongodb import MongoDbBackend

# Default queue for machinery tasks.
DEFAULT_QUEUE = "default_queue"

# Default polling frequency in seconds for machinery to check new tasks.
DEFAULT_POLLING_PERIOD = 3


class Value:
    """Represents a value interface between machinery and a Python worker."""

    # A simple dictionary with the following format:
    # {
    #   "Name": "string" (optional)
    #   "Type": "string"|"int"|"int64"|...
    #   "Value": any
    # }
    json: Dict

    def __init__(self, vtype, value, name=None):
        self.json = {"Value": value, "Type": vtype}
        if name is not None:
            self.json["Name"] = name

    def from_dict(table: Dict):
        """Creates a Value from a Python dictionary."""
        return Value(
            vtype=table.get("Type"),
            value=table.get("Value"),
            name=table.get("Name"),
        )

    def name(self):
        """Name of the value."""
        return self.json.get("Name")

    def value(self):
        """Returns the value."""
        return self.json.get("Value")

    def vtype(self):
        """Type of the value."""
        return self.json.get("Type")


class Machinery:
    """Manager instance for a machinery mesh.
    
    Limitations:
    - Only supported broker is Redis
    - Only supported backend is MongoDB
    - One queue per machinery instance. To interact with another queue, create
      another machinery instance in Python.
    - If this instance retrieved a task that it doesn't know how to handle, it
      will send the task back into the queue.
    - No concurrency, one running worker only per machinery instance. If you
      need concurrency, build it on top of this Machinery instance.

    Make sure to register tasks before calling machinery.start().
    """

    # Set to False to stop the manager.
    working: bool = True

    # Machinery broker.
    broker: RedisBroker

    # Machinery backend result.
    backend: MongoDbBackend

    # Machinery queue. Only 1 queue per machinery instance.
    queue: str

    # Lookup table for taskname-to-taskhandler mapping. Key is a string for
    # task names. Value is a task function that will be invoked if the
    # machinery instance retrieved a task from the queue with matching task
    # name.
    tasks: Dict

    def __init__(self, broker_uri, backend_uri, queue=DEFAULT_QUEUE):
        """Inits the machinery manager.
        
        Use Redis URI only for broker_uri.
        Use MongoDB URI only for backend_uri.
        """
        self.broker = RedisBroker(broker_uri)
        self.backend = MongoDbBackend(backend_uri)
        self.queue = queue

        # Instantiate worker lookup table. Key=<task name>, Value=<task handler>
        self.tasks = {}

    def register_task(self, task_name: str, task):
        """Creates a worker task for the given task name."""
        self.tasks[task_name] = task

    def send_simple_task(self, queue: str, task_name: str, args: List):
        """Sends a simple task to the broker."""
        task = self.broker.send_simple_task(queue, task_name,
                                            [arg.json for arg in args])
        return task

    def wait_for_results(self, task: Dict, poll_secs=DEFAULT_POLLING_PERIOD):
        """Waits and retrieve results for given task."""
        while self.working:
            results = self.backend.load_results(task["UUID"])
            if results is None:
                time.sleep(poll_secs)
                continue
        return results

    def start(self, poll_secs=DEFAULT_POLLING_PERIOD):
        """Start consuming tasks from the task queue. This method is blocking."""

        logging.info("Starting Python worker...")

        while self.working:
            task = self.broker.retrieve_task(self.queue, poll_secs)
            if task is None:
                continue

            task_name = task.get("Name")
            if task_name not in self.tasks:
                # If received task isn't handled by any of the registered task
                # callbacks, requeue the task to the broker.
                logging.error(f"Unknown task {task_name} from {self.queue}")
                self.broker.send_task(self.queue, task)
                time.sleep(poll_secs)
                continue

            logging.info(f"Got task: {task.get('UUID')}")

            task = self.tasks.get(task_name)
            try:
                # Convert dictionaries parameters into Value.
                parameters = [
                    Value.from_dict(item) for item in task.get("Args")
                ]
                results = task(*parameters)
                # Convert Value outputs into dictionaries.
                if isinstance(results, list) or isinstance(results, tuple):
                    dict_list = [item.json for item in results]
                else:
                    dict_list = [results.json]
                self._on_task_success(task, dict_list)
            except Exception as err:
                self._on_task_failure(task, str(err))

    def _on_task_success(self, task: Dict, results: Tuple):
        """Post-triggers once a task has been successfully executed."""

        # Save result to backend.
        self.backend.save_state(task, results=results, state="SUCCESS")

        # Success task handler.
        if task.get("OnSuccess") is not None:
            subtask = task.get("OnSuccess")
            # Pass result of the previous task to the success task.
            subtask["Args"] = [result for result in results]
            # Use routing key if specified, else fallback to instance queue.
            queue = subtask.get("RoutingKey") or self.queue
            # Send task task into the queue.
            self.backend.save_state(subtask, state="PENDING")
            self.broker.send_task(queue, subtask)

        # Chord task handler.
        group_uuid = task.get("GroupUUID")
        group_task_count = task.get("GroupTaskCount")
        chord_task = task.get("Chordtask")

        # Skip processing if no tasks, no group or chord is not completed.
        if group_uuid is None or chord_task is None:
            return
        if not self.backend.is_group_completed(group_uuid, group_task_count):
            return

        # Trigger chord task task into the queue.
        subtask = chord_task
        subtask["Args"] = self.backend.load_group_results(group_uuid)
        queue = subtask.get("RoutingKey") or self.queue
        self.backend.save_state(subtask, state="PENDING")
        # Update group_meta collection for the triggering chord.
        self.backend.update_group_meta(group_uuid, chord_triggered=True)
        self.broker.send_task(queue, subtask)

    def _on_task_failure(self, task: Dict, error: str):
        """Post-triggers once a task has failed execution."""

        self.backend.save_state(task, error=error, state="FAILED")

        if task.get("OnError") is not None:
            subtask = task.get("OnError")
            subtask["Args"] = [{
                "Name": "error",
                "Type": "string",
                "Value": error,
            }]
            queue = subtask.get("RoutingKey") or self.queue
            self.backend.save_state(subtask, state="PENDING")
            self.broker.send_task(queue, subtask)
