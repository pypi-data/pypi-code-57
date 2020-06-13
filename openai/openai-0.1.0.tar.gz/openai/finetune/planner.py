import logging
from openai.util import log_info
from collections import deque
import time
from openai.api_resources.file import File

import json
import os
import tempfile

import openai
from openai import encoding
from openai.api_resources.abstract import (
    APIResource,
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
)

logger = logging.getLogger(__name__)


class Planner:
    def __init__(self, output, encoding):
        self.encoding = encoding
        self._output = output
        self.file = tempfile.NamedTemporaryFile(
            mode="w+", prefix=output + ".tmp" if output is not None else None
        )
        self._write({"method": "headers", "params": {"encoding": self.encoding}})
        if self.sync:
            self.executor = Executor(model=model, engine=engine)
        else:
            self.executor = None

    def add(self, endpoint, **params):
        self._write({"method": endpoint, "params": params})

    def _write(self, record):
        json.dump(record, self.file)
        self.file.write("\n")

    def make_encoding(self):
        return encoding.get(self.encoding)

    def close(self):
        if self._output is not None:
            log_info("Moving scheduling info to final destination", output=self._output)
            os.rename(self.file.name, self._output)
        try:
            self.file.close()
        except FileNotFoundError:
            pass


class SyncPlanner:
    def __init__(self, engine, model, encoding, lines=None):
        self.engine = engine
        self.model = model
        self.branch = openai.Branch.create(engine=engine, model=model)
        logger.info(f"Created branch: engine={engine} id={self.branch.id}")
        self.encoding = encoding

        self.callbacks = deque()
        self.completed = []

        self.state = {"lines": lines}
        self.i = 0

        self.max_depth = 2

    def add(self, endpoint, **params):
        if self.i == 0:
            self.state["start"] = time.time()
            self.state["last_log"] = time.time()

        # TODO: turn branch -> model here too
        if endpoint == "POST /v1/updates":
            update = openai.Update.create(
                engine=self.engine, branch=self.branch.id, **params
            )
            self.callbacks.append(self.make_cb(update, self.i))
        elif endpoint == "POST /v1/completions":
            self.flush_to(0)
            completion = openai.Completion.create(
                engine=self.engine, model=self.branch.id, **params
            )
            self.completed.append(completion)
            self.callbacks.append(
                self.make_cb(completion, self.i, is_promise=False, params=params)
            )
        elif endpoint == "POST /v1/snapshots":
            snapshot = openai.Snapshot.create(
                engine=self.engine, branch=self.branch.id, **params
            )
            self.callbacks.append(self.make_cb(snapshot, self.i))
        self.i += 1
        self.flush_to(self.max_depth)

    def on_complete(self, object, params=None):
        if object["object"] == "completion":
            logprobs = params.get("logprobs")
            if logprobs is not None and logprobs >= 0:
                for snippet in object["snippets"]:
                    logger.info(
                        f"[LOGPROBS] {sum([t for t in snippet['logprobs']['token_logprobs'] if t is not None])}"
                    )

            if params.get("max_tokens", 16) > 0:
                for choice in object["choices"]:
                    logger.info(f"[COMPLETION] {choice['text']}")
        else:
            logger.info(f"Completed: {json.dumps(object)}")
        self.completed.append(object)

    def flush_to(self, depth=0):
        while len(self.callbacks) > depth:
            callback = self.callbacks.popleft()
            callback()

    def make_cb(self, object, i, is_promise=True, params=None):
        submit_start = time.time()

        def cb():
            wait_start = time.time()
            if is_promise:
                while True:
                    object.wait(60)
                    if object.status == "complete":
                        break
                    logger.info(
                        f"Waited 60s for object, going to wait again: {object.to_dict()}"
                    )

                end = time.time()
                end_to_end_time = end - submit_start
                wait_time = end - wait_start
                logger.info(
                    f"Finished: end_to_end={end_to_end_time:0.3f}s wait={wait_time:0.3f}s object={object.to_dict_recursive()}"
                )

            self.on_complete(object, params=params)

            now = time.time()
            if now - self.state["last_log"] < 30:
                self.state["last_log"] = time.time()

                lines = self.state["lines"]
                delta = (now - self.state["start"]) / 60
                if lines is not None:
                    lines_info = f" total={lines} progress={i/lines*100:0.1f}%"
                else:
                    lines_info = ""
                logger.info(
                    f"Progress: finished={i+1} lines_per_minute={i / delta:0.3f}{lines_info}"
                )

        return cb

    def make_encoding(self):
        return encoding.get(self.encoding)
