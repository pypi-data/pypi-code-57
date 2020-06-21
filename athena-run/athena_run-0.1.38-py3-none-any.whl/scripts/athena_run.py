#!/usr/bin/env python
from __future__ import print_function

from distutils import spawn
import os
import os.path as path
import sys
import logging
import argparse
import json
from urllib import request, parse

if os.environ.get("ATHENA_DEBUG"):
    logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

USAGE = """
Usage: athena-run <my_program>

Example: athena-run python main.py

Flags:
--local Run the profiler in local mode, without submitting any output
--output $FILE  Dump Athena Trace output to the path indicated by $FILE. Implies --local
--upload $FILE  Upload at the path indicated by $FILE

Example:
# Run profiler in local mode
athena-run --local python main.py

# Output trace to a file called trace.json
athena-run -o trace.json python main.py

# Upload trace at path "trace.json"
athena-run --upload trace.json
"""


def _root():
    return os.path.dirname(path.abspath(path.join(__file__ ,"../")))

def _add_bootstrap_to_pythonpath(bootstrap_dir):
    """
    Add our bootstrap directory to the head of $PYTHONPATH to ensure
    it is loaded before program code
    """
    python_path = os.environ.get("PYTHONPATH", "")

    if python_path:
        new_path = "%s%s%s" % (bootstrap_dir, os.path.pathsep, os.environ["PYTHONPATH"])
        os.environ["PYTHONPATH"] = new_path
    else:
        os.environ["PYTHONPATH"] = bootstrap_dir


def _upload_file(path):
    url = "http://app.athena-ml.com/api/traces"
    data = open(path, "rb")

    req = request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    resp = request.urlopen(req)

    data = open(path, "rb")
    traces = json.load(data)
    if len(traces["traces"]) > 0:
        for trace in traces["traces"]:
            log.warning(
                "Access the trace for your execution on Athena: %s",
                "http://app.athena-ml.com/traces/{}".format(trace["id"]),
            )


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    log.debug("sys.argv: %s", sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local", action="store_true", help="Run in local mode", required=False
    )

    parser.add_argument(
        "--upload", type=str, help="Upload trace file at PATH", required=False
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output trace to file at PATH. Implies --local",
        required=False,
    )

    args, stem = parser.parse_known_args()
    if args.upload is not None:
        _upload_file(args.upload)
        return

    if args.local:
        os.environ["ATHENA_DRY_RUN"] = "true"

    if args.output:
        os.environ["ATHENA_FILE_OUTPUT"] = args.output

    log.debug("parsed args: %s stem: %s", args, stem)

    root_dir = _root()
    bootstrap_dir = os.path.join(root_dir, "bootstrap")
    log.debug("athena bootstrap: %s", bootstrap_dir)

    _add_bootstrap_to_pythonpath(bootstrap_dir)
    log.debug("PYTHONPATH: %s", os.environ["PYTHONPATH"])
    log.debug("sys.path: %s", sys.path)

    executable = stem[0]
    executable_args = stem[1:]

    # Find the executable path
    executable = spawn.find_executable(executable)
    log.debug("program executable: %s", executable)
    log.debug("program executable args: %s", executable_args)

    if "ATHENA_SERVICE_NAME" not in os.environ:
        # infer service name from program command-line
        service_name = os.path.basename(executable)
        os.environ["ATHENA_SERVICE_NAME"] = service_name

    pid = os.getpid()
    log.debug("Process: %s", pid)
    os.environ["ATHENA_PID"] = str(pid)

    os.execl(executable, executable, *executable_args)
