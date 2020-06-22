# -*- coding: utf-8 -*-
"""
20200410 lw

"""

import pandas as pd
import pymongo
from pyalgotrade.utils import gmEnum
from pyalgotrade import calendayBylw
import datetime
from datetime import  timezone,timedelta
import re

# from pyalgotrade.positionHelpBylw import Positions, cusHoldingPostion
#



class cusTrade():

    def __init__(self,tradeId,symbol,side,positionEffect,price,volume,datetime):
        self._tradeid=tradeId
        self._symbol = symbol
        # self.positionSide = None

        self._side = side  # 买还是卖
        self._positionEffect = positionEffect  # 开仓还是平仓


        self._price=price #此次成交的成交价格。
        self._volume = volume  #此次成交的 数量
        # self.commission=None #此次成交 缴纳的手续费

        # 这2个时间限制为datetime形式。要带上时区
        self._created_at = datetime

        self._targetPositionSide=self._calPositionSide()
     #根据trade 描述出，改交易针对的是多头持仓，还是空头持仓
    def _calPositionSide(self):
        if self._positionEffect in [gmEnum.PositionEffect_Close, gmEnum.PositionEffect_CloseToday,
                                         gmEnum.PositionEffect_CloseYesterday]:

            # 本次平仓的成交完成了，需要取查 该持仓是否 还在，如果不在了，就要剔除相关止盈止损指令等。

            side_ = self._side
            if side_==1: #买平，表明针对空头持仓
                gmPos_=2
            if side_==2: #卖平，表明针对多头持仓
                gmPos_=1
        if self._positionEffect  in [gmEnum.PositionEffect_Open]:
            side_ = self._side   #买方向是1，卖方向是2，掘金中 多头方向也是1，空头方向也是2
            gmPos_=side_

        return gmPos_


    def getSymbol(self):
        return self._symbol
    def getSide(self):
        return self._side
    def getPositionEffect(self):
        return self._positionEffect
    def getPrice(self):
        return self._price
    def getVolume(self):
        return self._volume
    def getTradeTime(self):
        return self._created_at

    def setTradeTime(self,dt):
        self._created_at=dt

    def getTargetPositionSide(self):
        return self._targetPositionSide

    #ctp返回的czce和dce交易所的成交日期 都是用的交易日，不是实际的成交日期。所以这里设置一个函数，来调整日期。
    def adjustTradeTime_CZCEDCEReason(self):
        from pyalgotrade import calendayBylw
        aNewTradeCalendar = calendayBylw.getACalendarInstance()
        currDt=self._created_at.astimezone(timezone(timedelta(hours=8)))
        dtstr=currDt.strftime('%Y-%m-%d %H:%M:%S')
        realDt = aNewTradeCalendar.getRealDateTime(self._symbol, dtstr[0:10], dtstr[11:])
        self._created_at=datetime.datetime.strptime(realDt, '%Y-%m-%d %H:%M:%S')


class cusOrder():

    def __init__(self,orderId,symbol,side,positionEffect,price,volume,created_at):
        self._orderId = orderId
        self._symbol = symbol
        self.positionSide = None

        self._side=side #买还是卖
        self._positionEffect=positionEffect #开仓还是平仓

        self._price=price  #委托价格
        self._volume = volume



        # 这2个时间限制为datetime形式。 委托创建时间和委托更新时间
        self._created_at = created_at
        self._updated_at = created_at



        self._filled_volume=0

        self._targetPositionSide = self._calPositionSide()

    def getSymbol(self):
        return self._symbol

    def getSide(self):
        return self._side

    def getPositionEffect(self):
        return self._positionEffect

    def getPrice(self):
        return self._price

    def getVolume(self):
        return self._volume

    def getTradeTime(self):
        return self._created_at
    def getUpdateTime(self):
        return self._updated_at

    def setUpdateTime(self,dt):
        self._updated_at=dt
    def setTradeTime(self, dt):
        self._created_at = dt

    def _calPositionSide(self):
        if self._positionEffect in [gmEnum.PositionEffect_Close, gmEnum.PositionEffect_CloseToday,
                                         gmEnum.PositionEffect_CloseYesterday]:

            # 本次平仓的成交完成了，需要取查 该持仓是否 还在，如果不在了，就要剔除相关止盈止损指令等。

            side_ = self._side
            if side_==1: #买平，表明针对空头持仓
                gmPos_=2
            if side_==2: #卖平，表明针对多头持仓
                gmPos_=1
        if self._positionEffect  in [gmEnum.PositionEffect_Open]:
            side_ = self._side   #买方向是1，卖方向是2，掘金中 多头方向也是1，空头方向也是2
            gmPos_=side_

        return gmPos_


    def getTargetPositionSide(self):
        return self._targetPositionSide
