import scrapy


class BaseItem(scrapy.Item):
    # 保存到mongo中的_id
    # _id = scrapy.Field()
    # 数据id，根据类型自动生成的
    data_id = scrapy.Field()
    # 任务id
    task_id = scrapy.Field()
    # 请求id
    request_id = scrapy.Field()
    insert_time = scrapy.Field()
