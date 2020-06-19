import pendulum

from cc_py_commons.config.env import app_config
from cc_py_commons.utils.redis import distance_db_conn

def pc_miler_limit_reached(logger):
    hourly_cache_key = __get_hourly_key()
    monthly_cache_key = __get_monthly_key()
    return __hourly_limit_reached(hourly_cache_key, logger) or __monthly_limit_reached(monthly_cache_key, logger)

def update_pc_miler_requests_count(logger):
    hourly_cache_key = __get_hourly_key()
    monthly_cache_key = __get_monthly_key()
    __update_hourly_requests_count(hourly_cache_key, logger)
    __update_monthly_requests_count(monthly_cache_key, logger)

def __hourly_limit_reached(hourly_cache_key, logger):
    limit_reached = False
    hourly_requests_count = distance_db_conn.get(hourly_cache_key)
    if hourly_requests_count:
        hourly_requests_count = int(hourly_requests_count)
        limit_reached = (hourly_requests_count >= app_config.PC_MILER_HOURLY_LIMIT)
    logger.debug(f'pc_miler_utils.__hourly_limit_reached - hourly_cache_key : {hourly_cache_key} has cached value: {hourly_requests_count}')
    return limit_reached

def __monthly_limit_reached(monthly_cache_key, logger):
    limit_reached = False
    monthly_requests_count = distance_db_conn.get(monthly_cache_key)
    if monthly_requests_count:
        monthly_requests_count = int(monthly_requests_count)
        limit_reached = (monthly_requests_count >= app_config.PC_MILER_MONTHLY_LIMIT)
    logger.debug(f'pc_miler_utils.__monthly_limit_reached - monthly_cache_key : {monthly_cache_key} has cached value: {monthly_requests_count}')
    return limit_reached

def __update_hourly_requests_count(hourly_cache_key, logger):
    hourly_requests_count = distance_db_conn.get(hourly_cache_key)
    updated_count = None
    if hourly_requests_count:
        hourly_requests_count = int(hourly_requests_count)
        updated_count = (hourly_requests_count + 1)
    else:
        updated_count = 1
    logger.debug(f'pc_miler_utils.__update_hourly_requests_count - hourly_cache_key : {hourly_cache_key} has cached value: {hourly_requests_count}')
    distance_db_conn.set(hourly_cache_key, updated_count)

def __update_monthly_requests_count(monthly_cache_key, logger):
    monthly_requests_count = distance_db_conn.get(monthly_cache_key)
    updated_count = None
    if monthly_requests_count:
        monthly_requests_count = int(monthly_requests_count)
        updated_count = (monthly_requests_count + 1)
    else:
        updated_count = 1
    logger.debug(f'pc_miler_utils.__update_monthly_requests_count - monthly_cache_key : {monthly_cache_key} has cached value: {monthly_requests_count}')
    distance_db_conn.set(monthly_cache_key, updated_count)

def __get_hourly_key():
    return pendulum.now().set(minute=0,second=0).format('MM-DD-YY HH:mm:ss')

def __get_monthly_key():
    return pendulum.now().format('MM-YY')
