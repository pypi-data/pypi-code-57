import json
import logging
from os import environ
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class NominodeClient:
    def __init__(self):
        self.logger = logging.getLogger("nomigen.nominode_api")
        self.token = environ["token"]
        self.execution_uuid = environ["execution_uuid"]
        self.project_uuid = environ["project_uuid"]
        # ensure we always have a trailing / on the api url, otherwise we mess up urljoin
        api_url = environ["nomnom_api"]
        self.nominode_url = api_url if api_url.endswith("/") else api_url + "/"
        self.session = requests.Session()
        self.session.headers.update({"token": self.token})
        # max value for each backoff is 2 minutes, 20 retries gets us about 30 minutes of retrying
        retries = Retry(total=20, backoff_factor=1, status_forcelist=[502, 503, 504, 404])
        self.session.mount(self.nominode_url, HTTPAdapter(max_retries=retries))

    def request(
        self,
        method,
        url_prefix=None,
        data=None,
        params=None,
        reg_data=None,
        headers=None,
        path_override=None,
    ):
        """
        Authenticated request to nominode.

        Makes an authenticated request to the nominode and returns a JSON blob.

        Parameters:
            method (string): HTTP Method to use (GET,POST,PUT,ect)
            url_prefix (string): Endpoint to hit eg execution/log
            data (dict): Payload for request, must be JSON serializable
            params (dict): URL Parameters, must be url encodable
            reg_data (string): Non JSON data to append to request. Cannot be used with data parameter
            headers (dict): Header dictionary
            path_override (string): Override string for the start of the nominode url (usually /api/v1)

        Returns:
            dict: JSON response data

        """
        response_data = self._get_response_data(
            method=method,
            endpoint_url=url_prefix,
            data=reg_data,
            headers=headers,
            json_data=data,
            params=params,
            path_override=path_override,
        )
        return response_data

    def _get_response_data(
        self,
        method,
        endpoint_url,
        json_data=None,
        params=None,
        data=None,
        headers=None,
        path_override=None,
    ):
        # endpoint urls should not start with a /
        endpoint_url = (
            endpoint_url if not endpoint_url.startswith("/") else endpoint_url.lstrip("/")
        )
        # this is to support overriding /api/1/ to /api/v2 if needed
        if path_override:
            split_url = list(urlsplit(self.nominode_url))
            split_url[2] = path_override
            base_url = urlunsplit(split_url)
            url = urljoin(base_url, endpoint_url)
        else:
            url = urljoin(self.nominode_url, endpoint_url)

        response = self.session.request(
            method, url, headers=headers, params=params, json=json_data, data=data
        )
        try:
            response.raise_for_status()
            data = response.json()
            if data:
                return data
            else:
                raise Exception("Empty json body response calling url: {}".format(url))
        except Exception:
            self.logger.exception(
                f"Error during {method}:{url} - {response.status_code} - response payload:\n{response.text}"
            )
            raise

    def update_progress(self, message=None, progress=None):
        """
        Update nominode with current task progress

        Parameters:
            message (string): Message for to attach to current task progress
            progress (int): Whole number representing the percentage complete of the task (0-100)
        Returns:
            dict: success/response data
        """
        # Called to periodically update the completion status of a given execution
        # Always sets to - '05': 'Executing: Running in docker container'
        if message is None and progress is None:
            raise Exception(
                "Message or Progress needs to be provided when updating execution status..."
            )
        data = {"status_code": "05", "progress": progress, "message": message}
        return self.request("put", "execution/update/%s" % self.execution_uuid, data=data)

    def update_connection(self, connection, connection_uuid):
        """
        Update a connection on the nominode

        Parameters:
            connection (dict): Dictionary representing the updated connection object
            connection_uuid (connection_uuid): UUID of the connection to be updated
        Returns:
            dict: success/response data
        """
        data = {"alias": connection["alias"], "parameters": json.dumps(connection)}
        return self.request("post", "connection/%s/update" % connection_uuid, data=data)

    def checkout_execution(self):
        """
        Fetch the task parameters. Should only be called once.

        Returns:
            dict: task parameters dictionary
        """
        return self.request("put", "execution/checkout/%s" % self.execution_uuid)

    def update_task_parameters(self, task_uuid, parameters):
        """
        Update the task parameters on the nominode

        Parameters:
            task_uuid (connection_uuid): UUID of this task
            parameters (dict): Dictionary representing what the new parameters will be. This overwrites all existing parameters.
        Returns:
            dict: success/response data
        """
        result = self.request(
            "put", "/task/{}/parameters".format(task_uuid), data=parameters
        )
        if "error" in result:
            raise Exception(result["error"])

    def update_result(self, result):
        """
        Update the task parameters on the nominode

        Parameters:
            result (dict): JSON data representing the result of this task. Currently only a json encoded Bokeh plot is supported.
        Returns:
            dict: success/response data
        """
        assert "result_type" in result
        assert "result" in result
        result = self.request(
            "put",
            f"projects/{self.project_uuid}/task_execution/{self.execution_uuid}/result",
            data=result,
            path_override="api/v2/",
        )
        if "error" in result:
            raise Exception(result["error"])
        else:
            return result

    def get_secrets(self):
        """
        Fetch the encoded connections associated with this task
        Returns:
            dict: decoded connections
        """
        x = self.request("get", "execution/decode/%s" % self.execution_uuid)
        if "error" in x:
            raise Exception(x["error"])
        else:
            return x

    def get_metadata_table(self, metadata_uuid, data_table_uuid):
        """
        Fetch a specific metadata table and data table from the nominode

        Parameters:
            metadata_uuid (string): UUID String of the metadata table.
            data_table_uuid (string): UUID String of the data table within the metadata.

        Returns:
            dict: success/response data
        """
        assert metadata_uuid, "metadata_uuid is required"
        assert data_table_uuid, "data_table_uuid is required"

        # Get the data_table details and column information
        url = "metadata/{metadata_uuid}/{data_table_uuid}"
        url = url.format(metadata_uuid=metadata_uuid, data_table_uuid=data_table_uuid)
        data_table = self.request("get", url)
        if "results" in data_table:
            # Grab first data table that matches.
            data_table = data_table["results"][0]
        else:
            raise Exception(
                "Error getting data table details for {}...".format(data_table_uuid)
            )

        return data_table
