# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import  copy
from pyalgotrade.const import ORDER_TYPE,ORDER_STATUS,STOP_PROFIT_LOSS_ORDER_STATUS,POSITION_SIDE
from pyalgotrade import observer
from pyalgotrade.tradeBylw import cusTrade
from pyalgotrade.orderBylw import cusOrder
FRE__NAME_MAP_STR={
    '1d': '1d',

    '60min': str(60 * 60) + 's',
    '30min':str(30*60)+'s',
    '1min':str(1*60)+'s',
    '5min':str(5*60)+'s',


    '60分钟':str(60*60)+'s',
    '30分钟': str(30 * 60) + 's',
    '1分钟':str(1*60)+'s',
    '3分钟':str(3*60)+'s',
    '5分钟':str(5*60)+'s',
    '15分钟':str(15*60)+'s',
}



def get_change_percentage(actual, prev):
    if actual is None or prev is None or prev == 0:
        raise Exception("Invalid values")

    diff = actual-prev
    ret = diff / float(abs(prev))
    return ret


def safe_min(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)


def safe_max(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return max(left, right)


def id_gen(start=1):
    i = start
    while True:
        yield i
        i += 1


def parseToGmFre(freName):
    return FRE__NAME_MAP_STR[freName]

def freMapFromGM(gmFreStr):
    return int(gmFreStr[:-1])



#这个类 是因为掘金的订阅，只有品种，没有频率。
#比如我每日盘前，先清除所有订阅，就没法清除，因为掘金只是记录了订阅品种，没有记录订阅品种的频率。
class subScribeSeqCollection:
    def __init__(self):
        self.seq=set()
        self.outerSubFun = observer.Event()  # 外部接口用来订阅行情的函数都放在这里。
        self.outerUnSubFun = observer.Event()  # 外部接口用来退订行情的函数都放在这里。

    def getOuterSubFunEvent(self):
        return self.outerSubFun
    def getOuterUnSubFunEvent(self):
        return self.outerUnSubFun
    def add(self,symbol,fre):
        if (symbol,fre) not in self.seq:
            self.outerSubFun.emit(symbol,fre)
        self.seq.add((symbol,fre))
    def remove(self,symbol,fre):
        self.outerUnSubFun.emit(symbol, fre)
        self.seq.remove((symbol,fre))


    def getFreSet(self,fre):

        aset=set()
        for aTupel in self.seq:
            if aTupel[1]==fre:
                aset.add(aTupel)

        return aset

    def getNonFreSet(self,fre):
        sSet=self.getFreSet(fre)

        return self.seq.difference(sSet)

    def removeFreSet(self,freSet):
        aset = copy.deepcopy(self.seq)

        for fre in freSet:
            for aTupel in aset:
                if aTupel[1]==fre:
                    self.seq.remove(aTupel)
    def removeAll(self):
        for sym,fre in self.seq:
            self.outerUnSubFun.emit(sym, fre)
        self.seq.clear()

    #即用外部的set，置换掉内部同频率的set
    #比如原来内部是rb1910 30min,现在进来个i2001 30min,那么就是要剔除掉rb1910 30min，添加进来i2001 30min
    def updateFreSet(self,outset):

        freset=set()
        for aoutvar in outset:
            fre=aoutvar[1]
            freset.add(fre)

        self.removeFreSet(freset)
        self.seq.update(outset)

        #


def createTradeRecordFromGmorder(gmorder):
    # if gmorder.status == 3:
    # 利用掘金的回测的order对象。来构造一个trade记录
    tradedict = {}
    tradedict['symbol'] = gmorder.symbol
    tradedict['orderID'] = gmorder.cl_ord_id
    tradedict['side'] = gmorder.side
    tradedict['position_effect'] = gmorder.position_effect
    tradedict['volume'] = gmorder.volume
    tradedict['price'] = gmorder.price
    tradedict['commission'] = 0
    tradedict['tax'] = 0
    return tradedict


def createCusPositionFromGmPosition(gmPosition):

    aorderPosition = cusHoldingPostion()
    # if gmPosition.side==1:
    #     aorderPosition.positionSide= 1
    # if gmPosition.side==2:
    #     aorderPosition.positionSide= 2
    #即1为多头，2为空头
    aorderPosition.positionSide=gmPosition.side

    aorderPosition.symbol= gmPosition.symbol
    aorderPosition.volume = gmPosition.volume
    aorderPosition.vwap = gmPosition.vwap

    aorderPosition.created_at = gmPosition.created_at
    aorderPosition.updated_at = gmPosition.updated_at
    return aorderPosition


def createCusOrderFromGmOrder(gmOrder):

    aorder = cusOrder(gmOrder.order_id,gmOrder.symbol,gmOrder.side,gmOrder.position_effect,\
                      gmOrder.price,gmOrder.volume,gmOrder.created_at)
    aorder.setUpdateTime(gmOrder.updated_at)
    return aorder

def createCusTradeFromGmTrade(gmTrade):
    aTrade = cusTrade(gmTrade.exec_id,gmTrade.symbol,gmTrade.side,gmTrade.position_effect,gmTrade.price,gmTrade.volume,gmTrade.created_at)
    # # if gmTrade.side == 1:
    # #     aTrade.side = 1
    # # if gmTrade.side == 2:
    # #     aTrade.side = 2
    # aTrade.side=gmTrade.side
    # aTrade.positionEffect = gmTrade.position_effect
    # aTrade.price=gmTrade.price
    # aTrade.commission=gmTrade.commission
    # # aTrade.positionSide = gmTrade.side
    # aTrade.symbol = gmTrade.symbol
    # aTrade.volume = gmTrade.volume
    #
    # aTrade.created_at = gmTrade.created_at

    return aTrade

#我自定以的持仓方向 是一个enum形式，有时候要转成掘金的形式
def cusPositionSideToGMPositionSide(side_):
    if side_ == POSITION_SIDE.LONG:
        gmside = 1
    if side_ == POSITION_SIDE.SHORT:
        gmside = 2
    return gmside



# class cusOrder():
#
#     def __init__(self):
#         self.symbol = None
#         self.positionSide = None
#
#         self.side=None #买还是卖
#         self.positionEffect=None #开仓还是平仓
#
#
#         self.volume = None
#
#
#         # 这2个时间限制为datetime形式。
#         self.created_at = None
#         self.updated_at = None


    # @property
    # def barsSinceEntry(self):
    #     return self.__barsSinceEntry
    #
    # @barsSinceEntry.setter
    # def barsSinceEntry(self, value):
    #     if not isinstance(value, int):
    #         raise ValueError('value must be an integer!')
    #     # if value < 0 or value > 100:
    #     #     raise ValueError('score must between 0 ~ 100!')
    #     self.__barsSinceEntry = value

#
# def create_stop_loss_order_fromGmOrders(gmOrderObj,stopLossThresh,simuBroker4StopLossProfit):
#
#
#     tradeo = tradeOrder(gmOrderObj.cl_ord_id, gmOrderObj.symbol, gmOrderObj.volume, \
#                                       gmOrderObj.side, ORDER_TYPE.MARKET, gmOrderObj.position_effect)
#     simuBroker4StopLossProfit.addTradeOrder(tradeo)
#
#
#     # o = stop_loss_by_order(tradeo, 'percent', stopLossThresh)
#     # simuBroker4StopLossProfit.addStopLossOrder(o)
#
#     # #在掘金的回测环境中。直接委托就成交了。这种情况下，需要变更下tradeorder的状态
#     if gmOrderObj.status==3:
#
#         #利用掘金的回测的order对象。来构造一个trade记录
#         tradedict = {}
#         tradedict['volume'] = gmOrderObj.filled_volume
#         tradedict['price'] = gmOrderObj.filled_vwap
#         tradedict['commission'] = gmOrderObj.filled_commission
#         tradedict['tax'] = 0
#         # tradeo.fill(tradedict)
#
#         simuBroker4StopLossProfit.onTrade(tradedict)
#
#
