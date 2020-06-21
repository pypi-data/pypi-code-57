"""Constants used."""
import logging

_LOGGER = logging.getLogger("pyfireservicerota")

FSR_DEFAULT_TIMEOUT = 20
FSR_ENDPOINT_TOKEN = "oauth/token"
FSR_ENDPOINT_USER = "users/current.json"
FSR_ENDPOINT_MEMBERSHIPS = "memberships/{}/combined_schedule?start_time={}&end_time={}"
