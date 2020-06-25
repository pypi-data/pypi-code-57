from logging import getLogger

from flask import g, request
from sqlalchemy.exc import DatabaseError

from . import logs
from .models import *

logger = getLogger(__name__)


@logs.before_app_request
def before_request():
    log_prefix = f'[ LOGGING BEFORE | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        log_id = Log.init(request)
        g.log_id = log_id
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')


@logs.after_app_request
def after_request(response):
    log_prefix = f'[ LOGGING AFTER | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        if g.log_id is not None:
            Log.complete(g.log_id, response)
        else:
            print('log_id is None, cannot complete logging process')
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')
    return response
