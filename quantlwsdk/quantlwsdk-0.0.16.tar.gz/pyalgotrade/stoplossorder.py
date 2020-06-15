# -*- coding: utf-8 -*-
#

import time
from decimal import Decimal

import numpy as np

from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday
from gm.api import OrderStatus_Filled
from pyalgotrade.const import STOP_PROFIT_LOSS_ORDER_STATUS,ORDER_STATUS
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
        self.orderLog=None
        self.target_order_position = None
        self._targetSymbol = None

        # self._open_price = None
        self._stop_type = None
        self._stop_gap = None

        self._target_order_cost = None
        self._clear_price = None  # 本止盈止损单就是是用来平仓的，那么平仓价格是这里记录

        self._status = None




    @classmethod
    def __from_create__(cls, target_order_position, stop_type, stop_gap,orderLog=None):

        # stopCommand 描述是止损，还是止盈。因为两个指令除了出场价算的不一样，其他全部一样，所以为了复用代码，就写在一起

        # assert target_order.position_effect == PositionEffect_Open

        stop_loss_order = cls()
        stop_loss_order.orderLog=orderLog
        stop_loss_order._stop_loss_order_id = next(cls.order_id_gen)

        stop_loss_order.target_order_position = target_order_position


        stop_loss_order._targetSymbol = target_order_position.symbol

        stop_loss_order._stop_type = stop_type
        stop_loss_order._stop_gap = stop_gap

        # stop_loss_order._position_effect = PositionEffect_Close

        # if target_order_position.positionSide == 1:
        #     stop_loss_order._side = OrderSide_Sell
        # if target_order_position.positionSide == 2:
        #     stop_loss_order._side = OrderSide_Buy

        stop_loss_order._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
        stop_loss_order._target_order_cost = target_order_position.vwap

        stop_loss_order.init_excute_fun()


        target_order_position.positionClearedEvent.subscribe(stop_loss_order.onPositionClear)

        target_order_position.set_start_stop_position(True)

        return stop_loss_order



    @abc.abstractmethod
    def init_excute_fun(self):
        raise NotImplementedError


    # def onTrade(self, tradedict):
    #     self.target_order_position.onTrade(tradedict)
    #     if self.target_order_position.volume == 0:
    #         self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def onPositionClear(self):

        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def is_final(self):
        return self._status in {
            STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED
        }








class StopLossOrder(riskStopOrder):


    def __init__(self):

        super(StopLossOrder, self).__init__()

    def init_excute_fun(self):
        # 持仓是多头还是空头
        if self.target_order_position.positionSide == 1:
            if self._stop_type == 'percent':

                self._clear_price = self._target_order_cost * (1 - self._stop_gap)
                signalName = 'stopLoss-cLong'


                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol,
                                                      self.target_order_position.volume,
                                                      signalName,orderlog=self.orderLog)

        if self.target_order_position.positionSide == 2:
            if self._stop_type == 'percent':

                self._clear_price = self._target_order_cost * (1 + self._stop_gap)
                signalName = 'stopLoss-cShort'

                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                                      self.target_order_position.volume,
                                                      signalName,orderlog=self.orderLog)

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.positionSide == 2:
                # if self._side==OrderSide_Buy:
                if tick_.price >= self._clear_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED

            if self.target_order_position.positionSide == 1:
                # if self._side==OrderSide_Sell:
                if tick_.price <= self._clear_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED

