# -*- coding: utf-8 -*-
'''


lw李文写的
模拟能够处理止盈止损指令的broker。
'''


import time
from pyalgotrade.const import ORDER_TYPE,ORDER_STATUS,STOP_PROFIT_LOSS_ORDER_STATUS,POSITION_SIDE
from pyalgotrade.stoplossorder_3rdAccount import StopProfitOrder,StopLossOrder,trailingOrder
from pyalgotrade.conditionOrder.aboveOrder import AboveOrder

from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday

from pyalgotrade import observer

from pyalgotrade.utils import createCusPositionFromGmPosition,cusPositionSideToGMPositionSide


class BaseConditionBroker():
    def __init__(self, bTestID, positionObj=None, stopOrderLog=None):

        self.bTestID = bTestID
        # self.orderLog = orderLog  # 这个是委托的日志，用来真正下委托的时候记录的日志
        self.stopOrderLog = stopOrderLog  # 这个用来记录，止损，止盈，跟踪止盈等指令，建立起来后的，要写个日志。



        # key为symbol+long 或者symbol+short.算了，还是key为symbol吧
        self._condition_orders_dict = {}

        # 这2个list 是  装的函数，一个是用来订阅行情，一个是用来退订行情.函数通过偏函数处理了，即
        # 包裹了一个频率的字段，symbol字段在内部来提供
        # self.subfunList=subfunList
        # self.unsubfunList=unsubfunList

        self._positions = positionObj

        self.stoplossOrderCreatedEvent = observer.Event()

    def setStopOrderLog(self, stopOrderLog):
        self.stopOrderLog = stopOrderLog

    def setPositions(self, positionsObj):
        self._positions = positionsObj

    def getSLOrdersSymbols(self):
        # return set([o._targetSymbol for o in self._stoploss_orders])

        return set(list(self._condition_orders_dict.keys()))

    def getConditionOrders(self):
        return self._condition_orders_dict

    def addOrder(self, o):
        # self._stoploss_orders.append(o)

        sym = o.getSymbol()
        if sym not in self._condition_orders_dict:
            self._condition_orders_dict[sym] = []

        self._condition_orders_dict[sym].append(o)
        i=1

    # def addStopOrder(self,o):
    #
    #     sym=o.getSymbol()
    #     self._stoploss_orders.append(o)
    #

    # 1、持仓没有了，则建立在该持仓上面的slorder要剔除掉

    # def deleteSLOrders(self,context):
    #     tempOrders=[]
    #
    #     for aOrders in self._stoploss_orders:
    #         symbol_=aOrders._targetSymbol
    #         side_=aOrders.target_order_position.positionSide
    #         gmposi=context.account().position(symbol_,side_)
    #         if gmposi is not None:
    #             tempOrders.append(aOrders)
    #     self._stoploss_orders=tempOrders

    # 2、已经下单了。比如止损单，已经达到了，然后下出了单子。
    # def deleteSLOrders(self):
    #     self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]

    def deleteSLOrders(self, sym):
        currSymOrders = self._condition_orders_dict[sym]
        self._condition_orders_dict[sym] = [o for o in currSymOrders if not o.is_final()]

    # 删除某些持仓的所有条件单
    def deleteOrdersBySpecialHolding(self, sym, side_):
        currSymOrders = self._condition_orders_dict.setdefault(sym, [])
        self._condition_orders_dict[sym] = [o for o in currSymOrders if
                                            o.getOrderPositionObj().getPositionSide() != side_]

        print(currSymOrders)
        for o in currSymOrders:
            print(o.getOrderPositionObj().getPositionSide())

        print('deletPositonOrder: ', sym, ' ', side_)

        print('now curr sym orders: ', self._condition_orders_dict.setdefault(sym, []))

    def getSLOrders(self, sym):
        currSymOrders = self._condition_orders_dict.setdefault(sym, [])
        return currSymOrders

    def ontick(self, tick, context=None):
        asymbol = tick.symbol
        # matchOrders = [o for o in self._stoploss_orders if o._targetSymbol == asymbol]
        matchOrders = self._condition_orders_dict.setdefault(asymbol, [])
        for aspOrder in matchOrders:
            aspOrder.on_tick_hq(tick, context=context)
        self.deleteSLOrders(asymbol)

    def onbar(self, bar, context=None):
        asymbol = bar.symbol
        matchOrders = self._condition_orders_dict.setdefault(asymbol, [])
        # matchOrders = [o for o in self._stoploss_orders if o._targetSymbol == asymbol]

        for aspOrder in matchOrders:
            aspOrder.on_bar_hq(bar, context=context)
        self.deleteSLOrders(asymbol)

    # def simulateTrade(self):

    # self.deleteSLOrders()
    # self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]



    def onTradeRsp(self, gmTrade):

        positionSide_ = gmTrade.getTargetPositionSide()
        symbol_ = gmTrade.getSymbol()
        side_ = gmTrade.getSide()
        cusposi = self._positions.getHolding(symbol_, str(positionSide_))

        if gmTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
                                           PositionEffect_CloseYesterday]:


            if cusposi is None:
                currsymOrders = self.getSLOrders(symbol_)
                for aOrders in currsymOrders:
                    if symbol_ == aOrders.getSymbol() and side_ == aOrders.getOrderPositionObj().getPositionSide():
                        aOrders.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED)
                self.deleteOrdersBySpecialHolding(symbol_, positionSide_)
                # self.deleteSLOrders(symbol_)



    # 给symbol 订阅行情
    def _subHQ(self, symbol, subfunList):
        for afun in subfunList:
            afun(symbol)
        # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下

    # 这个是具体的条件单订阅退订行情的函数，等到这些条件单失效，就会调用这些函数 来退订行情
    def _unsubHQ(self, o, unsubfunList):
        for afun in unsubfunList:
            o.getOrderInvalidEvent().subscribe(afun)




