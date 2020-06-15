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

class riskStopOrder():
    order_id_gen = id_gen(int(time.time()) * 10000)

    def __init__(self):
        self._order_id = None
        # self.orderLog=None  日志都是带有时间的，条件单的日志，可能前几日 建立的，但是呢要今天才会触发，所以不适合日志是固定的。必须随时从外界传入
        self.target_order_position = None
        self._targetSymbol = None

        # self._open_price = None
        self._stop_type = None
        self._stop_gap = None

        self._order_type=None

        self._target_posi_cost = None
        self._clear_price = None  # 本止盈止损单就是是用来平仓的，那么平仓价格是这里记录
        self._signalName=None
        self._status = None

        self.orderInvalidEvent = observer.Event() #用来退订tick行情的函数会在这里。


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
    def getOrderInfo(self):
        infodict={}
        infodict['symbol']=self._targetSymbol
        infodict['cost'] = self._target_posi_cost
        infodict['clearPrice'] = self._clear_price
        infodict['status'] = self._status
        infodict['posiNum'] = self.target_order_position.getVolume()

        return  infodict


    #orderType=1表示限价单，orderType=2表示市价委托

    @classmethod
    def __from_create__(cls, target_order_position, stop_type, stop_gap,order_type=2):

        # stopCommand 描述是止损，还是止盈。因为两个指令除了出场价算的不一样，其他全部一样，所以为了复用代码，就写在一起

        # assert target_order.position_effect == PositionEffect_Open

        stop_loss_order = cls()
        # stop_loss_order.orderLog=orderLog
        stop_loss_order._stop_loss_order_id = next(cls.order_id_gen)

        stop_loss_order.target_order_position = target_order_position


        stop_loss_order._targetSymbol = target_order_position.getSymbol()

        stop_loss_order._stop_type = stop_type
        stop_loss_order._stop_gap = stop_gap
        stop_loss_order._order_type=order_type

        # stop_loss_order._position_effect = PositionEffect_Close

        # if target_order_position.positionSide == 1:
        #     stop_loss_order._side = OrderSide_Sell
        # if target_order_position.positionSide == 2:
        #     stop_loss_order._side = OrderSide_Buy

        stop_loss_order._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
        stop_loss_order._target_posi_cost = target_order_position.getVwap()

        stop_loss_order.init_excute_fun()


        # target_order_position.positionClearedEvent.subscribe(stop_loss_order.onPositionClear)

        # target_order_position.set_start_stop_position(True)

        return stop_loss_order

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
                                           self._signalName, orderType=self._order_type,
                                           price=self._clear_price)

        if self.target_order_position.getPositionSide() == 2:

            if self._order_type == 2:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName)

            if self._order_type == 1:
                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                           self.target_order_position.getAvailableVolume(),
                                           self._signalName, orderType=self._order_type,
                                           price=self._clear_price)


    # def onTrade(self, tradedict):
    #     self.target_order_position.onTrade(tradedict)
    #     if self.target_order_position.volume == 0:
    #         self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    # def onPositionClear(self):
    #
    #     self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def is_final(self):
        return self._status in {
            STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED
        }








