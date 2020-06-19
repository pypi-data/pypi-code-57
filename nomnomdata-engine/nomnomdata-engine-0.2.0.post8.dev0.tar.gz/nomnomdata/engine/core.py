import collections
import json

from nomnomdata.engine import api
from nomnomdata.engine.logging import getLogger


class EngineParameters(collections.MutableMapping):
    """
        A Dict like collection representing the parameters the running task can access.
    """

    def __init__(self, parameters, task_uuid):
        self.nominode_client = api.NominodeClient()

        self.task_uuid = task_uuid
        if isinstance(parameters, str):
            self.__params = json.loads(parameters)
        else:
            self.__params = parameters
        self.__params["config"] = self.nominode_client.get_secrets()
        self.__connections = []
        for key, values in self.__params.items():
            if isinstance(values, dict) and "connection_uuid" in values:
                self.__connections.append(key)
                self.__params[key].update(
                    self.__params["config"][values["connection_uuid"]]
                )

    def __getitem__(self, key):
        return self.__params[key]

    def __setitem__(self, key, value):
        raise NotImplementedError(
            "Cannot set parameter values directly, use foo.commit(key, value)"
        )

    def commit(self, key, value, local_only=False):
        """
        Send the new parameter value to the nominode.

        Parameters:
            key (string): Parameter key.
            value (dict|list|tuple|bool|None): New value of the parameter. Must be JSON serializable or an exception will occur unless local_only is True.
            local_only (boolean): Set to True to only update the value of the parameter locally and not update the nominode stored version
        Returns:
            None
        """
        if key in self.__connections or key == "config":
            raise NotImplementedError("Updating connections is not currently supported")
        if not local_only:
            self.nominode_client.update_task_parameters(self.task_uuid, {key: value})
        self.__params[key] = value

    def __delitem__(self, key):
        raise ValueError("Cannot delete parameters")

    def __iter__(self):
        return iter(self.__params)

    def __len__(self):
        return len(self.__params)

    def __keytransform__(self, key):
        return key

    def __str__(self):
        return str(self.__params)


class Executable(object):
    """
        The key base class for any task. This must be inherited.
        WARNING : super().__init__() MUST be called before doing anything else in the task!.
        This sets up self.params,self.nominode_client and self.logger for use by the task.
        Extend this class with extra functions that are your code to be run.
        self.logger is special in that it logs all messages to the nominode, using other loggers means users will not see those messages.
    """

    def __init__(self, logger_name="nomigen"):
        self.nominode_client = api.NominodeClient()
        self.logger = getLogger(logger_name)
        self.checkout = self.nominode_client.checkout_execution()
        self.params = EngineParameters(
            self.checkout["parameters"], self.checkout["task_uuid"]
        )
        self.action = self.params.get("action_name", "no_action")
        self.task_uuid = self.checkout["task_uuid"]

    def get_action(self):
        return self.action

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        pass