class normalConditionBroker(BaseConditionBroker):
    def __init__(self, bTestID, positionObj=None, orderLog=None, stopOrderLog=None):
        super(normalConditionBroker, self).__init__(bTestID,positionObj=positionObj,stopOrderLog=stopOrderLog)



    def create_above_orderOnOrderRsp(self, cusOrder,price, orderType=2, subfunList=[], unsubfunList=[]):
        # positionSide_ = gmTrade.getTargetPositionSide()
        # symbol_ = gmTrade.getSymbol()
        # side_ = gmTrade.getSide()
        #
        # gmposi = context.account().position(symbol_, positionSide_)
        # print(symbol_, ' ', positionSide_)
        # self._positions.setAvailableVolume(symbol_, positionSide_, gmposi['available'])
        # cusposi = self._positions.getHolding(symbol_, str(positionSide_))

        if cusOrder.getPositionEffect() in [PositionEffect_Open]:
            symbol_ = cusOrder.getSymbol()
            positionSide_ = cusOrder.getTargetPositionSide()
            cusposi = self._positions.getHolding(symbol_, str(positionSide_))

            while (1):
                # 即能够查到的持仓，刚好是这个委托全部成交的持仓
                if cusposi is not None and cusposi.getVolume() == cusOrder.getVolume():
                    currhqDateTime = cusOrder.getUpdateTime().strftime('%Y-%m-%d %H:%M:%S')
                    o = AboveOrder(price, cusposi, order_type=orderType)
                    break
                else:
                    time.sleep(1)


        if self.stopOrderLog is not None:
            orderInfo = o.getOrderInfo()
            # dtstr=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msgStr = 'aboveOrder ' + \
                     ' symbol:' + orderInfo['symbol'] + \
                     ' positionSide:' + str(orderInfo['positionSide']) + \
                     ' posiVol:' + str(orderInfo['posiNum']) + \
                     ' status:' + orderInfo['status'].value
            # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
            #                        orderInfo['clearPrice'],orderInfo['status'])
            self.stopOrderLog.info("%s,%s", currhqDateTime, msgStr)

        self._subHQ(o.getSymbol(), subfunList)
        self._unsubHQ(o, unsubfunList)  # 这里不是退订行情，而是给条件单 的事件 订阅一个退订函数。
        self.addOrder(o)
    #这个是因为，掘金回测中，成交回报在委托回报之后，所以委托回报中，mongo持仓是要成交回报来形成的。导致委托回报中，根本查不到持仓。
    def create_above_orderOnTradeRsp(self, cusTrade,price, orderType=2, subfunList=[], unsubfunList=[]):


        if cusTrade.getPositionEffect() in [PositionEffect_Open]:
            symbol_ = cusTrade.getSymbol()
            positionSide_ = cusTrade.getTargetPositionSide()
            cusposi = self._positions.getHolding(symbol_, str(positionSide_))


            currhqDateTime = cusTrade.getTradeTime().strftime('%Y-%m-%d %H:%M:%S')
            o = AboveOrder(price, cusposi, order_type=orderType)


            if self.stopOrderLog is not None:
                orderInfo = o.getOrderInfo()
                # dtstr=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msgStr = 'aboveOrder ' + \
                         ' symbol:' + orderInfo['symbol'] + \
                         ' positionSide:' + str(orderInfo['positionSide']) + \
                         ' posiVol:' + str(orderInfo['posiNum']) + \
                         ' status:' + orderInfo['status'].value
                # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
                #                        orderInfo['clearPrice'],orderInfo['status'])
                self.stopOrderLog.info("%s,%s", currhqDateTime, msgStr)

            self._subHQ(o.getSymbol(), subfunList)
            self._unsubHQ(o, unsubfunList)  # 这里不是退订行情，而是给条件单 的事件 订阅一个退订函数。
            self.addOrder(o)

