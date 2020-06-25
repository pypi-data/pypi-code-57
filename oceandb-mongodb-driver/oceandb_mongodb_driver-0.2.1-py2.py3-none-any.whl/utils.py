#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging
from datetime import datetime, timedelta

import oceandb_mongodb_driver.indexes as index

logger = logging.getLogger(__name__)

AND = "$and"
OR = "$or"
GT = "$gte"
LT = "$lte"


def query_parser(query):
    query_result = {}
    for key, value in query.items():
        if 'cost' == key:
            create_cost_query(query, query_result)
        elif 'license' == key:
            create_query(query['license'], index.service_license, query_result, OR)
        elif 'categories' == key:
            create_query(query['categories'], index.categories, query_result, OR)
        elif 'tags' == key:
            create_query(query['tags'], index.tags, query_result, OR)
        elif 'service_type' == key:
            create_query(query['service_type'], index.service_type, query_result, AND)
        # Support older key for searching service type
        elif 'type' == key:
            create_query(query['type'], index.service_type, query_result, AND)
        elif 'metadata_type' == key:
            create_query(query['metadata_type'], index.metadata_type, query_result, AND)
        elif 'updateFrequency' == key:
            create_query(query['updateFrequency'], index.updated_frequency, query_result, OR)
        elif 'created' == key:
            create_created_query(query, query_result)
        elif 'dataToken' == key:
            create_query(query['dataToken'], index.dataToken, query_result, AND)
        elif 'sample' == key:
            query_result[index.sample] = 'sample'
        elif 'text' == key:
            create_text_query(query['text'], query_result)
        else:
            logger.error('The key %s is not supported by OceanDB.' % key[0])
            raise Exception('The key %s is not supported by OceanDB.' % key[0])
    return query_result


def create_query(values, index_name, query, operator):
    for i, value in enumerate(values):
        if i == 0 and operator not in query:
            query[operator] = [{index_name: value}]
        else:
            query[operator] += [{index_name: value}]
    return query


def create_cost_query(query, query_result):
    if len(query['cost']) > 2:
        logger.info('You are sending more values than needed.')
    elif len(query['cost']) == 0:
        logger.info('You are not sending any value.')
    elif len(query['cost']) == 1:
        query_result[index.cost] = {GT: 0, LT: query['cost'][0]}
    else:
        query_result[index.cost] = {GT: query['cost'][0], LT: query['cost'][1]}
    return query_result


def create_created_query(query, query_result):
    now = datetime.now() - timedelta(weeks=1000)
    for values in query['created']:
        if values == 'today':
            now = datetime.now() - timedelta(days=1)
        elif values == 'lastWeek':
            now = datetime.now() - timedelta(days=7)
        elif values == 'lastMonth':
            now = datetime.now() - timedelta(days=30)
        elif values == 'lastYear':
            now = datetime.now() - timedelta(days=365)
        else:
            logger.info('The key %s is not supported in the created query' % values)
    query_result['created'] = {GT: now}
    return query_result


def create_text_query(query, query_result):
    query_result['$text'] = {"$search": query[0]}
    return query_result
