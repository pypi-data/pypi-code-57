# -*- coding: utf-8 -*-
"""Top-level package for twinthread."""
from twinthread.twinthread.jupyter import register_jupyter
from twinthread.twinthread.string import task_string_to_context

__author__ = """Brent Baumgartner"""
__email__ = "brent@twinthread.com"
__version__ = "0.4.0"

import re
import json
import requests
import pandas as pd
from io import StringIO


def do_login(base_url, username):
    import getpass

    password = getpass.getpass("Password?")
    response = requests.post(
        f"{base_url}/Token",
        {"grant_type": "password", "username": username, "password": password},
    )

    if response.status_code != 200:
        raise Exception("Invalid credentials")

    print("Login succeeded")

    return response.json()["access_token"]


def select_keys(obj, keys):
    # print("filtered", {k:v for k, v in obj.items() if k not in keys})
    return {k: v for k, v in obj.items() if k in keys}


default_keys = [
    "name",
    "operationId",
    "status",
    "modelId",
    "assetModelId",
    "taskId",
    "description",
    "executionLevel",
    "isActive",
    "type",
]

import os


def mkdir(name):
    try:
        os.stat(name)
    except Exception as e:
        os.mkdir(name)


def filter_results(results, search_text="", keys=default_keys):
    return [
        select_keys(result, keys)
        for result in results
        if search_text.lower() in result["name"].lower()
    ]