class SimulationStopLossProfitBroker():
    def __init__(self,bTestID,positionObj=None,stopOrderLog=None,subfunList=None,unsubfunList=None):

        self.bTestID=bTestID
        # self.orderLog=orderLog #这个是委托的日志，用来真正下委托的时候记录的日志
        self.stopOrderLog=stopOrderLog  #这个用来记录，止损，止盈，跟踪止盈等指令，建立起来后的，要写个日志。

        self._stoploss_orders = []

        # key为symbol+long 或者symbol+short.算了，还是key为symbol吧
        self._condition_orders_dict={}

        #这2个list 是  装的函数，一个是用来订阅行情，一个是用来退订行情.函数通过偏函数处理了，即
        #包裹了一个频率的字段，symbol字段在内部来提供
        # self.subfunList=subfunList
        # self.unsubfunList=unsubfunList


        self._positions=positionObj

        self.stoplossOrderCreatedEvent = observer.Event()

    # def setOrderLog(self,orderLog):
    #     self.orderLog=orderLog
    def setStopOrderLog(self,stopOrderLog):
        self.stopOrderLog=stopOrderLog

    def setPositions(self,positionsObj):
        self._positions=positionsObj

    def getSLOrdersSymbols(self):
        # return set([o._targetSymbol for o in self._stoploss_orders])

        return set(list(self._condition_orders_dict.keys()))


    def getConditionOrders(self):
        return self._condition_orders_dict


    def addStopOrder(self,o):
        # self._stoploss_orders.append(o)

        sym=o.getSymbol()
        if sym not in self._condition_orders_dict:
            self._condition_orders_dict[sym]=[]

        self._condition_orders_dict[sym].append(o)




    # def addStopOrder(self,o):
    #
    #     sym=o.getSymbol()
    #     self._stoploss_orders.append(o)
    #




    #1、持仓没有了，则建立在该持仓上面的slorder要剔除掉

    # def deleteSLOrders(self,context):
    #     tempOrders=[]
    #
    #     for aOrders in self._stoploss_orders:
    #         symbol_=aOrders._targetSymbol
    #         side_=aOrders.target_order_position.positionSide
    #         gmposi=context.account().position(symbol_,side_)
    #         if gmposi is not None:
    #             tempOrders.append(aOrders)
    #     self._stoploss_orders=tempOrders

    # 2、已经下单了。比如止损单，已经达到了，然后下出了单子。
    # def deleteSLOrders(self):
    #     self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]

    def deleteSLOrders(self,sym):
        currSymOrders = self._condition_orders_dict[sym]
        self._condition_orders_dict[sym]=[o for o in currSymOrders if not o.is_final()]

