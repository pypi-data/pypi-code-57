import os
from distutils.util import convert_path

from .age_verification import SandboxAgeVerificationBuilder
from .client import SandboxClientBuilder
from .token import YotiTokenRequestBuilder

DEFAULTS = {
    "YOTI_API_URL": "https://api.yoti.com",
    "YOTI_API_PORT": 443,
    "YOTI_API_VERSION": "v1",
    "YOTI_API_VERIFY_SSL": "true",
}

DEFAULT_SANDBOX_URL = DEFAULTS["YOTI_API_URL"] + "/sandbox/v1"

main_ns = {}

directory_name = os.path.dirname(__file__)
version_path = os.path.join(directory_name, "version.py")

ver_path = convert_path(version_path)
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

__version__ = main_ns["__version__"]

__all__ = [
    __version__,
    SandboxClientBuilder,
    SandboxAgeVerificationBuilder,
    YotiTokenRequestBuilder,
]
