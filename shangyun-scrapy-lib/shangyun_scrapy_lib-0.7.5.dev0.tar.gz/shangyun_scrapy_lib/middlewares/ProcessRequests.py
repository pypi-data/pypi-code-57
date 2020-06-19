import hashlib
import logging
import time
from datetime import datetime

import scrapy
from scrapy import Spider, Request
from scrapy.http import Response

from shangyun_scrapy_lib.constants import DataType, TaskStatus
from shangyun_scrapy_lib.constants.DictKey import REQUEST_ID, PARENT_ID, INSERT_TIME, DATA_ID
from shangyun_scrapy_lib.utils.MongoUtils import requests_relate

from shangyun_scrapy_lib.utils.Serialize import request_serialize

logger = logging.getLogger(__name__)


class ProcessRequestsMiddleware(object):
    """
    处理请求
    """

    def request_id(self, spider: Spider, r: Request):
        if r.method == "GET":
            request_md5 = md5(r.url)
        else:
            request_md5 = md5(r.url + str(r.body))
        return f"{spider.name}-{request_md5}"

    def data_id(self, res, name):
        media_type = res.get("media_type")
        if media_type == DataType.NEWS:
            id = res.get("news_id")
        elif media_type == DataType.COMMENT:
            id = res.get("comment_id")
        else:
            return f"{media_type}-{name}"

        return f"{media_type}-{name}-{id}"


    def process_start_requests(self, start_requests, spider: Spider):
        for r in start_requests:
            if isinstance(r, Request):
                r.meta[REQUEST_ID] = self.request_id(spider, r)
                r.meta[INSERT_TIME] = datetime.now()
                update_request(r)
            yield r

    def process_spider_output(self, response: Response, result, spider: Spider):
        name = spider.name
        # 关联父请求
        p_request: Request = response.request
        if not p_request.meta.get(REQUEST_ID):
            logger.warning("the parent request has not id")

        def process_request(res):
            res.meta["status"] = TaskStatus.not_run
            # todo 以后补充，请求为GET或POST的情况，生成不同的ID
            res.meta[REQUEST_ID] = self.request_id(spider, res)
            # 关联父请求
            res.meta[PARENT_ID] = p_request.meta.get(REQUEST_ID) or ""
            res.meta[INSERT_TIME] = datetime.now()
            update_request(res)
            return res

        def process_item(res):
            # 生成数据id
            res[DATA_ID] = self.data_id(res, name)
            return res

        def handle(res):
            if isinstance(res, dict) or isinstance(res, scrapy.Item):
                return process_item(res)
            elif isinstance(res, Request):
                return process_request(res)
            return res

        return [handle(res) for res in result or ()]


def update_request(request: Request):
    return requests_relate.col.find_one_and_update(
        {"url": request.url},
        {"$set": request_serialize(request)},
        upsert=True
    )


def md5(string: str):
    h1 = hashlib.md5()
    h1.update(string.encode("utf8"))
    return h1.hexdigest()