#删除某些持仓的所有条件单
    def deleteOrdersBySpecialHolding(self,sym,side_):
        currSymOrders = self._condition_orders_dict.setdefault(sym,[])
        self._condition_orders_dict[sym]=[o for o in currSymOrders if o.getOrderPositionObj().getPositionSide()!=side_]

        print(currSymOrders)
        for o in currSymOrders:
            print(o.getOrderPositionObj().getPositionSide())

        print('deletPositonOrder: ',sym,' ',side_)

        print('now curr sym orders: ',self._condition_orders_dict.setdefault(sym,[]))

    def getSLOrders(self,sym):
        currSymOrders = self._condition_orders_dict.setdefault(sym,[])
        return currSymOrders




    def ontick(self,tick,context=None):
        asymbol = tick.symbol
        # matchOrders = [o for o in self._stoploss_orders if o._targetSymbol == asymbol]
        matchOrders=self._condition_orders_dict.setdefault(asymbol,[])
        for aspOrder in matchOrders:
            aspOrder.on_tick_hq(tick,context=context)
        self.deleteSLOrders(asymbol)

    def onbar(self,bar,context=None):
        asymbol = bar.symbol
        matchOrders = self._condition_orders_dict.setdefault(asymbol, [])
        # matchOrders = [o for o in self._stoploss_orders if o._targetSymbol == asymbol]

        for aspOrder in matchOrders:
            aspOrder.on_bar_hq(bar,context=context)
        self.deleteSLOrders(asymbol)

# def simulateTrade(self):
        






        # self.deleteSLOrders()
        # self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]

    def onOrderRsp(self,cusOrder,context):
        #context 关于平仓指令,有2个名字，一个是平仓的信号名字，即因为什么信号平仓，另外一个是平仓的是针对哪个开仓信号。要存为list
        #context关于开仓指令的名字，只需要存为一个，开仓的信号名字

        if  gmOrderObj.positionEffect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:
            # if context.is_backtest_model():
            #     self._create_clear_order_fromGmOrders(gmOrderObj)

           #委托已成 后，平仓委托 需要取查 该持仓是否 还在，如果不在了，就要剔除相关止盈止损指令等。
            symbol_=gmOrderObj.symbol
            side_=gmOrderObj.getPositionSide()

            gmside=cusPositionSideToGMPositionSide(side_)
            gmposi=context.account().position(symbol_,gmside)
            if gmposi is None:
                
                for aOrders in self._stoploss_orders:
                    if symbol_ == aOrders.getSymbol() and side_ == aOrders.getOrderPositionObj().getPositionSide():
                        aOrders.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED)
        
                self.deleteSLOrders()

        if  cusOrder.getPositionEffect() in [PositionEffect_Open]:
            symbol_=cusOrder.getSymbol()
            side_=cusOrder.getTargetPositionSide()

            gmposi=context.account().position(symbol_,side_)
            # print(symbol_,' ',side_,' ',gmposi)
            if gmposi is None:
                print(symbol_,' ',gmside,' ',gmOrderObj.positionEffect,' ',gmOrderObj.created_at)
            if gmposi and  gmposi['available']>0:
                aposi=createCusPositionFromGmPosition(gmposi)
                context._createSOrder(aposi,context.bTestParams,self,context.now.strftime('%Y-%m-%d %H:%M:%S'))

    def onTradeRsp(self, gmTrade, context,account=None):

        positionSide_=gmTrade.getTargetPositionSide()
        symbol_ = gmTrade.getSymbol()
        side_ = gmTrade.getSide()
        cusposi = self._positions.getHolding(symbol_, str(positionSide_))

        if gmTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
                                         PositionEffect_CloseYesterday]:
            # if context.is_backtest_model():
            #     self._create_clear_order_fromGmOrders(gmOrderObj)

            # 本次平仓的成交完成了，需要取查 该持仓是否 还在，如果不在了，就要剔除相关止盈止损指令等。


            # gmside = cusPositionSideToGMPositionSide(side_)

            #side_ 为1表示买动作，2为卖动作

            # if side_==1: #买平，表明针对空头持仓
            #     gmPos_=2
            # if side_==2: #卖平，表明针对多头持仓
            #     gmPos_=1

            # #这里是用掘金的账户来查持仓
            # gmposi = context.account().position(symbol_, gmPos_)

            # 这里是用自己记录的mongodb账户来查持仓
            # gmposi = account.getHolding(symbol_, str(gmPos_))


            if cusposi is None:
                currsymOrders=self.getSLOrders(symbol_)
                for aOrders in currsymOrders:
                    if symbol_ == aOrders.getSymbol() and side_ == aOrders.getOrderPositionObj().getPositionSide():
                        aOrders.setStatus(STOP_PROFIT_LOSS_ORDER_STATUS.ORDER_CANCELED)
                self.deleteOrdersBySpecialHolding(symbol_, positionSide_)
                # self.deleteSLOrders(symbol_)
        if gmTrade.getPositionEffect()  in [PositionEffect_Open]:
            # symbol_ = gmTrade.getSymbol()
            # side_ = gmTrade.getSide()   #买方向是1，卖方向是2，掘金中 多头方向也是1，空头方向也是2
            # positionSide_=side_

            gmposi = context.account().position(symbol_, positionSide_)
            print(symbol_,' ',positionSide_)
            self._positions.setAvailableVolume(symbol_,positionSide_,gmposi['available'])
            cusposi = self._positions.getHolding(symbol_, str(positionSide_))
            # print(symbol_,' ',side_,' ',gmposi)
            if cusposi is None:
                print('stopOrder on tradeRsp  ',symbol_, ' ', positionSide_, ' ', gmTrade.getPositionEffect(), ' ', gmTrade.getTradeTime())
            if cusposi and cusposi.getAvailableVolume() > 0:

                #如果是开仓形成的头寸，因为是成交 回报，所以认为是 一笔委托的第n个成交，那么前面的成交形成的持仓 上建立
                #起来的头寸，需要完全被删除掉。
                self.deleteOrdersBySpecialHolding(symbol_,positionSide_)

                # aposi = createCusPositionFromGmPosition(gmposi)



                # 这里是用自己记录的mongodb账户来查持仓，mongodb账户的持仓中会计算具体的持仓均价。
                # aposi=account.getHolding(symbol_, str(positionSide_),8)

                context._createSOrder(cusposi, context.bTestParams, self, context.now.strftime('%Y-%m-%d %H:%M:%S'))




