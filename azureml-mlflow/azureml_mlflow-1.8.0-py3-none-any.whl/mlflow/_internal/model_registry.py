# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowModelRegistry** provides a class to manage MLFlow models in Azure."""

import logging
from functools import wraps

from mlflow.store.model_registry.rest_store import RestStore
from .azureml_reststore import AzureMLAbstractRestStore

_VERSION_WARNING = "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."

logger = logging.getLogger(__name__)


class AzureMLflowModelRegistry(AzureMLAbstractRestStore, RestStore):
    """
    Client for a remote model registry accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """

    def __init__(self, service_context, host_creds=None):
        """
        Construct an AzureMLflowModelRegistry object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        logger.debug("Initializing the AzureMLflowModelRegistry")
        AzureMLAbstractRestStore.__init__(self, service_context, host_creds)
        RestStore.__init__(self, self.get_host_creds)

    @wraps(RestStore._call_endpoint)
    def _call_endpoint(self, *args, **kwargs):
        return super(AzureMLflowModelRegistry, self)._call_endpoint_with_retries(
            super(AzureMLflowModelRegistry, self)._call_endpoint, *args, **kwargs)
