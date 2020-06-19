import os

from pymongo import MongoClient

from shangyun_scrapy_lib.constants.DictKey import DATA_ID


class MongoUtils:
    def __init__(self, db_name: str, col_name: str):
        self.mongo = MongoClient(
            host=os.environ.get('CRAWLAB_MONGO_HOST') or 'localhost',
            port=int(os.environ.get('CRAWLAB_MONGO_PORT') or 27017),
            username=os.environ.get('CRAWLAB_MONGO_USERNAME'),
            password=os.environ.get('CRAWLAB_MONGO_PASSWORD'),
            authSource=os.environ.get('CRAWLAB_MONGO_AUTHSOURCE') or 'admin'
        )
        self.db_name = db_name
        self.col_name = col_name
        self.db = self.mongo[db_name]
        self.col = self.mongo[db_name][col_name]
        self.index_list = []

    def create_index(self, name: str) -> bool:
        res = self.col.create_index([(name, 1)], name=name, unique=True)
        self.index_list = [index['name'] for index in self.col.list_indexes()]
        return res

    def exist_index(self, name):
        if len(self.index_list) == 0:
            self.index_list = [index['name'] for index in self.col.list_indexes()]

        return name in self.index_list


def ensure_index():
    unique_index = DATA_ID
    if not news_result.exist_index(unique_index):
        news_result.create_index(unique_index)
    if not comment_result.exist_index(unique_index):
        comment_result.create_index(unique_index)

    if not requests_relate.exist_index("_meta.request_id"):
        requests_relate.create_index("_meta.request_id")



db_name = os.environ.get('CRAWLAB_MONGO_DB') or 'crawlab_test'
col_name = os.environ.get('ERROR_LOGGER_COLLECTION') or 'scrapy_error'
task_error = MongoUtils(db_name, col_name)

# 关键任务的存储
col_name = os.environ.get('TASK_RELATE_COLLECTION') or 'scrapy_requests'
requests_relate = MongoUtils(db_name, col_name)

# 任务执行的统计
col_name = os.environ.get('STATISTIC_COLLECTION') or 'scrapy_statistic'
requests_statistic = MongoUtils(db_name, col_name)

# 存储新闻
col_name = os.environ.get('DATA_NEWS') or 'scrapy_news'
news_result = MongoUtils(db_name, col_name)

# 存储评论
col_name = os.environ.get('DATA_COMMENTS') or 'scrapy_comments'
comment_result = MongoUtils(db_name, col_name)

# 存储趋势
# col_name = os.environ.get('CRAWLAB_COLLECTION') or 'scrapy_trend'
# trend_result = MongoUtils(db_name, col_name)


# 确保每个数据存储的collection都有索引
ensure_index()

__all__ = [task_error, requests_relate, requests_statistic,
           news_result, comment_result, MongoUtils]

if __name__ == '__main__':
    # print(task_statistic.col.insert({"test": 123}))
    pass
