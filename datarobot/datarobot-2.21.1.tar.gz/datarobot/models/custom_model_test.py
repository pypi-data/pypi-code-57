import time

import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.errors import AsyncProcessUnsuccessfulError
from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class CustomModelTest(APIObject):
    """An custom model test.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        test id
    dataset_id: str
        id of a dataset used for testing
    dataset_version_id: str
        id of a dataset version used for testing
    custom_model_image_id: str
        id of a custom model image
    overall_status: str
        a string representing testing status.
        Status can be
        - 'not_tested': the check not run
        - 'failed': the check failed
        - 'succeeded': the check succeeded
        - 'warning': the check resulted in a warning, or in non-critical failure
        - 'in_progress': the check is in progress
    detailed_status: dict
        detailed testing status - maps the testing types to their status and message.
        The keys of the dict are one of 'errorCheck', 'nullValueImputation',
        'longRunningService', 'sideEffects'.
        The values are dict with 'message' and 'status' keys.
    created_by: str
        a user who created a test
    completed_at: str, optional
        ISO-8601 formatted timestamp of when the test has completed
    created_at: str, optional
        ISO-8601 formatted timestamp of when the version was created
    """

    _path = "customModelTests/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("dataset_id"): t.String(),
            t.Key("dataset_version_id"): t.String(),
            t.Key("custom_model_image_id"): t.String(),
            t.Key("overall_status"): t.String(),
            t.Key("testing_status") >> "detailed_status": t.Dict(
                {
                    t.Key("error_check"): t.Dict(
                        {
                            t.Key("status"): t.String(),
                            t.Key("message"): t.String(allow_blank=True),
                        }
                    ),
                    t.Key("null_value_imputation"): t.Dict(
                        {
                            t.Key("status"): t.String(),
                            t.Key("message"): t.String(allow_blank=True),
                        }
                    ),
                    t.Key("long_running_service"): t.Dict(
                        {
                            t.Key("status"): t.String(),
                            t.Key("message"): t.String(allow_blank=True),
                        }
                    ),
                    t.Key("side_effects"): t.Dict(
                        {
                            t.Key("status"): t.String(),
                            t.Key("message"): t.String(allow_blank=True),
                        }
                    ),
                }
            ),
            t.Key("created_by"): t.String(),
            t.Key("completed_at", optional=True): t.String(allow_blank=True),
            t.Key("created", optional=True) >> "created_at": t.String(),
        }
    ).allow_extra("*")

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return encode_utf8_if_py2(
            u"{}({!r})".format(self.__class__.__name__, self.id)
        )

    def _set_values(
        self,
        id,
        dataset_id,
        dataset_version_id,
        custom_model_image_id,
        overall_status,
        detailed_status,
        created_by,
        completed_at=None,
        created_at=None,
    ):
        self.id = id
        self.dataset_id = dataset_id
        self.dataset_version_id = dataset_version_id
        self.custom_model_image_id = custom_model_image_id
        self.overall_status = overall_status
        self.detailed_status = detailed_status
        self.created_by = created_by
        self.completed_at = completed_at
        self.created_at = created_at

    @classmethod
    def create(
            cls,
            custom_model_id,
            custom_model_version_id,
            dataset_id,
            environment_id,
            environment_version_id=None,
            max_wait=DEFAULT_MAX_WAIT,
    ):
        """Create and start a custom model test.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model
        custom_model_version_id: str
            the id of the custom model version
        dataset_id: str
            the id of the testing dataset
        environment_id: str
            the id of the execution environment
        environment_version_id: str, optional
            the id of the execution environment version
        max_wait: int, optional
            max time to wait for a test completion.
            If set to None - method will return without waiting.

        Returns
        -------
        CustomModelTest
            created custom model test

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {
            "custom_model_id": custom_model_id,
            "custom_model_version_id": custom_model_version_id,
            "dataset_id": dataset_id,
            "environment_id": environment_id,
            "environment_version_id": environment_version_id,
        }
        response = cls._client.post(cls._path, data=payload)

        # at this point custom model test is already created
        custom_model_test = cls.list(custom_model_id)[0]

        if max_wait is None:
            # return without waiting for the test to finish
            return custom_model_test
        else:
            try:
                # wait for the test to finish
                custom_model_test_loc = wait_for_async_resolution(
                    cls._client, response.headers['Location'], max_wait
                )
                return cls.from_location(custom_model_test_loc)
            except AsyncProcessUnsuccessfulError:
                # if the job was aborted server sends appropriate status and
                # `wait_for_async_resolution` raises exception,
                # but the test has been already created, and contains error log,
                # so return the test

                # the test needs some time to update its state
                max_state_wait = 10
                custom_model_test.refresh()

                start_time = time.time()
                while custom_model_test.overall_status == 'in_progress':
                    if time.time() >= start_time + max_state_wait:
                        raise
                    time.sleep(1)
                    custom_model_test.refresh()

                return custom_model_test

    @classmethod
    def list(cls, custom_model_id):
        """List custom model tests.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_id: str
            the id of the custom model

        Returns
        -------
        List[CustomModelTest]
            a list of custom model tests

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {"custom_model_id": custom_model_id}
        data = unpaginate(cls._path, payload, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_model_test_id):
        """Get custom model test by id.

        .. versionadded:: v2.21

        Parameters
        ----------
        custom_model_test_id: str
            the id of the custom model test

        Returns
        -------
        CustomModelTest
            retrieved custom model test

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = "{}{}/".format(cls._path, custom_model_test_id)
        return cls.from_location(path)

    def get_log(self):
        """Get log of a custom model test.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}{}/log/".format(self._path, self.id)
        return self._client.get(path).text

    def get_log_tail(self):
        """Get log tail of a custom model test.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}{}/tail/".format(self._path, self.id)
        return self._client.get(path).text

    def cancel(self):
        """Cancel custom model test that is in progress.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}{}/".format(self._path, self.id)
        self._client.delete(path)

    def refresh(self):
        """Update custom model test with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = "{}{}/".format(self._path, self.id)

        response = self._client.get(path)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))
