import redis


# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:items'

BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'
# Sane connection defaults.
REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'shangyun_scrapy_lib.scrapy_redis.queue.PriorityQueue'
SCHEDULER_DELAY_QUEUE_KEY = '%(spider)s:updateRequests'
SCHEDULER_DELAY_QUEUE_CLASS = 'shangyun_scrapy_lib.scrapy_redis.queue.DelayQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'shangyun_scrapy_lib.scrapy_redis.dupefilter.RFPDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False
