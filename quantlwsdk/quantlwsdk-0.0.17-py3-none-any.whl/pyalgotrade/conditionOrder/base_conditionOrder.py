# -*- coding: utf-8 -*-
#
'''

本模块，针对第三方账户系统。即账户系统 由掘金或者其他平台提供。账户的持仓等字段，不由自己维护，由他们维护

'''
import time


from pyalgotrade.utils import id_gen
from pyalgotrade import observer
from pyalgotrade.const import ORDER_TYPE,ORDER_STATUS,STOP_PROFIT_LOSS_ORDER_STATUS,POSITION_SIDE
from functools import partial
from pyalgotrade import gm3HelpBylw
import abc






class BaseConditionOrder():
    order_id_gen = id_gen(int(time.time()) * 10000)

    def __init__(self,target_order_position,order_type=2):
        self._order_id = next(BaseConditionOrder.order_id_gen)
        # self.orderLog=None  日志都是带有时间的，条件单的日志，可能前几日 建立的，但是呢要今天才会触发，所以不适合日志是固定的。必须随时从外界传入
        self.target_order_position = target_order_position
        self._targetSymbol = target_order_position.getSymbol()


        self._order_type=order_type



        self._signalName=None
        self._status = None

        self.orderInvalidEvent = observer.Event() #用来退订tick行情的函数会在这里。

        self.init_excute_fun()


    def getOrderInvalidEvent(self):
        return self.orderInvalidEvent
    def setStatus(self,status):
        self._status=status
        if self.is_final():
            self.orderInvalidEvent.emit(self._targetSymbol)

    # def getSymbol(self):
    #     return self.target_order_position

    def getSymbol(self):
        return self._targetSymbol
    def getOrderPositionObj(self):
        return self.target_order_position
    # def getOrderInfo(self):
    #     infodict={}
    #     infodict['symbol']=self._targetSymbol
    #     infodict['cost'] = self._target_posi_cost
    #     infodict['clearPrice'] = self._clear_price
    #     infodict['status'] = self._status
    #     infodict['posiNum'] = self.target_order_position.getVolume()
    #
    #     return  infodict

    @abc.abstractmethod
    def getOrderInfo(self):
        raise NotImplementedError()

    #orderType=1表示限价单，orderType=2表示市价委托




#没有用init_excute_fun 抽象的原因是，clearprice有可能不是刚创建就能知道的，可能会随这tick来了才知道。
    #当然也可以在这里不封装进去clearprice，但是我 还是选择这里不封装init_excute_fun，让具体的条件单去处理似乎也行。

    # @abc.abstractmethod
    # def _prePareMsg(self):
    #     raise NotImplementedError
    @abc.abstractmethod
    def _prePareMsg(self):
        raise NotImplementedError
    def init_excute_fun(self):
        self._prePareMsg()

        # 持仓是多头还是空头
        if self.target_order_position.getPositionSide() == 1:

            if self._order_type == 2:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName)
            if self._order_type == 1:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName, orderType=self._order_type)

        if self.target_order_position.getPositionSide() == 2:

            if self._order_type == 2:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName)

            if self._order_type == 1:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName, orderType=self._order_type)



    def is_final(self):
        return self._status in {
            STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED
        }

