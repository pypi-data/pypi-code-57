from scrapy import Spider
from scrapy.http import Response
import logging

from shangyun_scrapy_lib.utils.requests import UpdateRequest

logger = logging.getLogger(__name__)


class UpdateSpiderMiddleware(object):
    """
    当处理完结果时，判断是否需要进行自动更新的处理
    """

    def __init__(self, update_limit, stats, verbose_stats=False, prio=1):
        self.update_limit = update_limit
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        update_limit = settings.getint('UPDATE_LIMIT')
        verbose = settings.getbool('UPDATE_STATS_VERBOSE')
        prio = settings.getint('UPDATE_PRIORITY')
        return cls(update_limit, crawler.stats, verbose, prio)

    def process_spider_output(self, response: Response, result, spider: Spider):
        def _filter(request):
            # 这个是要拦截什么东西来着。。。忘了。。。。
            # if response.meta.get("update", 0) > 0:
            #     return False

            if isinstance(request, UpdateRequest):
                update = response.meta['update'] + 1
                request.meta['update'] = update
                if self.prio:
                    request.priority -= update * self.prio
                if self.update_limit and update > self.update_limit:
                    logger.debug(
                        "Ignoring link (depth > %(maxupdate)d): %(requrl)s ",
                        {'maxupdate': self.update_limit, 'requrl': request.url},
                        extra={'spider': spider}
                    )
                    return False
                else:
                    if self.verbose_stats:
                        self.stats.inc_value('request_update_count', spider=spider)
                        # self.stats.inc_value('request_update_count/%s' % update, spider=spider)
                    self.stats.max_value('request_update_max', update, spider=spider)
            return True

        # base case (depth=0)
        if 'update' not in response.meta:
            response.meta['update'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_update_count', spider=spider)

        return (r for r in result or () if _filter(r))
