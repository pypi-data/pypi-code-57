# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import
import six

#lw  从gm中引入过来的。为了positions
from pyalgotrade.broker.enum import PositionSide_Long, PositionSide_Short



'''
该文件是从掘金中 拷贝过来的。pyalgotrade的原始代码中，并没有账户类。缺少很多东西。
我在这里补起来，特别是补充 cash 和 position（持仓这两个东西）

注意，pyalgotrrae中，有position这个模块，但是其 是用来 标记策略的 开仓委托和平仓委托的，
和我们平时的 认为当前的holding 不一样。

这里的position 就是holding的意思。


'''
# 账户
class Account(object):
    def __init__(self, id, name, cash =0):
        self.id = id
        self.name = name
        self.cash = cash
        self.inside_positions = {}


    def addCash(self,cashNum):
        self.cash = self.cash + cashNum

    def setCash(self,cashNum):
        self.cash = cashNum


    def match(self, name):
        if self.name == name:
            return True

        if self.id == name:
            return True

    def positions(self, symbol='', side=None):
        # 默认返回全部
        if not symbol and not side:
            info = list(six.itervalues(self.inside_positions))
            return info

        # 只有side 返回空仓和多仓
        if not symbol and side:
            info = list(six.itervalues(self.inside_positions))
            return [i for i in info if i.get('side') == side]

        # 只有symbol 没有side 返回固定symbol的空仓和多仓
        if symbol and not side:
            long_key = '{}.{}'.format(symbol, PositionSide_Long)
            long_info = self.inside_positions.get(long_key)

            short_key = '{}.{}'.format(symbol, PositionSide_Short)
            short_info = self.inside_positions.get(short_key)

            result = []
            if long_info:
                result.append(long_info)
            if short_info:
                result.append(short_info)
            return result

        # 返回指定仓位
        key = '{}.{}'.format(symbol, side)
        info = self.inside_positions.get(key)
        if not info:
            return []

        return [info]

    def position(self, symbol, side):
        key = '{}.{}'.format(symbol, side)
        return self.inside_positions.get(key)