class StopLossOrder(riskStopOrder):


    def __init__(self):

        super(StopLossOrder, self).__init__()

    def _prePareMsg(self):
        # 持仓是多头还是空头

        if self.target_order_position.getPositionSide() == 1:
            self._signalName = 'stopLoss-cLong'
            if self._stop_type == 'percent':

                self._clear_price = self._target_posi_cost * (1 - self._stop_gap)
            if self._stop_type == 'point':

                self._clear_price = self._target_posi_cost  - self._stop_gap

        if self.target_order_position.getPositionSide() == 2:
            self._signalName = 'stopLoss-cShort'
            if self._stop_type == 'percent':

                self._clear_price = self._target_posi_cost * (1 + self._stop_gap)
            if self._stop_type == 'point':

                self._clear_price = self._target_posi_cost  + self._stop_gap

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.getPositionSide() == 2:
                # if self._side==OrderSide_Buy:
                if tick_.price >= self._clear_price:
                    # context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    # self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)



            if self.target_order_position.getPositionSide() == 1:
                # if self._side==OrderSide_Sell:
                if tick_.price <= self._clear_price:
                    # context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

    def on_bar_hq(self, bar_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.getPositionSide() == 2:
                # if self._side==OrderSide_Buy:
                if bar_.high >= self._clear_price:
                    # context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    # self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)



            if self.target_order_position.getPositionSide()  == 1:
                # if self._side==OrderSide_Sell:
                if bar_.low <= self._clear_price:
                    # context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

class StopProfitOrder(riskStopOrder):


    def __init__(self):

        super(StopProfitOrder, self).__init__()

    def _prePareMsg(self):
        # 持仓是多头还是空头

        if self.target_order_position.getPositionSide()  == 1:
            self._signalName = 'stopProfit-cLong'
            if self._stop_type == 'percent':

                self._clear_price = self._target_posi_cost * (1 + self._stop_gap)
            if self._stop_type == 'point':

                self._clear_price = self._target_posi_cost  + self._stop_gap




        if self.target_order_position.getPositionSide()  == 2:
            self._signalName = 'stopProfit-cShort'
            if self._stop_type == 'percent':

                self._clear_price = self._target_posi_cost * (1 - self._stop_gap)

            if self._stop_type == 'point':

                self._clear_price = self._target_posi_cost - self._stop_gap

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。


#加了个限制对止盈，多头为例，如果多头涨停了，那么止盈就不触发了，等待涨停打开再止盈。这样是为了 第二天可能还会涨停。
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
            danghq_1 = tick_.quotes[0] #一档行情

            if self.target_order_position.getPositionSide()  == 2:
                # if self._side==OrderSide_Buy:

                #空头涨停，就是一档的买价没有。
                if 'bid_p' not in danghq_1:
                    return
                if tick_.price <= self._clear_price:

                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

            if self.target_order_position.getPositionSide()  == 1:
                if 'ask_p' not in danghq_1:
                    return
                # if self._side==OrderSide_Sell:
                if tick_.price >= self._clear_price:

                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

    def on_bar_hq(self, bar_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.getPositionSide() == 2:
                # if self._side==OrderSide_Buy:
                if bar_.low <= self._clear_price:

                    gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)

            if self.target_order_position.getPositionSide() == 1:
                # if self._side==OrderSide_Sell:
                if bar_.high >= self._clear_price:

                    gmorderRe = self._excute_fun(bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),context=context, orderLog=context.orderLog)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


def stop_loss_by_order(target_order_position,stop_type,stop_gap):
    stopLossOrder = StopLossOrder.__from_create__(target_order_position,
        stop_type=stop_type,
        stop_gap=stop_gap
    )

    return stopLossOrder




