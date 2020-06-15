from logging import Logger, getLogger
from typing import Optional

from flasgger import Swagger
from flask import Flask
from marshmallow import ValidationError
from requests import post

from avatar_utils.validation import SuccessResponseSchema
from avatar_utils.validation.constants import ServiceHTTPCodes

logger = getLogger(__name__)

def service_registration(swagger: Swagger,
                         url: str,
                         service_name: str,
                         username: str,
                         password: str) -> Optional[dict]:
    app: Flask = swagger.app

    with app.app_context():
        spec = swagger.get_apispecs()
        logger.debug(f'spec = {spec}')

    try:
        response = post(url=url, json=dict(username=username,
                                           password=password,
                                           api_description=spec))
        if response.status_code == ServiceHTTPCodes.OK.value:
            logger.debug(response.json())
            data = SuccessResponseSchema().loads(response.text)
            logger.info(f'Service {service_name} registration completed')
            return data
        else:
            logger.debug(response.text)
            raise Exception
    except ValidationError as err:
        logger.error('Incorrect service registration response')
        logger.error(err.messages)
    except Exception as err:  # noqa W0703
        logger.error(err)
        logger.error(f'Something going wrong during service {service_name} registration')
