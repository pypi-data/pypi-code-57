from os import environ

KCB_PASSWORD_GENERATOR_SIZE = int(environ.get(
    "KCB_PASSWORD_GENERATOR_SIZE", 32))
KCB_AWS_REGION_NAME = environ.get("KCB_AWS_REGION_NAME", "us-east-1")
