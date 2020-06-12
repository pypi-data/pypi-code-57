"""
Module with useful user permissions classes meant to be used with Django Rest Framework.
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import requests
from django.conf import settings
from jsm_user_services.services.google import perform_recaptcha_validation
from jsm_user_services.services.user import get_user_data_from_server
from rest_framework import permissions
from rest_framework.request import Request


class JSMUserBasePermission(permissions.BasePermission):
    """
    Base class for JSM user permissions. Implements methods for validating requests against
    the user micro service so that any type of permission can be carried out (role, status, etc).
    """

    APPEND_USER_DATA = getattr(settings, "JSM_USER_SERVICES_DRF_APPEND_USER_DATA", True)
    USER_DATA_ATTR_NAME = getattr(settings, "JSM_USER_SERVICES_DRF_REQUEST_USER_DATA_ATTR_NAME", "user_data")
    USER_SERVICE_NOT_AUTHORIZED_CODES = (401, 403, 404)

    @classmethod
    def _retrieve_user_data(cls, request: Request) -> Dict:
        try:
            user_data = getattr(request, cls.USER_DATA_ATTR_NAME)
        except AttributeError:
            user_data = get_user_data_from_server()

        return user_data

    @classmethod
    def _validate_request_against_user_service(cls, request: Request, append_user_data_to_request: bool = True) -> Dict:
        """
        Gets valid user_data from the User micro service.
        """
        try:
            user_data: Dict = cls._retrieve_user_data(request)

            if append_user_data_to_request:
                setattr(request, cls.USER_DATA_ATTR_NAME, user_data)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in cls.USER_SERVICE_NOT_AUTHORIZED_CODES:
                return {}

            raise

        return user_data

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Abstract method that must be implemented by children classes.
        """
        raise NotImplementedError("This method must be overridden!")


class StatusBasedPermission(JSMUserBasePermission):
    """
    Base class for the status-based permissions. Implements methods for validating requests against
    the user micro service and an utility method that asserts that the user has the appropriate status.
    """

    @classmethod
    def _validate_user_status(cls, request: Request, allowed_status: List[str]):
        """
        Validates if the user has the appropriate status against the allowed status.
        """
        append_user_data_to_request = cls.APPEND_USER_DATA
        user_data = cls._validate_request_against_user_service(
            request, append_user_data_to_request=append_user_data_to_request
        )

        if "status" not in user_data:
            return False

        return user_data["status"] in allowed_status


class RoleBasedPermission(JSMUserBasePermission):
    """
    Base class for the role-based permissions. Implements methods for validating requests against
    the user micro service and an utility method that asserts that the user has the appropriate role.
    """

    @classmethod
    def _validate_user_role(cls, request: Request, allowed_roles: List[str]):
        """
        Validates if the user has the appropriate role against the allowed roles.
        """
        append_user_data_to_request = cls.APPEND_USER_DATA
        user_data = cls._validate_request_against_user_service(
            request, append_user_data_to_request=append_user_data_to_request
        )
        user_roles: List[str] = user_data.get("roles", [])

        if not user_roles:
            return False

        return any([user_role in allowed_roles for user_role in user_roles])


class ProfessionalUserPermission(RoleBasedPermission):
    """
    Permission that allows only users with the role 'professional'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user is a professional.
        """
        return self._validate_user_role(request, allowed_roles=["professional"])


class EmployeeOrManagerUserPermission(RoleBasedPermission):
    """
    Permission that allows only users with the role 'employee' or 'manager'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user is either an employee or manager.
        """
        return self._validate_user_role(request, allowed_roles=["employee", "manager"])


class EmployeeOnlyUserPermission(RoleBasedPermission):
    """
    Permission that allows only users with the role 'employee'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user is an employee.
        """
        return self._validate_user_role(request, allowed_roles=["employee"])


class OwnerUserPermission(RoleBasedPermission):
    """
    Permission that allows only users with the role 'owner'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user is an owner.
        """
        return self._validate_user_role(request, allowed_roles=["owner"])


class AnyLoggedUserPermission(RoleBasedPermission):
    """
    Permission that allows users to access the requested resource regardless
    of their roles as long as they have a VALID, NON EXPIRED JSM JWT.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user is just logged in with a valid jwt (non expired).
        """
        return self._validate_user_role(request, allowed_roles=["professional", "employee", "manager", "owner"])


class ActiveUserPermission(StatusBasedPermission):
    """
    Permission that allows only users which the status is 'active'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user status is 'active'.
        """
        return self._validate_user_status(request, allowed_status=["active"])


class PendingValidationUserPermission(StatusBasedPermission):
    """
    Permission that allows only users which the status is 'pending-validation'.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        """
        Asserts that the user status is 'pending-validation'.
        """
        return self._validate_user_status(request, allowed_status=["pending-validation"])


class GoogleRecaptchaPermission(permissions.BasePermission):
    """
    A permission class which deals which checks if the request is authorized by Google Recaptcha V3.

    In order to use it, the request must have the key "g_recaptcha_response" or "g-recaptcha-response" on the request's
    body or header. Otherwise the request won't be authorized without even checking it on Google.

    Just be aware that a header with underscore is not allowed. So do not use the key "g_recaptcha_response"
    on the header.
    """

    @classmethod
    def has_permission(cls, request: Request, view: Any) -> bool:
        """
        Retrieves the Google data on the request and then performs a request to Google, in order to check if the
        received data is valid or not.
        """

        g_recaptcha_response = cls._retrieve_g_recaptcha_response(request)
        if not g_recaptcha_response:
            return False

        return perform_recaptcha_validation(g_recaptcha_response)

    @classmethod
    def _retrieve_g_recaptcha_response(cls, request: Request) -> Optional[str]:
        """
        Merges the request data (header and body), and then looks up for expected keys.

        When merging the request data, if the same key is present on header and body, the header data will be
        overridden by the body value.
        """

        merged_request_data = {**request.headers, **request.data}

        return merged_request_data.get("g_recaptcha_response", merged_request_data.get("g-recaptcha-response", None))