class trailingOrder():

    order_id_gen = id_gen(int(time.time()) * 10000)

    '''
    stop_type	int	止损类型，1 =‘point’2 = ‘percent’
    stop_gap	int	止损距离，整数点（非最小变动单位）
    trailing_type	int	追踪止盈触发距离计算类型，1 =‘point’2 = ‘percent’
    trailing_gap	int	追踪止盈触发距离计算距离，整数点（非最小变动单位）
    order_type	int	止盈止损执行时的委托类型,即以市价下单还是限价下单
    '''
    def __init__(self,target_order_position, stop_type, stop_gap, trailing_type, trailing_gap, currhqDateTime,order_type=2):

        self.orderInvalidEvent = observer.Event()




        # self.ordrLog=orderLog

        self._stop_loss_order_id = next(trailingOrder.order_id_gen)

        self.target_order_position = target_order_position

        self._order_type = order_type
        self._targetSymbol = target_order_position.getSymbol()

        self._stop_type = stop_type
        self._stop_gap = stop_gap

        self._trailing_type	=trailing_type
        self._trailing_gap=trailing_gap

        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING
        self._target_posi_cost = target_order_position.getVwap()


        #准备好跟踪过程中的目标价格点


        if self.target_order_position.getPositionSide() == 2:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_posi_cost * (1 - self._trailing_gap)
            if self._trailing_type == 'point':
                self.trailing_target_price = self._target_posi_cost - self._trailing_gap
        if self.target_order_position.getPositionSide() == 1:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_posi_cost * (1 + self._trailing_gap)
            if self._trailing_type == 'point':
                self.trailing_target_price = self._target_posi_cost + self._trailing_gap


        self._hh=None
        self._ll=None


        self.setRealStatus(currhqDateTime)



        # target_order_position.positionClearedEvent.subscribe(self.onPositionClear)
        # target_order_position.set_start_stop_position(True)
        
    def getSymbol(self):
        return self._targetSymbol
    def getOrderPositionObj(self):
        return self.target_order_position
    def getOrderInvalidEvent(self):
        return self.orderInvalidEvent

    def setStatus(self, status):
        self._status = status
        if self.is_final():
            self.orderInvalidEvent.emit(self._targetSymbol)

            
    def setRealStatus(self,currhqDateTime):
        dt=self.target_order_position.getUpdateTime().strftime('%Y-%m-%d %H:%M:%S')
        # dtnow=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        dtnow = currhqDateTime
        hq=gm3HelpBylw.getHQData_Fade([self._targetSymbol],dt,dtnow)

        if hq.empty:
            return

        hh=hq['high'].max()
        ll = hq['low'].min()




        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:

            if self.target_order_position.getPositionSide() == 2:
                if ll <= self.trailing_target_price:
                    # self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh=hh
                    self._ll = ll

            if self.target_order_position.getPositionSide() == 1:
                if hh >= self.trailing_target_price:
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                    self._hh = hh
                    self._ll = ll







    # def onPositionClear(self):
    #
    #     self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        # if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE:



            if self.target_order_position.getPositionSide() == 2:

                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)
                if self._stop_type == 'point':
                    clear_price = self._ll + self._stop_gap
                if tick_.price >= clear_price:
                    if self._order_type == 2:
                        gm3HelpBylw.gmOrder.clearShort(self._targetSymbol,self.target_order_position.getAvailableVolume(),\
                                                       'trailing-cshort',tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),orderLog=context.orderLog\
                                                       ,context=context)
                    if self._order_type == 1:
                        gm3HelpBylw.gmOrder.clearShort(self._targetSymbol, self.target_order_position.getAvailableVolume(), \
                                                       'trailing-cshort',
                                                       tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),\
                                                       orderType=self._order_type,price=clear_price,\
                                                       orderLog=context.orderLog\
                                                       ,context=context)
                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)



            if self.target_order_position.getPositionSide() == 1:
                if self._stop_type == 'percent':
                    clear_long_price = self._hh * (1 - self._stop_gap)
                if self._stop_type == 'point':
                    clear_long_price = self._hh - self._stop_gap
                if tick_.price <= clear_long_price:
                    if self._order_type == 2:
                        gm3HelpBylw.gmOrder.clearLong(self._targetSymbol, self.target_order_position.getAvailableVolume(), \
                                                       'trailing-clong', tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),orderLog=context.orderLog
                                                      ,context=context)
                    if self._order_type == 1:
                        gm3HelpBylw.gmOrder.clearLong(self._targetSymbol, self.target_order_position.getAvailableVolume(), \
                                                       'trailing-clong', tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),\
                                                      orderType=self._order_type,price=clear_long_price,\
                                                      orderLog=context.orderLog\
                                                      ,context=context)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))

            self._hh = max(self._hh, tick_.price)
            self._ll = min(self._ll, tick_.price)
        else:
            if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:

                if self.target_order_position.getPositionSide() == 2:
                    if tick_.price <= self.trailing_target_price:
                        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                        self._hh=tick_.price
                        self._ll = tick_.price

                if self.target_order_position.getPositionSide() == 1:
                    if tick_.price >= self.trailing_target_price:
                        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                        self._hh = tick_.price
                        self._ll = tick_.price
    def on_bar_hq(self, bar_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        # if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:
        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE:


            if self.target_order_position.getPositionSide() == 2:

                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)
                if self._stop_type == 'point':
                    clear_price = self._ll + self._stop_gap
                if bar_.high >= clear_price:

                    gm3HelpBylw.gmOrder.clearShort(self._targetSymbol,self.target_order_position.getAvailableVolume(),\
                                                   'trailing-cshort',bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),orderLog=context.orderLog\
                                                   ,context=context)

                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)



            if self.target_order_position.getPositionSide() == 1:
                if self._stop_type == 'percent':
                    clear_long_price = self._hh * (1 - self._stop_gap)
                if self._stop_type == 'point':
                    clear_long_price = self._hh  - self._stop_gap


                if bar_.low <= clear_long_price:

                    gm3HelpBylw.gmOrder.clearLong(self._targetSymbol, self.target_order_position.getAvailableVolume(), \
                                                   'trailing-clong', bar_.eob.strftime('%Y-%m-%d %H:%M:%S'),orderLog=context.orderLog\
                                                  ,context=context)
                    self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED)


                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))

            self._hh = max(self._hh, bar_.high)
            self._ll = min(self._ll, bar_.low)
        else:
            if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING:

                if self.target_order_position.getPositionSide() == 2:
                    if bar_.low <= self.trailing_target_price:
                        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                        self._hh=bar_.high
                        self._ll = bar_.low

                if self.target_order_position.getPositionSide() == 1:
                    if bar_.high >= self.trailing_target_price:
                        self.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE)
                        self._hh = bar_.high
                        self._ll = bar_.low

    def getOrderInfo(self):
        infodict = {}
        infodict['symbol'] = self._targetSymbol
        infodict['cost'] = self._target_posi_cost
        infodict['trailingPrice'] = self.trailing_target_price
        infodict['status'] = self._status
        infodict['posiNum'] = self.target_order_position.getVolume()
        infodict['hh'] = self._hh
        infodict['ll'] = self._ll
        return infodict



    def is_final(self):
        return self._status in {
            STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED
        }



