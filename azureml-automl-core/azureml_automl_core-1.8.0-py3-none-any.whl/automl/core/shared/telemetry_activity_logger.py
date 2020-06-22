# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Telemetry activity logger."""
from typing import Any, Dict, Iterator, Optional
from datetime import datetime
import logging
import uuid

from azureml.automl.core.shared import constants as constants
from azureml.automl.core.shared import log_server

from azureml.telemetry import get_event_logger
from azureml.telemetry.contracts import (Event, RequiredFields, RequiredFieldKeys, StandardFields, StandardFieldKeys,
                                         ExtensionFields, ExtensionFieldKeys)
from .activity_logger import ActivityLogger
from .logging_fields import AutoMLExtensionFieldKeys, WHITELISTED_PROPERTIES, update_schematized_fields


class TelemetryActivityLogger(ActivityLogger):
    """Telemetry activity logger."""

    def __init__(self):
        """
        Construct activity logger object.
        """
        self._event_logger = get_event_logger()

    def _log_activity(self,
                      logger: logging.Logger,
                      activity_name: str,
                      activity_type: Optional[str] = None,
                      custom_dimensions: Optional[Dict[str, Any]] = None) -> Iterator[None]:
        """
        Log activity with duration and status.

        :param logger: logger
        :param activity_name: activity name
        :param activity_type: activity type
        :param custom_dimensions: custom dimensions
        """
        activity_info = {'activity_id': str(uuid.uuid4()),
                         'activity_name': activity_name,
                         'activity_type': activity_type}  # type: Dict[str, Any]

        with log_server.lock:
            activity_info.update(log_server.custom_dimensions)
            required_fields, standard_fields, extension_fields = \
                update_schematized_fields(log_server.custom_dimensions)

        activity_status = constants.Status.Started
        completion_status = constants.TelemetryConstants.SUCCESS

        start_time = datetime.utcnow()
        logger.info("ActivityStarted: {}".format(activity_name), extra={"properties": activity_info})
        self._log_status_event(
            required_fields,
            standard_fields,
            extension_fields,
            activity_name=activity_name,
            activity_status=activity_status)

        activity_status = constants.Status.Completed
        try:
            yield
        except Exception:
            completion_status = constants.TelemetryConstants.FAILURE
            activity_status = constants.Status.Terminated
            raise
        finally:
            end_time = datetime.utcnow()
            duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)
            activity_info["durationMs"] = duration_ms
            activity_info["completionStatus"] = completion_status

            logger.info("ActivityCompleted: Activity={}, HowEnded={}, Duration={}[ms]".
                        format(activity_name, completion_status, duration_ms),
                        extra={"properties": activity_info})
            self._log_status_event(
                required_fields,
                standard_fields,
                extension_fields,
                activity_name,
                activity_status=activity_status,
                completion_status=completion_status,
                duration_milliseconds=duration_ms)

    def _log_status_event(self,
                          required_fields: RequiredFields,
                          standard_fields: StandardFields,
                          extension_fields: ExtensionFields,
                          activity_name: str,
                          activity_status: str,
                          completion_status: Optional[str] = None,
                          duration_milliseconds: Optional[float] = None) -> None:
        extension_fields[AutoMLExtensionFieldKeys.ACTIVITY_STATUS_KEY] = activity_status
        if completion_status is not None:
            extension_fields[AutoMLExtensionFieldKeys.COMPLETION_STATUS_KEY] = completion_status
        if duration_milliseconds is not None:
            extension_fields[AutoMLExtensionFieldKeys.DURATION_IN_MILLISECONDS_KEY] = duration_milliseconds

        self._log_event(required_fields, standard_fields, extension_fields, event_name=activity_name)

        extension_fields.pop(AutoMLExtensionFieldKeys.ACTIVITY_STATUS_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.COMPLETION_STATUS_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.DURATION_IN_MILLISECONDS_KEY, None)

    def _log_error_event(self,
                         required_fields: RequiredFields,
                         standard_fields: StandardFields,
                         extension_fields: ExtensionFields,
                         failure_reason: str,
                         error_code: str,
                         exception_class: str,
                         error_message: str,
                         traceback_message: str,
                         is_critical: bool = False,
                         exception_target: Optional[str] = None) -> None:
        extension_fields[AutoMLExtensionFieldKeys.EXCEPTION_CLASS_KEY] = exception_class
        extension_fields[AutoMLExtensionFieldKeys.EXCEPTION_TARGET_KEY] = exception_target
        standard_fields[StandardFieldKeys.FAILURE_REASON_KEY] = failure_reason
        extension_fields[AutoMLExtensionFieldKeys.INNER_ERROR_CODE_KEY] = error_code
        extension_fields[AutoMLExtensionFieldKeys.IS_CRITICAL_KEY] = is_critical
        extension_fields[AutoMLExtensionFieldKeys.TRACEBACK_MESSAGE_KEY] = traceback_message

        self._log_event(required_fields, standard_fields, extension_fields, event_name=error_message)

        extension_fields.pop(AutoMLExtensionFieldKeys.EXCEPTION_CLASS_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.EXCEPTION_TARGET_KEY, None)
        standard_fields.pop(StandardFieldKeys.FAILURE_REASON_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.INNER_ERROR_CODE_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.IS_CRITICAL_KEY, None)
        extension_fields.pop(AutoMLExtensionFieldKeys.TRACEBACK_MESSAGE_KEY, None)
        self._event_logger.flush()

    def _log_event(self,
                   required_fields: RequiredFields,
                   standard_fields: StandardFields,
                   extension_fields: ExtensionFields,
                   event_name: str) -> None:
        self._redact_fields(required_fields, standard_fields, extension_fields)
        event = Event(name=event_name,
                      required_fields=required_fields,
                      standard_fields=standard_fields,
                      extension_fields=extension_fields)

        self._event_logger.log_event(telemetry_event=event, white_listed_properties=WHITELISTED_PROPERTIES)

    def _redact_fields(self,
                       required_fields: RequiredFields,
                       standard_fields: StandardFields,
                       extension_fields: ExtensionFields) -> None:
        # Remove experiment id from V2 schema
        extension_fields.pop(AutoMLExtensionFieldKeys.EXPERIMENT_ID_KEY, None)
