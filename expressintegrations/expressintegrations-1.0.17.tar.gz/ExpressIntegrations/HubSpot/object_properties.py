from ..HTTP.Requests import *
from .hubspot import BASE_URL
from .hubspot import HEADERS


def get_properties(object_type):
  post_url = f"{BASE_URL}crm/v3/properties/{object_type}?archived=false"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve deal. Result: {result}")
  return result


def get_property(object_type, property_name):
  post_url = f"{BASE_URL}crm/v3/properties/{object_type}/{property_name}?archived=false"
  result = get(post_url, HEADERS)
  if not Utils.is_success(result['status_code']):
    raise Exception(f"Failed to retrieve deal. Result: {result}")
  return result