# '''
# 构造一个tradeorder类，这个委托类，代替掘金中的order，因为掘金，或者是ctp
# 中的order，其onorder 和ontrade，来的顺序不一样。我这里需要一个 必须是在ontrade之后才
# 进行更新的order
#
# '''
# class tradeOrder():
#
#     #标的，数量，买卖方向，市价单子还是限价单子，开仓还是平仓
#     def __init__(self,orderID,symbol, quantity, side, type, position_effect,signalName):
#
#
#         self.orderID=orderID
#         self.signalName=signalName
#
#
#         self.symbol=symbol
#         self.volume=quantity
#         self.side=side
#         self.type=type
#         self.position_effect=position_effect
#
#
#
#         #多两个字段来记录gm回测中的成交数量和成交均价 ，这个正常情况是在成交回报中获取，但是gm回测不太对。这里暂时应对一下
#         self.gm_filled_volume=0
#         self.gm_filled_vwap=0
#
#
#
#
#         self.filled_volume=0  #已成委托数
#         self.filled_vwap=0 ##已成委托 平均价
#
#         self.avgPriceWithCost=0  #这个东西是 包含了手续费等等费用的持仓价
#         self.cost=0
#
#         self.status = ORDER_STATUS.PENDING_NEW
#
#         self.orderTotalFIlledEvent = observer.Event()
#
#
#
#     def fill(self, tradeDict):
#
#         assert self.status != ORDER_STATUS.FILLED  #判断下，能进这个函数的，必须是委托还没有完全成交完的。如果出现相等，查查什么情况
#
#         quantity = tradeDict['volume']
#         # if self.filled_volume + quantity > self.volume:
#         #     i=1
#         assert self.filled_volume + quantity <= self.volume
#         new_quantity = self.filled_volume + quantity
#         self.filled_vwap = (self.filled_vwap * self.filled_volume + tradeDict['price'] * quantity) / new_quantity
#         self.cost += tradeDict['commission'] + tradeDict['tax']
#         self.filled_volume = new_quantity
#
#         self.avgPriceWithCost= (self.filled_vwap * self.filled_volume+self.cost)/self.filled_volume
#
#         if self.volume - self.filled_volume == 0:
#             self.status = ORDER_STATUS.FILLED
#
#             # aOrderPosition=OrderHoldingPostion(self)
#
#             self.orderTotalFIlledEvent.emit(self)
#     def is_final(self):
#         return self.status  in {
#             ORDER_STATUS.FILLED
#         }
#
