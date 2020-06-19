import json

from rest_framework import status


def debug_response(response):
    return json.dumps(response.json(), indent=4, sort_keys=True)


def assert_response_status(response, status):
    assert response.status_code == status, debug_response(response)


def assert_status_ok(response):
    assert_response_status(response, status.HTTP_200_OK)


def assert_status_created(response):
    assert_response_status(response, status.HTTP_201_CREATED)


def assert_status_no_content(response):
    assert_response_status(response, status.HTTP_204_NO_CONTENT)


def assert_status_forbidden(response):
    assert_response_status(response, status.HTTP_403_FORBIDDEN)


def assert_status_not_allowed(response):
    assert_response_status(response, status.HTTP_405_METHOD_NOT_ALLOWED)
