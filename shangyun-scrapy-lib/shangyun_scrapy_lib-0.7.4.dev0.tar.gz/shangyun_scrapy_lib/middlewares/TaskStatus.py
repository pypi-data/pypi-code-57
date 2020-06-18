import traceback

from scrapy import Spider, Request
from scrapy.http import Response

from shangyun_scrapy_lib.constants.DictKey import REQUEST_ID
from shangyun_scrapy_lib.utils.Serialize import request_serialize

from shangyun_scrapy_lib.constants import TaskStatus
from shangyun_scrapy_lib.utils.MongoUtils import requests_relate, task_error


class TaskStatusSpiderMiddleware(object):
    """
    给每个结果生成一个uuid，
    """

    def process_start_requests(self, start_requests, spider: Spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            if isinstance(r, Request):
                r.meta["status"] = TaskStatus.not_run
                _update_status(r)
            yield r

    def process_spider_output(self, response: Response, result, spider: Spider):
        # def set_status(res):
        #     if isinstance(res, Request):
        #         res.meta["status"] = TaskStatus.not_run
        #         _update_status(res)
        #     return res

        if response.request:
            r: Request = response.request
            r.meta["status"] = TaskStatus.success
            _update_status(r)

        # return [set_status(res) for res in result or ()]
        return result

    def process_spider_exception(self, response: Response, exception, spider):
        error_info = {
            "error": traceback.format_exc(),
            "request": request_serialize(response.request),
            "type": "spider"
        }
        task_error.col.save(error_info)
        # 通过id更新task状态r
        if response.request:
            r: Request = response.request
            r.meta["status"] = TaskStatus.parse_error
            _update_status(r)



class TaskStatusDownloaderMiddleware(object):
    def process_request(self, request: Request, spider):
        request.meta["status"] = TaskStatus.running
        _update_status(request)
        return request


    def process_exception(self, request: Request, exception: Exception, spider):
        # 保存错误信息
        error_info = {
            "error": traceback.format_exc(),
            "request": request_serialize(request),
            "type": "download"
        }
        task_error.col.save(error_info)
        # 更新task状态
        request.meta["status"] = TaskStatus.download_error
        _update_status(request)


def _update_status(r: Request):
    _id = r.meta.get(REQUEST_ID)
    if not _id:
        return
    requests_relate.col.update_one({"_meta.request_id": _id}, {"$set": {"_meta.status": r.meta.get("status")}})

