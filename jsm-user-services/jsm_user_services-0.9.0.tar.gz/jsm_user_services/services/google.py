import logging

from django.conf import settings
from jsm_user_services.exception import MissingRequiredConfiguration
from jsm_user_services.support.http_utils import request

logger = logging.getLogger(__name__)

GOOGLE_RECAPTCHA_URL = getattr(settings, "GOOGLE_RECAPTCHA_URL", "https://www.google.com/recaptcha/api/siteverify")
GOOGLE_RECAPTCHA_SECRET_KEY = getattr(settings, "GOOGLE_RECAPTCHA_SECRET_KEY")


def perform_recaptcha_validation(g_recaptcha_response: str) -> bool:
    """
    Performs a request to Google in order to validate the reCAPTCHA.
    For more details, check: https://developers.google.com/recaptcha/docs/verify
    """

    logger.debug("Performing request to Google to check if recaptcha is valid")

    if not GOOGLE_RECAPTCHA_SECRET_KEY:
        raise MissingRequiredConfiguration("Please, provide 'GOOGLE_RECAPTCHA_SECRET_KEY' on the project's setting")

    data = {"response": g_recaptcha_response, "secret": GOOGLE_RECAPTCHA_SECRET_KEY}

    with request() as r:
        resp = r.post(GOOGLE_RECAPTCHA_URL, data=data)
    result_json = resp.json()

    logger.debug(f"Status code: {resp.status_code}; body: {result_json}")

    return result_json.get("success")
