import base64
import json
import time
# REMOVE
import logging

from functools import wraps

from requests import api as requests_api

# mapping: url -> jwt token
cached_jwt = {}


def _wrap(f):
    @wraps(f)
    def wrapper(*args, **kwgs):
        if kwgs.pop("gcp_auth", True) is False:
            # REMOVE
            logging.info("gcp_auth set to false, using normal requests")

            return f(*args, **kwgs)

        url = kwgs["url"]
        headers = kwgs.pop("headers", None) or {}
        jwt = cached_jwt.get(url, None)
        if _jwt_expired(jwt):
            # REMOVE
            logging.info(f"jwt expired or not set for {url}, refreshing")

            jwt = _get_gcp_auth_token(url)
            cached_jwt[url] = jwt
        # REMOVE
        else:
            logging.info(f"using cached jwt for {url}")

        # REMOVE
        logging.info(f"request {url} -> {jwt}")

        headers.update({"Authorization": f"bearer {jwt}"})
        return f(*args, headers=headers, **kwgs)

    return wrapper


# Exported
request = _wrap(requests_api.request)
get = _wrap(requests_api.get)
head = _wrap(requests_api.head)
post = _wrap(requests_api.post)
put = _wrap(requests_api.put)
patch = _wrap(requests_api.patch)
delete = _wrap(requests_api.delete)
options = _wrap(requests_api.options)


def _get_gcp_auth_token(url: str) -> str:
    token_request_url = ("http://metadata/computeMetadata/v1/instance/service-accounts"
                         f"/default/identity?audience={url}")
    token_response = requests_api.get(token_request_url,
                                      headers={"Metadata-Flavor": "Google"})
    return token_response.content.decode("utf-8")


def _jwt_expired(jwt: str) -> bool:
    if not jwt or len(jwt) == 0:
        return True

    jwt_arr = jwt.split(".")
    jwt_payload = base64.b64decode(f"{jwt_arr[1]}==").decode()
    expiry = int(json.loads(jwt_payload)["exp"])
    # Add 30 seconds to allow time for requests
    now = int(time.time()) + 30

    return expiry <= now