class StopProfitOrder(riskStopOrder):


    def __init__(self):

        super(StopProfitOrder, self).__init__()

    def init_excute_fun(self):
        # 持仓是多头还是空头
        if self.target_order_position.positionSide == 1:
            if self._stop_type == 'percent':

                self._clear_price = self._target_order_cost * (1 + self._stop_gap)
                signalName = 'stopProfit-cLong'


                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearLong, self._targetSymbol,
                                                      self.target_order_position.volume,
                                                      signalName)

        if self.target_order_position.positionSide == 2:
            if self._stop_type == 'percent':

                self._clear_price = self._target_order_cost * (1 - self._stop_gap)
                signalName = 'stopProfit-cShort'

                self._excute_fun = partial(gm3HelpBylw.gmOrder.clearShort, self._targetSymbol,
                                                      self.target_order_position.volume,
                                                      signalName)

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:

            if self.target_order_position.positionSide == 2:
                # if self._side==OrderSide_Buy:
                if tick_.price <= self._clear_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED

            if self.target_order_position.positionSide == 1:
                # if self._side==OrderSide_Sell:
                if tick_.price >= self._clear_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED

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
    def __init__(self,target_order_position, stop_type, stop_gap, trailing_type, trailing_gap, order_type=2,orderLog=None):

        self.ordrLog=orderLog

        self._stop_loss_order_id = next(trailingOrder.order_id_gen)

        self.target_order_position = target_order_position



        self._targetSymbol = target_order_position.symbol

        self._stop_type = stop_type
        self._stop_gap = stop_gap

        self._trailing_type	=trailing_type
        self._trailing_gap=trailing_gap

        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.TRAILING
        self._target_order_cost = target_order_position.vwap


        #准备好跟踪过程中的目标价格点


        if self.target_order_position.positionSide == 2:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_order_cost * (1 - self._trailing_gap)
        if self.target_order_position.positionSide == 1:
            if self._trailing_type == 'percent':
                self.trailing_target_price = self._target_order_cost * (1 + self._trailing_gap)



        target_order_position.positionClearedEvent.subscribe(self.onPositionClear)
        target_order_position.set_start_stop_position(True)


    def onPositionClear(self):

        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED

    def on_tick_hq(self, tick_, context=None):

        # 这个东东是掘金的context全局变量，有时候需要用它传递信息出去。最关键的是，下单的时候，需要给定平仓单平的是哪个信号的持仓。
        # 在本类中，涉及到下单，所以，需要在这里给定平仓单针对哪个信号的持仓。

        if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.ACTIVE:




            if self.target_order_position.positionSide == 2:

                if self._stop_type == 'percent':
                    clear_price = self._ll * (1 + self._stop_gap)

                if tick_.price >= clear_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gm3HelpBylw.gmOrder.clearShort(self._targetSymbol,self.target_order_position.volume,\
                                                   'trailing-cshort',tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),orderLog=self.ordrLog)

                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED

            if self.target_order_position.positionSide == 1:
                if self._stop_type == 'percent':
                    clear_long_price = self._hh * (1 - self._stop_gap)

                if tick_.price <= clear_long_price:
                    context.clearPositionSignalNames = [self.target_order_position.postionSigalName]
                    gm3HelpBylw.gmOrder.clearLong(self._targetSymbol, self.target_order_position.volume, \
                                                   'trailing-clong', tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'),orderLog=self.ordrLog)
                    self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED
                    # gmorderRe = self._excute_fun(tick_.created_at.strftime('%Y-%m-%d %H:%M:%S'))

            self._hh = max(self._hh, tick_.price)
            self._ll = min(self._ll, tick_.price)
        else:
            if self._status == STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED.TRAILING:

                if self.target_order_position.positionSide == 2:
                    if tick_.price <= self.trailing_target_price:
                        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
                        self._hh=tick_.price
                        self._ll = tick_.price

                if self.target_order_position.positionSide == 1:
                    if tick_.price >= self.trailing_target_price:
                        self._status = STOP_PROFIT_LOSS_ORDER_STATUS.ACTIVE
                        self._hh = tick_.price
                        self._ll = tick_.price


    def is_final(self):
        return self._status in {
            STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_SENDED, STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED
        }



'''
构造一个tradeorder类，这个委托类，代替掘金中的order，因为掘金，或者是ctp
中的order，其onorder 和ontrade，来的顺序不一样。我这里需要一个 必须是在ontrade之后才
进行更新的order

'''
class tradeOrder():

    #标的，数量，买卖方向，市价单子还是限价单子，开仓还是平仓
    def __init__(self,orderID,symbol, quantity, side, type, position_effect,signalName):


        self.orderID=orderID
        self.signalName=signalName


        self.symbol=symbol
        self.volume=quantity
        self.side=side
        self.type=type
        self.position_effect=position_effect



        #多两个字段来记录gm回测中的成交数量和成交均价 ，这个正常情况是在成交回报中获取，但是gm回测不太对。这里暂时应对一下
        self.gm_filled_volume=0
        self.gm_filled_vwap=0


        

        self.filled_volume=0  #已成委托数
        self.filled_vwap=0 ##已成委托 平均价

        self.avgPriceWithCost=0  #这个东西是 包含了手续费等等费用的持仓价
        self.cost=0

        self.status = ORDER_STATUS.PENDING_NEW

        self.orderTotalFIlledEvent = observer.Event()



    def fill(self, tradeDict):

        assert self.status != ORDER_STATUS.FILLED  #判断下，能进这个函数的，必须是委托还没有完全成交完的。如果出现相等，查查什么情况

        quantity = tradeDict['volume']
        # if self.filled_volume + quantity > self.volume:
        #     i=1
        assert self.filled_volume + quantity <= self.volume
        new_quantity = self.filled_volume + quantity
        self.filled_vwap = (self.filled_vwap * self.filled_volume + tradeDict['price'] * quantity) / new_quantity
        self.cost += tradeDict['commission'] + tradeDict['tax']
        self.filled_volume = new_quantity

        self.avgPriceWithCost= (self.filled_vwap * self.filled_volume+self.cost)/self.filled_volume

        if self.volume - self.filled_volume == 0:
            self.status = ORDER_STATUS.FILLED

            # aOrderPosition=OrderHoldingPostion(self)

            self.orderTotalFIlledEvent.emit(self)
    def is_final(self):
        return self.status  in {
            ORDER_STATUS.FILLED
        }


#lw 李文 添加
###委托的持仓，即某笔开仓委托  对应的持仓。
#这个持仓，在平仓委托动作后，会被处理掉。
class OrderHoldingPostion():

    def __init__(self, order_,createTime=None):
        assert order_.status== ORDER_STATUS.FILLED

        
        self.orderId = order_.orderID

        orderSignalList=order_.signalName.split('-')
        self.postionSigalName=orderSignalList[0]
        self.postionSigalAction = orderSignalList[1] # 即这个变量用来记录 委托的名字的横杠后面的东西，比如mabars-oLong,这个变量记录的是oLong

        self.symbol = order_.symbol

        if order_.side == OrderSide_Buy:
            self.positionSide = 1
        if order_.side == OrderSide_Sell:
            self.positionSide = 2

        self.volume = order_.filled_volume
        self.vwap = order_.filled_vwap
        self.avgPriceWithCost = order_.avgPriceWithCost # 这个东西是 包含了手续费等等费用的持仓价
        self.cost = order_.cost


        self.__barsSinceEntry=None
        self.__createTime=createTime

        self.clearOrderID=[]   #如果为[]，表示这个持仓，还没收到其对应的平仓指令

        self.positionClearedEvent = observer.Event()


        self.start_stop_position=False  #这个来标记，是否有止盈止损指令来建立在本orderposition上了.一旦为True，就表示要tick行情了
        self.startStopEvent = observer.Event() #这个是，如果有止盈止损指令来建立在本orderposition上了，那么开始启动本事件

    def set_start_stop_position(self,boolFlag):
        if boolFlag:
            if not self.start_stop_position:
                self.startStopEvent.emit(self.symbol)
                self.start_stop_position=True


    def onClearOrder(self,clearGmOrderObj,clearPositionSignalNames):

        #clearSignalNanmes 为一个list，即某个平仓委托，可以指定平掉好几个信号的持仓
        #clearSignalNanmes只有一个元素的时候，且元素值为all的时候，表示该平仓委托是平仓该品种所有信号进场的持仓

        assert clearGmOrderObj.position_effect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]

        # trueSig = clearSignalNanme.split('-')[0]
        # 如果平仓指令带的信号名字 和 止损止盈指令中的持仓的信号名字能对上。说明此次平仓针对的就是该
        # 止盈止损指令 针对的持仓，所以要对持仓进行仓位的减少。

        #首先呢，采集 平仓委托的id，这样等待trade记录来了，能够识别出，这个trade是哪个委托的
        if self.positionSide==1:

            if (clearGmOrderObj.symbol==self.symbol) and (clearPositionSignalNames[0]=='allLong' or self.postionSigalName in clearPositionSignalNames):
                self.clearOrderID.append(clearGmOrderObj.cl_ord_id)
        if self.positionSide==2:

            if (clearGmOrderObj.symbol==self.symbol) and (clearPositionSignalNames[0]=='allShort' or self.postionSigalName in clearPositionSignalNames):
                self.clearOrderID.append(clearGmOrderObj.cl_ord_id)

    def onTrade(self,tradedict):
        if len(self.clearOrderID)!=0 and tradedict['orderID'] in self.clearOrderID:
            assert tradedict['position_effect'] in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]
            assert tradedict['symbol']==self.symbol

            if self.positionSide == 1:
                # print(tradedict)
                # print(self.postionSigalName,' ',self.postionSigalAction)
                if tradedict['side']!=OrderSide_Sell:
                    i=1
                assert tradedict['side']==OrderSide_Sell
            if self.positionSide == 2:
                assert tradedict['side']==OrderSide_Buy



            #从现有持仓中 清除掉 平仓的仓位
            assert  self.volume>=tradedict['volume']

            self.volume = self.volume-tradedict['volume']

            if self.volume == 0:
                self.positionClearedEvent.emit()


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
