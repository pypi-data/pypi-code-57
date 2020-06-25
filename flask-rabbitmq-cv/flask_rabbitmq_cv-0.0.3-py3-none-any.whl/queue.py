# encoding:utf-8
from . import ExchangeType

class Queue():

    def __init__(self):
        self._rpc_class_list = []

    def __call__(self, queue=None, type = ExchangeType.DEFAULT, exchange = '', routing_key = '', durable = False, auto_delete = True):
        """
        当Queue对象被调用时，如@queue()执行的操作
        :param queue_name: 队列名
        :param type: 交换机的类型
        :param exchange_name:
        :param routing_key:
        :param durable:
        :param auto_delete:
        :return:
        """
        def _(func):
            self._rpc_class_list.append((type, queue, exchange, routing_key, durable, auto_delete, func))
        return _