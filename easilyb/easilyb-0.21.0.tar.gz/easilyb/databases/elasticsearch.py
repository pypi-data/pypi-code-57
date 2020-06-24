import requests
import json
import logging
from urllib.parse import quote_plus
from easilyb.docker import elastic_instance, stop_container

KEY_ID = '_key_id'
logger = logging.getLogger(__name__)


class ElasticDB:
    def __init__(self, index_name="default", server_url=None, docker_server=False, container_name="default",
                 stop_at_exit=True, data_path=None):
        if docker_server:
            self.container_name = "easylib_elastic_" + container_name
            self.container, self.server_url = elastic_instance(self.container_name, data_path=data_path)
            if stop_at_exit:
                import atexit
                atexit.register(stop_container, self.container)
        else:
            self.server_url = server_url
        self.index_name = index_name
        self._init_db()

    def __getitem__(self, key):
        resp_data = self._es_request(requests.get, "/_doc/%s" % quote_plus(key))
        if "found" in resp_data and resp_data["found"]:
            return resp_data["_source"]
        else:
            return None

    def __setitem__(self, key, value):
        # if key is None:
        #     resp_data = self._es_request(requests.post, "/_doc/", json_data=value)
        value[KEY_ID] = key
        self._es_request(requests.put, "/_doc/%s" % quote_plus(key), json_data=value)

    def __delitem__(self, key):
        resp_data = self._es_request(requests.delete, "/_doc/%s" % quote_plus(key))
        if "result" in resp_data and resp_data['result'] == 'deleted':
            logger.debug("Deleted %s", key)
        else:
            logger.debug("Could not delete %s", key)

    def __contains__(self, key):
        return self.__getitem__(key) is not None

    def __len__(self):
        c = self.count()
        if c is None:
            raise Exception("Error getting index count")
        return c

    def __iter__(self):
        yield from self.scroll_search()

    def _es_request(self, method, uri, json_data=None, index_=True):
        if index_:
            url = self.server_url + '/' + self.index_name + uri
        else:
            url = self.server_url + uri
        try:
            resp = method(url, json=json_data)

            resp_data = json.loads(resp.text)
            if "error" in resp_data and "reason" in resp_data["error"]:
                logger.error("Error while requesting in %s index url=%s: %s", self.index_name, url,
                             _get_error_reason(resp_data['error']))
                if isinstance(resp_data['error'], dict) and 'reason' in resp_data['error'] \
                        and 'Limit of total fields' in resp_data['error']['reason']:
                    logger.error("Limit exceed error: resp_data=%s, json_data=%s", resp_data, json_data)
            return resp_data

        except:
            logger.error("Error while %sing in %s index url=%s", self.index_name, url, exc_info=True)
            raise

    def _init_db(self):
        url = self.server_url + '/' + self.index_name
        resp = requests.head(url)
        if resp.status_code == 404:
            print("Creating index:", self.index_name)
            # create index
            try:
                resp = requests.put(self.server_url + '/%s' % self.index_name)
                resp_data = json.loads(resp.text)
                if "error" in resp_data and "reason" in resp_data["error"]:
                    logger.warning("Elastic search error: %s", resp_data["error"]['reason'])
                if ("acknowledged" in resp_data and resp_data["acknowledged"]) \
                        or ("error" in resp_data and "type" in resp_data["error"]
                            and resp_data["error"]["type"] == "resource_already_exists_exception"):
                    logger.info("index '%s' created", self.index_name)
                else:
                    if "error" in resp_data and "reason" in resp_data["error"]:
                        raise Exception("Could not create %s index: %s", self.index_name, resp_data["error"]['reason'])
                    else:
                        raise Exception("Could not create %s index", self.index_name)
            except:
                logging.fatal("Error while creating %s index", self.index_name, exc_info=True)
                raise

            # TODO: mapping

    def count(self, q=None):
        if q is None:
            uri = "/_doc/_count"
        else:
            uri = "/_doc/_count?q=" + quote_plus(q)
        resp_data = self._es_request(requests.get, uri)
        if "count" in resp_data and resp_data:
            return resp_data["count"]
        else:
            logger.error("Could not get count for q=%s, resp_data=%s", q, resp_data)
            return None

    def bulk_requests(self, reqs):
        url = self.server_url + '/' + self.index_name + '/_bulk'

        response = requests.post(url, data='\n'.join([json.dumps(r) for r in reqs]) + '\n',
                                 headers={'content-type': 'application/json', 'charset': 'UTF-8'})

        return response

    def bulk_index(self, dict_obj):
        reqs = list()
        for k in dict_obj:
            dict_obj[k][KEY_ID] = k
            reqs.append({"index": {"_index": self.index_name, "_id": k}})
            reqs.append(dict_obj[k])
        return self.bulk_requests(reqs)

    def delete_by_query(self, query):
        uri = "/_delete_by_query?q=" + quote_plus(query)
        resp_data = self._es_request(requests.post, uri)
        return resp_data['deleted']

    def bulk_delete(self, keys):
        reqs = list()
        for k in keys:
            reqs.append({"delete": {"_index": self.index_name, "_id": k}})
        self.bulk_requests(reqs)

    def scroll_search(self, query=None, size=100, scroll="1m", sort=None):
        uri = "/_search?size=%d&scroll=%s" % (size, scroll)
        if query is not None:
            uri += "&q=%s" % quote_plus(query)
        if sort is not None:
            uri += "&sort=%s" % quote_plus(sort)

        resp_data = self._es_request(requests.get, uri)
        scroll_id = resp_data['_scroll_id']
        while "hits" in resp_data and "hits" in resp_data['hits'] and len(resp_data["hits"]['hits']) > 0:
            yield from [h['_source'] for h in resp_data['hits']['hits']]
            resp_data = self._es_request(requests.post,
                                         "/_search/scroll",
                                         json_data={'scroll': scroll, "scroll_id": scroll_id},
                                         index_=False)
        self._es_request(requests.delete, "/_search/scroll", json_data={"scroll_id": scroll_id}, index_=False)

    def search_after(self, query=None, size=100, sort='_doc'):
        uri = "/_search?size=%d" % size
        if query is not None:
            uri += "&q=%s" % quote_plus(query)
        if sort is not None:
            uri += "&sort=%s" % quote_plus(sort)

        resp_data = self._es_request(requests.get, uri)
        while "hits" in resp_data and "hits" in resp_data['hits'] and len(resp_data["hits"]['hits']) > 0:
            yield from [h['_source'] for h in resp_data['hits']['hits']]
            last_sort = resp_data['hits']['hits'][-1]['sort']
            resp_data = self._es_request(requests.get, uri, json_data={"search_after": last_sort})


def _get_error_reason(error):
    reason = ''
    if 'reason' in error:
        reason = error['reason']
    if 'caused_by' in error and 'reason' in error['caused_by']:
        reason += ', caused by: ' + error['caused_by']['reason']
    if reason.startswith(', caused by: '):
        reason = reason[len(', caused by: '):]
    if reason == '':
        reason = repr(error)
    reason += '.'
    return reason
