import io
import os
import os.path as osp
import json
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

NAME = "aiopdhttp"
DESCRIPTION = "Swagger-generated Async API Client for Pulse Robotic Arm"
URL = "https://rozum.com"
EMAIL = "dev@rozum.com"
AUTHOR = "Rozum Robotics"

with open(osp.join(here, "config.json")) as c:
    VERSION = json.loads("".join(c.readlines()))["packageVersion"]

if "dev" in VERSION:
    DEVELOPMENT_STATUS = "Development Status :: 4 - Beta"
else:
    DEVELOPMENT_STATUS = "Development Status :: 5 - Production/Stable"

REQUIRED = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23",
    "aiohttp>=3.6.2",
]


setup(
    name=NAME,
    version=VERSION,
    packages=[p for p in find_packages() if "test" not in p],
    install_requires=REQUIRED,
    url=URL,
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        DEVELOPMENT_STATUS,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: AsyncIO",
    ],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    zip_safe=False,
)
