# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Auto ML common logging module."""
from typing import Any, Dict, Optional, TYPE_CHECKING
import pkg_resources

from azureml.telemetry.contracts import (RequiredFields,
                                         RequiredFieldKeys,
                                         StandardFields,
                                         StandardFieldKeys,
                                         ExtensionFields,
                                         ExtensionFieldKeys)
from azureml.automl.core.shared import logging_fields
from azureml.automl.core.shared import log_server
from .constants import ComputeTargets
from .utilities import _InternalComputeTypes
from ._azureautomlsettings import AzureAutoMLSettings


def set_run_custom_dimensions(
        automl_settings: AzureAutoMLSettings,
        parent_run_id: Optional[str],
        child_run_id: Optional[str],
        parent_run_uuid: Optional[str] = None,
        child_run_uuid: Optional[str] = None) -> None:
    """
    Create the logger with telemetry hook.

    :param automl_settings: the AutoML settings object
    :param parent_run_id: parent run id
    :param child_run_id: child run id
    :param parent_run_uuid: Parent run UUID
    :param child_run_uuid: Child run UUID
    :return
    """
    azure_automl_sdk_version = pkg_resources.get_distribution("azureml-train-automl-client").version
    automl_core_sdk_version = pkg_resources.get_distribution("azureml-automl-core").version

    custom_dimensions = {
        "automl_client": "azureml",
        "automl_sdk_version": azure_automl_sdk_version,
        "automl_core_sdk_version": automl_core_sdk_version
    }  # type: Dict[str, Optional[Any]]

    fields = {
        RequiredFieldKeys.CLIENT_TYPE_KEY: 'sdk',
        RequiredFieldKeys.CLIENT_VERSION_KEY: azure_automl_sdk_version,
        RequiredFieldKeys.COMPONENT_NAME_KEY: logging_fields.TELEMETRY_AUTOML_COMPONENT_KEY,
        logging_fields.AutoMLExtensionFieldKeys.AUTOML_SDK_VERSION_KEY: azure_automl_sdk_version,
        logging_fields.AutoMLExtensionFieldKeys.AUTOML_CORE_SDK_VERSION_KEY: automl_core_sdk_version,
        ExtensionFieldKeys.DISK_USED_KEY: None
    }

    if automl_settings.is_timeseries:
        task_type = "forecasting"
    else:
        task_type = automl_settings.task_type

    # Override compute target based on environment.
    compute_target = _InternalComputeTypes.identify_compute_type(compute_target=automl_settings.compute_target,
                                                                 azure_service=automl_settings.azure_service)
    if not compute_target:
        if automl_settings.compute_target == ComputeTargets.LOCAL:
            compute_target = _InternalComputeTypes.LOCAL
        elif automl_settings.compute_target == ComputeTargets.AMLCOMPUTE:
            compute_target = _InternalComputeTypes.AML_COMPUTE
        elif automl_settings.spark_service == 'adb':
            compute_target = _InternalComputeTypes.DATABRICKS
        else:
            compute_target = _InternalComputeTypes.REMOTE

    custom_dimensions.update(
        {
            "task_type": task_type,
            "compute_target": compute_target,
            "subscription_id": automl_settings.subscription_id,
            "region": automl_settings.region
        }
    )

    fields[StandardFieldKeys.ALGORITHM_TYPE_KEY] = task_type
    # Don't fill in the Compute Type as it is being overridden downstream by Execution service
    # ComputeTarget field is still logged in customDimensions that contains these values
    # fields[StandardFieldKeys.COMPUTE_TYPE_KEY] = compute_target

    fields[RequiredFieldKeys.SUBSCRIPTION_ID_KEY] = automl_settings.subscription_id
    # Workspace name can have PII information. Therefore, not including it.
    # fields[RequiredFieldKeys.WORKSPACE_ID_KEY] = automl_settings.workspace_name

    snake_cased_fields = {
        logging_fields.camel_to_snake_case(field_name): field_value
        for field_name, field_value in fields.items()
    }

    if parent_run_id is not None:
        log_server.update_custom_dimension(parent_run_id=parent_run_id)
    if child_run_id is not None:
        log_server.update_custom_dimension(run_id=child_run_id)
    if parent_run_uuid is not None:
        log_server.update_custom_dimension(parent_run_uuid=parent_run_uuid)
    if child_run_uuid is not None:
        log_server.update_custom_dimension(run_uuid=child_run_uuid)

    log_server.update_custom_dimensions(snake_cased_fields)