class TwinThreadClient:
    def __init__(self, base_url="https://dev.twinthread.com"):
        self.__access_token = "UNAUTHORIZED"
        self.__base_url = base_url
        self.__context = {}

        self.__files = []
        self.__request_id = None
        self.__input_data = None

    def login(self, username):
        self.__access_token = do_login(self.__base_url, username)

    def __auth_check(self):
        if self.__access_token == "UNAUTHORIZED":
            raise Exception("Client must be authorized for this action.")
        return True

    def __post_base(self, route, body):
        self.__auth_check()

        headers = {"Authorization": f"Bearer {self.__access_token}"}
        data = {**self.__context, **body}
        print("body", data)
        response = requests.post(
            f"{self.__base_url}/api{route}", data=data, headers=headers
        )

        if response.status_code != 200:
            raise Exception("Request failed")

        return response

    def __post(self, route, body):
        response = self.__post_base(route, body)
        try:
            return response.json()
        except:
            raise Exception("Invalid server response. Please check query.")

    def __post_data(self, route, body):
        response = self.__post_base(route, body)
        return pd.read_csv(StringIO(response.text))

    def __require_model_context(self):
        if "modelId" not in self.__context:
            raise Exception(
                "Context Required: Please set API context to a model or pass one in as an argument to this function."
            )
        return True

    def __require_instance_context(self):
        if "assetModelId" not in self.__context or "modelId" not in self.__context:
            raise Exception(
                "Context Required: Please set API context to a model instance or pass one in as an argument to this function."
            )
        return True

    def __require_operation_context(self):
        if (
            "assetModelId" not in self.__context
            or "modelId" not in self.__context
            or "operationId" not in self.__context
        ):
            raise Exception(
                "Context Required: Please set API context to a model instance or pass one in as an argument to this function."
            )
        return True

    def __require_task_context(self):
        if (
            "assetModelId" not in self.__context
            or "modelId" not in self.__context
            or "operationId" not in self.__context
            or "taskId" not in self.__context
        ):
            raise Exception(
                "Context Required: Please set API context to a task or pass one in as an argument to this function."
            )
        return True

    def set_context(self, context):
        if isinstance(context, str):
            try:
                context = task_string_to_context(context)
            except Exception as e:
                print(e)
                pass

        # if context.get("name", False):
        #     print("Set context to:", context["name"])
        # else:
        #     print("Context set.")
        self.__context = context

    def get_context(self):
        return self.__context

    def __get_operation(self):
        self.__require_operation_context()
        return self.__post("/Model/Index", {})

    def get_org(self):
        self.__require_operation_context()
        return self.__post("/Model/Index", {})

    def list_models(self, search_text=""):
        models = self.__post("/Model/List", {})
        return filter_results(models, search_text)

    def list_model_instances(self, model, search_text=""):
        instances = self.__post("/Search/ListModelInstances", model)
        return filter_results(instances, search_text)

    def list_instance_operations(self, instance, search_text=""):
        operations = self.__post("/Model/ListOperations", instance)
        return filter_results(operations, search_text)

    def get_tasks(self, search_text="", filter=True):
        operation = self.__get_operation()
        tasks = operation.get("tasks", [])
        if filter:
            return filter_results(tasks, search_text)
        else:
            return tasks

    def get_task(self, context):
        operation = self.__post("/Model/Index", context)

        matches = [
            t for t in operation.get("tasks", []) if t["taskId"] == context["taskId"]
        ]
        if len(matches) > 0:
            return matches[0]

        raise Exception("Could not find task.")

    def get_instance_content(self):
        self.__require_instance_context()
        return self.__post("/Model/ListContent", {})

    def _update_task_code(self, task, code):
        configuration = json.loads(task["configuration"])
        configuration["pythonCode"] = code
        task["configuration"] = json.dumps(configuration)
        return self.__post("/Model/UpdateTask", task)

    def get_input_data(self, task={}):
        if isinstance(task, str):
            task = task_string_to_context(task)
        if self.__input_data is not None:
            return self.__input_data
        return self.__post_data(
            "/Model/ExportPortData",
            {**task, "portId": "input,dataset", "useAttachment": False},
        )

    def get_output_data(self, task={}):
        if isinstance(task, str):
            task = task_string_to_context(task)
        self.__require_task_context()
        return self.__post_data(
            "/Model/ExportPortData",
            {**task, "portId": "dataset", "useAttachment": False},
        )

    def _start_run(self, request_id, input_data):
        self.__request_id = request_id
        self.__files = []
        self.__input_data = input_data

    def _get_files(self):
        return self.__files

    def get_organization_name(self):
        return self.__post("/Organization/Open", {})["organization"]["name"]

    def __save_local_file(self, file_type, name, contents):

        blob_name = re.sub(r"\W+", "", name).lower()
        mkdir("./tasks")
        mkdir(f"./tasks/{self.__request_id}")
        path = f"./tasks/{self.__request_id}/{blob_name}"

        with open(path, "w") as f:
            f.write(contents)

        self.__files.append((file_type, name, path))

    def __save_remote_file(self, type, name, contents):
        blob_name = re.sub(r"\W+", "", name).lower()
        organization_name = "demo"  # this only works with masterdb right now.
        blob_name = f"{self.__context['assetModelId']}_{self.__context['taskId']}_{blob_name}_org{organization_name}_i0"

        response_type = "text/csv" if type is "table" else "arraybuffer"
        content_type = "b" if response_type is "arraybuffer" else ""

        self.__auth_check()

        filename = type + "_" + name
        file = open(filename, "w" + content_type)
        file.write(contents)
        file.close()
        from requests_toolbelt import MultipartEncoder

        m = MultipartEncoder(
            fields={
                "assetModelId": str(self.__context["assetModelId"]),
                "taskId": str(self.__context["taskId"]),
                "name": blob_name,
                "file": (blob_name, open(filename, "rb"), "text/csv"),
            }
        )

        headers = {
            "Authorization": f"bearer {self.__access_token}",
            "Content-Type": m.content_type,
        }

        p = requests.post(
            f"{self.__base_url}/api/Model/ImportTaskData", data=m, headers=headers
        )

    def save_table(self, table, name=""):
        if not isinstance(table, pd.DataFrame):
            raise ValueError("Table must be a pandas dataframe, not " + type(table))

        if name == "":
            name = "dataset"

        if self.__request_id is not None:
            self.__save_local_file("table", name, table.to_csv())
        else:
            self.__save_remote_file("table", name, table.to_csv())

        print("Saved table", name)


register_jupyter()