#stopType是描述 stopThresh 这个值是什么。是pencent，还是point,stopThresh 就是具体的值了。
    # order_type	int	止盈止损执行时的委托类型，即是市价委托还是限价委托。
    def create_stop_order(self,aOrderPosition,stopType,stopThresh,currhqDateTime,\
                          stopCommand='stoploss',orderType=2,subfunList=[],unsubfunList=[]):


       
        


       


       
        if stopCommand=='stoploss':
            # o = StopLossOrder.__from_create__(aOrderPosition, stopType, stopThresh,order_type=orderType,orderLog=self.orderLog)
            o = StopLossOrder.__from_create__(aOrderPosition, stopType, stopThresh, order_type=orderType)
            if self.stopOrderLog is not None:
                orderInfo=o.getOrderInfo()
                # dtstr=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msgStr='stopLoss '+\
                    ' symbol:'+orderInfo['symbol']+ \
                    ' cost:' + str(round(orderInfo['cost'],2)) + \
                    ' clearPrice:' + str(round(orderInfo['clearPrice'], 2)) + \
                    ' posiVol:' + str(orderInfo['posiNum']) + \
                    ' status:' + orderInfo['status'].value
                    # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
                #                        orderInfo['clearPrice'],orderInfo['status'])
                self.stopOrderLog.info("%s,%s",currhqDateTime,msgStr)
        if stopCommand=='stopprofit':
            o = StopProfitOrder.__from_create__(aOrderPosition, stopType, stopThresh,order_type=orderType)
            if self.stopOrderLog is not None:
                orderInfo = o.getOrderInfo()
                # dtstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msgStr = 'stopProfit ' + \
                         ' symbol:' + orderInfo['symbol'] + \
                         ' cost:' + str(round(orderInfo['cost'], 2)) + \
                         ' clearPrice:' + str(round(orderInfo['clearPrice'], 2)) + \
                         ' posiVol:' + str(orderInfo['posiNum']) + \
                         ' status:' + orderInfo['status'].value
                # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
                #                        orderInfo['clearPrice'],orderInfo['status'])
                self.stopOrderLog.info("%s,%s", currhqDateTime, msgStr)
                
        self._subHQ(o.getSymbol(),subfunList)
        self._unsubHQ(o,unsubfunList) #这里不是退订行情，而是给条件单 的事件 订阅一个退订函数。
        self.addStopOrder(o)



    # #给symbol 订阅行情
    # def _subHQ(self,symbol):
    #     for afun in self.subfunList:
    #         afun(symbol)
    #     # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下
    #
    #
    # #这个是具体的条件单订阅退订行情的函数，等到这些条件单失效，就会调用这些函数 来退订行情
    # def _unsubHQ(self,o):
    #     for afun in self.unsubfunList:
    #         o.getOrderInvalidEvent().subscribe(afun)

    # 给symbol 订阅行情
    def _subHQ(self, symbol,subfunList):
        for afun in subfunList:
            afun(symbol)
        # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下

    # 这个是具体的条件单订阅退订行情的函数，等到这些条件单失效，就会调用这些函数 来退订行情
    def _unsubHQ(self, o,unsubfunList):
        for afun in unsubfunList:
            o.getOrderInvalidEvent().subscribe(afun)

    # trailing_type描述 trailingThresh 这个值是什么。是pencent，还是point,
    # stop_type，描述stopThresh 这个值是什么，是percent还是point，
    # order_type	int	止盈止损执行时的委托类型，即是市价委托还是限价委托。
    def create_trailing_order(self,aOrderPosition,trailing_type,trailingThresh,stop_type,stopThresh,currhqDateTime,\
                              subfunList=[],unsubfunList=[],orderType=2):

        # assert atradeOrder.status == ORDER_STATUS.FILLED
        # if atradeOrder.status == ORDER_STATUS.FILLED:

        # underLySym = commonHelpBylw.getMainContinContract(aOrderPosition.symbol)
        # orderLog = loggerHelpbylw.getFileLogger(self.bTestID + '-' + underLySym + '-orderlog',
        #                                         'log\\' + self.bTestID + '\\' + underLySym + '-orderRecord.txt',
        #                                         mode_='a')

        o = trailingOrder(aOrderPosition, stop_type, stopThresh, trailing_type, trailingThresh, currhqDateTime, \
                          order_type=orderType)
        # o = trailingOrder(aOrderPosition,stop_type,stopThresh,trailing_type,trailingThresh,currhqDateTime,\
        #                   order_type=orderType,orderLog=self.orderLog)
        

        if self.stopOrderLog is not None:
            orderInfo = o.getOrderInfo()
            # dtstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msgStr = 'stopTrailing ' + \
                     ' symbol:' + orderInfo['symbol'] + \
                     ' cost:' + str(round(orderInfo['cost'], 2)) + \
                     ' trailingPrice:' + str(round(orderInfo['trailingPrice'], 2)) + \
                     ' status:' + orderInfo['status'].value+ \
                     ' posiVol:' + str(orderInfo['posiNum']) + \
                     ' hh:' + str(orderInfo['hh']) + \
                     ' ll:' + str(orderInfo['ll'])
                # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
            #                        orderInfo['clearPrice'],orderInfo['status'])
            self.stopOrderLog.info("%s,%s", currhqDateTime, msgStr)

        self._subHQ(o.getSymbol(),subfunList)
        self._unsubHQ(o,unsubfunList)
        self.addStopOrder(o)
            # self.addOrderPosition(aOrderPosition)

            # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下


    # def onClearOrder(self,clearGmOrderObj,clearPositionSignalNames):
    #
    #
    #     for aOP in self.orderPostions:
    #         aOP.onClearOrder(clearGmOrderObj,clearPositionSignalNames)
    #
    #
    #


    def create_above_order(self, price, aOrderPosition,currhqDateTime,orderType=2, subfunList=[], unsubfunList=[]):

        o = AboveOrder(price, aOrderPosition, order_type=orderType)

        if self.stopOrderLog is not None:
            orderInfo = o.getOrderInfo()
            # dtstr=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msgStr = 'stopLoss ' + \
                     ' symbol:' + orderInfo['symbol'] + \
                     ' cost:' + str(round(orderInfo['cost'], 2)) + \
                     ' clearPrice:' + str(round(orderInfo['clearPrice'], 2)) + \
                     ' posiVol:' + str(orderInfo['posiNum']) + \
                     ' status:' + orderInfo['status'].value
            # self.stopOrderLog.info("%s,%s,%s,%s,%s,%s",dtstr,'stopLoss',orderInfo['symbol'],orderInfo['cost'],\
            #                        orderInfo['clearPrice'],orderInfo['status'])
            self.stopOrderLog.info("%s,%s", currhqDateTime, msgStr)


        self._subHQ(o.getSymbol(), subfunList)
        self._unsubHQ(o, unsubfunList)  # 这里不是退订行情，而是给条件单 的事件 订阅一个退订函数。
        self.addStopOrder(o)
