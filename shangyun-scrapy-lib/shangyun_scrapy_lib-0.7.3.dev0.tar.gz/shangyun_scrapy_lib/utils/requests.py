import time

from scrapy import Request

from shangyun_scrapy_lib.utils import default


class UpdateRequest(Request):
    update = True

    def __init__(self, *args, **kwargs):
        super(UpdateRequest, self).__init__(*args, **kwargs)
        self.dont_filter = True

        # 下一次更新时间
        default_time = int(time.time() + default.update_interval)
        self.next_time = kwargs.get("next_time", default_time)
        self.meta.update({"type": "update"})


class NewsRequest(Request):

    def __init__(self, *args, **kwargs):
        super(NewsRequest, self).__init__(*args, **kwargs)
        self.meta.update({"type": "news"})


class CommentRequest(Request):

    def __init__(self, *args, **kwargs):
        super(CommentRequest, self).__init__(*args, **kwargs)
        self.meta.update({"type": "comment"})
