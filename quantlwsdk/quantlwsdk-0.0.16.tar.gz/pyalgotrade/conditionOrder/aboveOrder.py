# -*- coding: utf-8 -*-
#
'''

本模块，针对第三方账户系统。即账户系统 由掘金或者其他平台提供。账户的持仓等字段，不由自己维护，由他们维护

'''
import time

from pyalgotrade import gm3HelpBylw
from functools import partial

from pyalgotrade.utils import id_gen
from pyalgotrade import observer
from pyalgotrade.const import ORDER_TYPE,ORDER_STATUS,STOP_PROFIT_LOSS_ORDER_STATUS,POSITION_SIDE

import abc


from pyalgotrade.conditionOrder.base_conditionOrder import BaseConditionOrder




#针对多头持仓，高于某个价格就出场，针对空头，低于某个价格就出场。相当于止盈了。
class AboveOrder(BaseConditionOrder):


    def __init__(self,price,target_order_position,order_type=2):

        self.price=price
        super(AboveOrder, self).__init__(target_order_position,order_type=order_type)

        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
    def _prePareMsg(self):
        # 持仓是多头还是空头

        if self.target_order_position.getPositionSide() == 1:
            self._signalName = 'above-cLong'


        if self.target_order_position.getPositionSide() == 2:
            self._signalName = 'above-cShort'

    def getOrderInfo(self):
        infodict={}
        infodict['symbol']=self._targetSymbol


        infodict['status'] = self._status
        infodict['posiNum'] = self.target_order_position.getVolume()
        infodict['positionSide'] = self.target_order_position.getPositionSide()

        return  infodict
    def on_tick_hq(self, tick_, context=None):

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.getPositionSide() == 2:
                # if self._side==OrderSide_Buy:
                if tick_.price <= self.price:

                    if self._order_type == 2:
                        gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog)
                    if self._order_type == 1:
                        gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog,price=self.price)

                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

            if self.target_order_position.getPositionSide() == 1:
                # if self._side==OrderSide_Sell:
                if tick_.price >= self.price:

                    if self._order_type == 2:
                        gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog)
                    if self._order_type == 1:
                        gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog,price=self.price)




                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

    def on_bar_hq(self, bar_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.getPositionSide() == 2:
                # if self._side==OrderSide_Buy:
                if bar_.low <= self.price:
                    if self._order_type == 2:
                        gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog)
                    if self._order_type == 1:
                        gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog, price=self.price)

                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)






            if self.target_order_position.getPositionSide()  == 1:
                # if self._side==OrderSide_Sell:
                if bar_.high >= self.price:
                    if self._order_type == 2:
                        gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog)
                    if self._order_type == 1:
                        gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'), context=context,
                                                     orderLog=context.orderLog, price=self.price)

                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


