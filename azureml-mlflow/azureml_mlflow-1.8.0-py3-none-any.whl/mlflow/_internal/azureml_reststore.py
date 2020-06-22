# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLTrackingStore** provides a base class for MLFlow RestStore related handling."""

import logging
import time
from abc import ABCMeta
from mlflow.utils.rest_utils import MlflowHostCreds
from mlflow.exceptions import RestException

from azureml.core.authentication import AzureMLTokenAuthentication
from azureml._restclient.clientbase import DEFAULT_BACKOFF, DEFAULT_RETRIES
from azureml._restclient.run_client import RunClient
from azureml._restclient.workspace_client import WorkspaceClient

_VERSION_WARNING = "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."

logger = logging.getLogger(__name__)


class AzureMLAbstractRestStore(object):
    """
    Client for a remote rest server accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """
    __metaclass__ = ABCMeta

    def __init__(self, service_context, host_creds=None):
        """
        Construct an AzureMLRestStore object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        self.service_context = service_context
        self.get_host_creds = host_creds if host_creds is not None else self.get_host_credentials
        self.workspace_client = WorkspaceClient(service_context)

    def get_host_credentials(self):
        """
        Construct a MlflowHostCreds to be used for obtaining fresh credentials and the host url.

        :return: The host and credential for rest calls.
        :rtype: mlflow.utils.rest_utils.MlflowHostCreds
        """
        return MlflowHostCreds(
            self.service_context._get_run_history_url() +
            "/mlflow/v1.0" + self.service_context._get_workspace_scope(),
            token=self.service_context.get_auth().get_authentication_header()["Authorization"][7:])

    @classmethod
    def _call_endpoint_with_retries(cls, rest_store_call_endpoint, *args, **kwargs):
        total_retry = DEFAULT_RETRIES
        backoff = DEFAULT_BACKOFF
        for i in range(total_retry):
            try:
                return rest_store_call_endpoint(*args, **kwargs)
            except RestException as rest_exception:
                more_retries_left = i < total_retry - 1
                is_throttled = rest_exception.json.get("error", {"code": 0}).get("code") == "RequestThrottled"
                if more_retries_left and is_throttled:
                    logger.debug("There were too many requests. Try again soon.")
                    cls._wait_for_retry(backoff, i, total_retry)
                else:
                    raise

    @classmethod
    def _wait_for_retry(cls, back_off, left_retry, total_retry):
        delay = back_off * 2 ** (total_retry - left_retry - 1)
        time.sleep(delay)

    def _update_authentication(self, run_id, experiment_name):
        """
        Helper function for initializing the AzureMLTokenAuthentication class
        to avoid expiring AAD tokens. Also initializes the AzureML token refresher.

        :param run_id: The run id for the Run.
        :type run_id: str
        :param experiment_name: The name of the experiment.
        :type experiment_name: str
        """
        run_client = RunClient(self.service_context, experiment_name, run_id)
        token = run_client.get_token().token
        auth = AzureMLTokenAuthentication.create(
            azureml_access_token=token,
            expiry_time=None,
            host=self.service_context._get_run_history_url(),
            subscription_id=self.service_context.subscription_id,
            resource_group_name=self.service_context.resource_group_name,
            workspace_name=self.service_context.workspace_name,
            experiment_name=experiment_name,
            run_id=run_id
        )
        self.service_context._authentication = auth
