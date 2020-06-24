import logging
import sys
import uuid
from typing import Text

from django.conf import settings
from django.db import connection
from isc_common.common import blinkString

logger = logging.getLogger(__name__)


def create_tmp_mat_view(sql_str, params=[], indexes=[], mat_view_name=None) -> Text:
    if mat_view_name != None:
        settings.LOCKS.acquire(f'create_tmp_mat_view_{mat_view_name}')
    else:
        mat_view_name = f'tmp_{str(uuid.uuid4()).replace("-", "_")}'

    if isinstance(indexes, list):
        indexes = [f'''CREATE INDEX {mat_view_name}_{index}_idx ON {mat_view_name} USING btree ("{index}")''' for index in indexes]
        suffix = ';'.join(indexes)
    sql_txt = f'''CREATE MATERIALIZED VIEW {mat_view_name} AS {sql_str} WITH DATA; {suffix}'''
    try:
        with connection.cursor() as cursor:
            logger.debug(f'Creating: {mat_view_name}')
            cursor.execute(sql_txt, params)
            logger.debug(f'Created: {mat_view_name}')
        if mat_view_name != None:
            settings.LOCKS.release(f'create_tmp_mat_view_{mat_view_name}')
        return mat_view_name
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        if mat_view_name != None:
            settings.LOCKS.release(f'create_tmp_mat_view_{mat_view_name}')
        return None


def create_view(sql_str, params=[], view_name=None) -> None:
    if view_name == None:
        raise Exception(f'View must have name/')
    settings.LOCKS.acquire(f'createt_view_{view_name}')

    sql_txt = f'''DROP VIEW IF EXISTS {view_name} CASCADE;'''
    sql_txt += f'''CREATE VIEW {view_name} AS {sql_str};'''
    try:
        with connection.cursor() as cursor:
            logger.debug(f'Creating: {view_name}')
            cursor.execute(sql_txt, params)
            logger.debug(f'Created: {view_name}')
        settings.LOCKS.release(f'createt_view_{view_name}')
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'createt_view_{view_name}')


def create_tmp_table(fields_str=None, sql_str=None, on_commit='delete rows', params=[], indexes=[], unique_indexes=[], table_name=None, drop=True) -> None:
    if table_name == None:
        raise Exception(f'Table must have name/')
    settings.LOCKS.acquire(f'create_tmp_table{table_name}')

    indexes_str = ''
    if isinstance(indexes, list):
        indexes = [f'''CREATE INDEX {table_name}_{index}_idx ON {table_name} USING btree ("{index}")''' for index in indexes]
        indexes_str = ';'.join(indexes)

    unique_indexes_str = ''
    if isinstance(unique_indexes, list):
        indexes = [f'''CREATE INDEX {table_name}_{index[0]}_idx ON {table_name} USING btree ("{index[0]}") WHERE ({index[1] if index[1] else "1=1"});''' for index in unique_indexes]
        unique_indexes_str = ';'.join(indexes)

    sql_txt = ''
    if drop:
        sql_txt = f'''DROP table IF EXISTS {table_name} CASCADE;'''

    on_commit_str = f'ON COMMIT {on_commit}'
    if on_commit == None:
        on_commit_str = ''

    if sql_str == None:
        sql_txt += f'''CREATE TEMPORARY TABLE {table_name} ({fields_str}) {on_commit_str};'''
    else:
        sql_txt += f'''CREATE TEMPORARY TABLE {table_name} as ({sql_str}); {on_commit_str};'''
    sql_txt += indexes_str
    sql_txt += unique_indexes_str

    try:
        with connection.cursor() as cursor:
            logger.debug(f'Creating: {table_name}')
            cursor.execute(sql_txt, params)
            logger.debug(f'Created: {table_name}')
        settings.LOCKS.release(f'create_tmp_table{table_name}')
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'create_tmp_table{table_name}')


def drop_mat_view(mat_view_name) -> bool:
    sql_txt = f'DROP MATERIALIZED VIEW IF EXISTS {mat_view_name} CASCADE;'
    try:
        settings.LOCKS.acquire(f'drop_mat_view_{mat_view_name}')
        with connection.cursor() as cursor:
            logger.debug(f'Droping: {mat_view_name}')
            cursor.execute(sql_txt)
        settings.LOCKS.release(f'drop_mat_view_{mat_view_name}')
        logger.debug(f'Droped: {mat_view_name}')
        return True
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'drop_mat_view_{mat_view_name}')
        return False


def refresh_mat_view(mat_view_name, progressStack=None):
    sql_txt = f'REFRESH MATERIALIZED VIEW {mat_view_name};'
    settings.LOCKS.acquire(f'refresh_mat_view_{mat_view_name}')
    try:
        with connection.cursor() as cursor:
            if progressStack != None:
                progressStack.setContentsLabel(blinkString(f'Обновление материализованного преставления {mat_view_name}', bold=True))
            cursor.execute(sql_txt)
        settings.LOCKS.release(f'refresh_mat_view_{mat_view_name}')
        if progressStack != None:
            progressStack.close()
        return True
    except Exception as ex:
        exc_info = sys.exc_info()
        logger.error(msg=ex, exc_info=exc_info)
        settings.LOCKS.release(f'refresh_mat_view_{mat_view_name}')
        if progressStack != None:
            progressStack.close()
        return False
