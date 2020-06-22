# -*- coding: utf-8 -*-
"""
20200410 lw

"""
from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday


import pymongo
from datetime import timezone
from datetime import timedelta

from pyalgotrade.positionHelpBylw import Positions, cusHoldingPostion



class memoryAccount():
    def __init__(self, positions):
        self._positions=positions

    def ontrade(self, gmTrade):
        symbol_ = gmTrade.getSymbol()
        targetPositionSide = gmTrade.getTargetPositionSide()



        self._positions.get_or_create(symbol_,targetPositionSide).ontrade(gmTrade)
        self.clearZeroRecord()

        #每次positions ontrade 之后，其内部可能持仓没了，没了的话，要很快清楚掉，否则持仓的创建时间就会更新的有问题。

    #将positions中 为0持仓的positon都删除掉
    def clearZeroRecord(self):

        listKey=list(self._positions.keys())
        listKey=listKey.copy()
        for key in listKey:
            if self._positions[key].getVolume()==0:
                del self._positions[key]

        i=1


def _prePareMemAccout(context):
    # 每次启动的时候，从数据库读取修交易记录，从而得到具体的持仓。

    positionsObj = Positions(cusHoldingPostion)
    cusAccout = memoryAccount(positionsObj)

    monTradeObj = mongoTrade(config.tradeDbName, config.tradeCollectionName, host=config.tradeDbHost)
    allstrade = monTradeObj.getAllTrades()

    for atrade in allstrade:
        cusAccout.ontrade(atrade)
    context.cusAccout=cusAccout