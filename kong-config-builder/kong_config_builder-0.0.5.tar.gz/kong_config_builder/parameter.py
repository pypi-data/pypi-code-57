import boto3
import logging

from typing import List, Tuple, Optional
from functools import reduce
from kong_config_builder.password import PasswordManager
from kong_config_builder.settings import KCB_AWS_REGION_NAME


class ParameterStoreAPI:
    def __init__(
        self,
        client=boto3.client("ssm", region_name=KCB_AWS_REGION_NAME),
        password=PasswordManager
    ):
        self._logger = logging.getLogger(__name__)
        self._client = client
        self._password_manager = password

        self._available_parameters_cache = {}

    def get(self, name: str) -> Optional[str]:
        value = self._available_parameters_cache.get(name, None)
        return value

    def put(
        self,
        name: str,
        value: str,
        tags: List[Tuple] = [],
        encrypt: bool = True,
        overwrite: bool = False
    ) -> None:
        _type = "SecureString" if encrypt else "String"
        _tags = list(map(lambda tag: {"Key": tag[0], "Value": tag[1]}, tags))
        try:
            self._client.put_parameter(
                Name=name,
                Value=value,
                Tags=_tags,
                Type=_type,
                Overwrite=overwrite
            )
            self._available_parameters_cache[name] = value
        except Exception as err:
            self._logger.error(err)

    def populate(self, namespace: str) -> None:
        parameters_list = self._get_parameters_by(namespace)

        for parameter in parameters_list:
            values = self._get_value_by(parameter)
            self._available_parameters_cache[parameter] = values[parameter]

    def _get_parameters_by(self, namespace: str) -> List:
        paginate = self._client.get_paginator("describe_parameters")
        parameter_filters = [{
            "Key": "Name",
            "Values": [namespace],
            "Option": "BeginsWith"
        }]
        iterator = paginate.paginate(ParameterFilters=parameter_filters)
        params = set()
        for page in iterator:
            for parameter in page["Parameters"]:
                params.add(parameter["Name"])

        return list(params)

    def _get_value_by(self, key: str):
        def objecter(current, next):
            current[next["Name"]] = next["Value"]
            return current
        parameters = self._client.get_parameters(
            Names=[key],
            WithDecryption=True
        )

        return reduce(objecter, parameters["Parameters"], {})
