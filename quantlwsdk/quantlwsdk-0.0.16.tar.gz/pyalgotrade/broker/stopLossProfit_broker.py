# -*- coding: utf-8 -*-
'''


lw李文写的
模拟能够处理止盈止损指令的broker。
'''


from pyalgotrade import loggerHelpbylw
from pyalgotrade.const import ORDER_TYPE,ORDER_STATUS,STOP_PROFIT_LOSS_ORDER_STATUS,POSITION_SIDE
from pyalgotrade.stoplossorder import stop_loss_by_order,tradeOrder,OrderHoldingPostion,StopProfitOrder,StopLossOrder,trailingOrder


from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday
from gm.api import OrderStatus_Filled
from pyalgotrade import observer
from pyalgotrade.utils import createTradeRecordFromGmorder
from pyalgotrade import commonHelpBylw
from functools import partial
class SimulationStopLossProfitBroker():
    def __init__(self,bTestID):

        self.bTestID=bTestID

        self._stoploss_orders = []
        self.trade_orders = {}  # trade_orders[tradeo.orderID]=tradeo

        self.orderPostions=[]

        # 这玩意用来记录平仓委托，本来trade_orders记录开仓委托就够了，对于止损逻辑
        #但是掘金回测这个傻逼玩意，ontrade中拿不到均价，所以只能在委托回报中先拿到，所以这里要存一下。
        self.clearOrders={}

        self.stoplossOrderCreatedEvent = observer.Event()

    def getSLOrdersSymbols(self):
        return list(set([o._targetSymbol for o in self._stoploss_orders]))

    def addClearOrder(self,tradeo):
        self.clearOrders[tradeo.orderID] = tradeo
    def addTradeOrder(self,tradeo):
        self.trade_orders[tradeo.orderID] = tradeo

    def addStopOrder(self,o):
        self._stoploss_orders.append(o)

    def addOrderPosition(self,o):
        self.orderPostions.append(o)

    
    
    #这个东西是因为，gm的回测中，ontade有许多东西没有填充，成交全部记录在委托中了
    #而这些委托，被我自己建立了tradeOrder记录了。
    def ongmbacktestTrade(self,gmexecrpt,context):
        cid=gmexecrpt.cl_ord_id
        if gmexecrpt.position_effect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:
            sOrder=self.clearOrders[cid]
            del self.clearOrders[cid]
        if gmexecrpt.position_effect ==PositionEffect_Open:
            sOrder=self.trade_orders[cid]
        tradedict = {}
        tradedict['symbol'] = gmexecrpt.symbol
        tradedict['orderID'] = gmexecrpt.cl_ord_id
        tradedict['side'] = gmexecrpt.side
        tradedict['position_effect'] = gmexecrpt.position_effect
        tradedict['volume'] = sOrder.gm_filled_volume
        tradedict['price'] = sOrder.gm_filled_vwap
        tradedict['commission'] = gmexecrpt.cost
        tradedict['tax'] = 0

        
        self.onTrade(tradedict,context)

    
    def onTrade(self,tradedict,context):


        #如果是开仓指令的trade来了，那么就考虑tradeorder是否已经全部成交了，成交了则考虑 建立止盈止损指令了
        #如果是平仓指令，那么就是考察orderposition是不是有影响


        #如果是开仓动作的交易回报，那么去处理 tradeorder，这个tradeorder就是记录开仓的委托的
        if tradedict['position_effect']==PositionEffect_Open:
            # 在这里给委托补充持仓均价字段。
            atradeOrder = self.trade_orders.get(tradedict['orderID'])
            if atradeOrder is not None:
                atradeOrder.fill(tradedict)


                #order 完全成交了，那么创建orderposition ,创建止盈止损指令。
                if atradeOrder.status == ORDER_STATUS.FILLED:
                    aOrderPosition = OrderHoldingPostion(atradeOrder)
                    self.addOrderPosition(aOrderPosition)

                    #给aOrderPosition 中的 startStopEvent 引用订阅行情的动作，这样当aOrderPosition第一次建立了
                    #止盈止损的时候，需要取订阅行情
                    subgmFun = partial(context.subscribe, frequency='tick')
                    aOrderPosition.startStopEvent.subscribe(subgmFun)

                    lwSubscribeFun = partial(context.subcribeObj.add, fre='tick')
                    aOrderPosition.startStopEvent.subscribe(lwSubscribeFun)



                    aSymbol = aOrderPosition.symbol
                    underLyingSymbol = commonHelpBylw.getMainContinContract(aSymbol)
                    stopLossThresh = context.bTestParams[underLyingSymbol]['stopLossRatio']
                    stopProfitThresh = context.bTestParams[underLyingSymbol]['stopProfitRatio']

                    trailing_type= context.bTestParams[underLyingSymbol]['trailing_type']
                    trailingThresh= context.bTestParams[underLyingSymbol]['trailingThresh']
                    trailing_stop_type=context.bTestParams[underLyingSymbol]['trailing_stop_type']
                    trailing_stopThresh=context.bTestParams[underLyingSymbol]['trailing_stopThresh']





                    self.create_stop_order(aOrderPosition,stopThresh=stopLossThresh, stopCommand='stoploss')


                    # 再创建一个止盈指令
                    # stopProfit = partial(context.simuBroker4StopLossProfit.create_stop_order,
                    #                      stopThresh=stopProfitThresh, stopCommand='stopprofit')
                    # tradeo.orderTotalFIlledEvent.subscribe(stopProfit)

                    self.create_stop_order(aOrderPosition,stopThresh=stopProfitThresh, stopCommand='stopprofit')



                    self.create_trailing_order(aOrderPosition,trailing_type,trailingThresh,trailing_stop_type,trailing_stopThresh)



            self._deleteTradeOrders()   #因为tradeorder已经完成了，stoporder会建立起来，所以应该清除掉了。

        if tradedict['position_effect'] in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:

            # for aSLOrder in self._stoploss_orders:
            #     aSLOrder.onTrade(tradedict)

            for aOP in self.orderPostions:
                aOP.onTrade(tradedict)

            # self.deleteSLOrdersByClearPosition()
            self.deleteOrderPositions()  #因为持仓可能为0，所以清除掉
            self.deleteSLOrders() #因为持仓可能为0，所以清除掉可能导致order的状态变为失效

    # def deleteSLOrdersByClearPosition(self):
    #     self._stoploss_orders = [o for o in self._stoploss_orders if o.target_order_position.volume > 0]


    def _deleteTradeOrders(self):
        new_trade_orders = {}
        for oid, o in self.trade_orders.items():
            if not o.is_final():
                new_trade_orders[oid] = o
        self.trade_orders = new_trade_orders

    #即已经执行的止损止盈单，要提出掉
    def deleteSLOrders(self):
        self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]

    def deleteOrderPositions(self):
        self.orderPostions = [op for op in self.orderPostions if op.volume>0]




    def ontick(self,tick,context=None):
        asymbol = tick.symbol
        matchOrders = [o for o in self._stoploss_orders if o._targetSymbol == asymbol]

        for aspOrder in matchOrders:
            aspOrder.on_tick_hq(tick,context=context)


# def simulateTrade(self):
        






        # self.deleteSLOrders()
        # self._stoploss_orders = [o for o in self._stoploss_orders if not o.is_final()]

    def onOrderRsp(self,gmOrderObj,context):
        #context 关于平仓指令,有2个名字，一个是平仓的信号名字，即因为什么信号平仓，另外一个是平仓的是针对哪个开仓信号。要存为list
        #context关于开仓指令的名字，只需要存为一个，开仓的信号名字

        if  gmOrderObj.position_effect in [PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday]:
            if context.is_backtest_model():
                self._create_clear_order_fromGmOrders(gmOrderObj)

            clearPositionSignalNames=context.clearPositionSignalNames
            self.onClearOrder(gmOrderObj,clearPositionSignalNames)


        if  gmOrderObj.position_effect in [PositionEffect_Open]:
            signalName=context.signalName
            tradeo=self._create_trade_order_fromGmOrders(gmOrderObj,signalName)


            # aSymbol = gmOrderObj.symbol
            # underLyingSymbol = commonHelpBylw.getMainContinContract(aSymbol)
            # stopLossThresh = context.bTestParams[underLyingSymbol]['stopLossRatio']
            # stopProfitThresh = context.bTestParams[underLyingSymbol]['stopProfitRatio']
            #
            # stoploss = partial(context.simuBroker4StopLossProfit.create_stop_order,
            #                    stopThresh=stopLossThresh, stopCommand='stoploss')
            # tradeo.orderTotalFIlledEvent.subscribe(stoploss)
            #
            # # 再创建一个止盈指令
            # stopProfit = partial(context.simuBroker4StopLossProfit.create_stop_order,
            #                      stopThresh=stopProfitThresh, stopCommand='stopprofit')
            # tradeo.orderTotalFIlledEvent.subscribe(stopProfit)



    def _create_clear_order_fromGmOrders(self,gmOrderObj):

        # 这个信号随便设置一个，反正这种平仓委托,就是暂时记录下，马上要踢掉
        tradeo = tradeOrder(gmOrderObj.cl_ord_id, gmOrderObj.symbol, gmOrderObj.volume, \
                            gmOrderObj.side, ORDER_TYPE.MARKET, gmOrderObj.position_effect,'sbname')

        if gmOrderObj.status == 3:
            tradeo.gm_filled_volume=gmOrderObj.filled_volume
            tradeo.gm_filled_vwap = gmOrderObj.filled_vwap
        self.addClearOrder(tradeo)


    def _create_trade_order_fromGmOrders(self,gmOrderObj,signalName):

        tradeo = tradeOrder(gmOrderObj.cl_ord_id, gmOrderObj.symbol, gmOrderObj.volume, \
                            gmOrderObj.side, ORDER_TYPE.MARKET, gmOrderObj.position_effect,signalName)

        if gmOrderObj.status == 3:
            tradeo.gm_filled_volume=gmOrderObj.filled_volume
            tradeo.gm_filled_vwap = gmOrderObj.filled_vwap
        self.addTradeOrder(tradeo)



        return  tradeo

    # def create_stop_loss_order(self,atradeOrder,stopLossThresh):
    #
    #     # assert atradeOrder.status == ORDER_STATUS.FILLED
    #     if atradeOrder.status == ORDER_STATUS.FILLED:
    #         aOrderPosition = OrderHoldingPostion(atradeOrder)
    #         o = stop_loss_by_order(aOrderPosition, 'percent', stopLossThresh)
    #         self.addStopOrder(o)
    #         self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol)
    #
    #
    # def create_stop_profit_order(self,atradeOrder,stopProfitThresh):
    #
    #     # assert atradeOrder.status == ORDER_STATUS.FILLED
    #     if atradeOrder.status == ORDER_STATUS.FILLED:
    #         aOrderPosition = OrderHoldingPostion(atradeOrder)
    #         # o = stop_loss_by_order(aOrderPosition, 'percent', stopProfitThresh,)
    #         o = StopProfitOrder.__from_create__(aOrderPosition, 'percent', stopProfitThresh)
    #         self.addStopOrder(o)
    #         self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol)


    def create_stop_order(self,aOrderPosition,stopThresh,stopCommand='stoploss'):


        # if atradeOrder.status == ORDER_STATUS.FILLED:
        #     aOrderPosition = OrderHoldingPostion(atradeOrder)
        #     # o = stop_loss_by_order(aOrderPosition, 'percent', stopProfitThresh,)
        #     if stopCommand=='stoploss':
        #         o = StopLossOrder.__from_create__(aOrderPosition, 'percent', stopThresh)
        #     if stopCommand=='stopprofit':
        #         o = StopProfitOrder.__from_create__(aOrderPosition, 'percent', stopThresh)
        #     self.addStopOrder(o)
        #     self.addOrderPosition(aOrderPosition)
        #
        #     self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下

        underLySym=commonHelpBylw.getMainContinContract(aOrderPosition.symbol)
        orderLog = loggerHelpbylw.getFileLogger(self.bTestID + '-'+underLySym+'-orderlog',
                                            'log\\'+self.bTestID+'\\' + underLySym + '-orderRecord.txt',mode_='a')


       


        # o = stop_loss_by_order(aOrderPosition, 'percent', stopProfitThresh,)
        if stopCommand=='stoploss':
            o = StopLossOrder.__from_create__(aOrderPosition, 'percent', stopThresh,orderLog=orderLog)
        if stopCommand=='stopprofit':
            o = StopProfitOrder.__from_create__(aOrderPosition, 'percent', stopThresh,orderLog=orderLog)
        self.addStopOrder(o)


        # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下

    def create_trailing_order(self,aOrderPosition,trailing_type,trailingThresh,stop_type,stopThresh):

        # assert atradeOrder.status == ORDER_STATUS.FILLED
        # if atradeOrder.status == ORDER_STATUS.FILLED:

        underLySym = commonHelpBylw.getMainContinContract(aOrderPosition.symbol)
        orderLog = loggerHelpbylw.getFileLogger(self.bTestID + '-' + underLySym + '-orderlog',
                                                'log\\' + self.bTestID + '\\' + underLySym + '-orderRecord.txt',
                                                mode_='a')

        o = trailingOrder(aOrderPosition,stop_type,stopThresh,trailing_type,trailingThresh,orderLog=orderLog)

        self.addStopOrder(o)
            # self.addOrderPosition(aOrderPosition)

            # self.stoplossOrderCreatedEvent.emit(atradeOrder.symbol) #大概是订阅的tick函数要执行下


    def onClearOrder(self,clearGmOrderObj,clearPositionSignalNames):

        # for aSLOrder in self._stoploss_orders:
        #     aSLOrder.target_order_position.onClearOrder(clearGmOrderObj,clearSignalNames)

            # # #在掘金的回测环境中。直接委托就成交了。这种情况下，需要变更下tradeorder的状态
            # if clearGmOrderObj.status == 3:
            #     # 利用掘金的回测的order对象。来构造一个trade记录
            #     tradedict = {}
            #     tradedict['orderID'] = clearGmOrderObj.cl_ord_id
            #     tradedict['side'] = clearGmOrderObj.side
            #     tradedict['position_effect'] = clearGmOrderObj.position_effect
            #     tradedict['volume'] = clearGmOrderObj.volume
            #     tradedict['price'] = clearGmOrderObj.price
            #     tradedict['commission'] = 0
            #     tradedict['tax'] = 0
            #     # tradeo.fill(tradedict)
            #
            #     self.onTrade(tradedict)






        # # #在掘金的回测环境中。直接委托就成交了。这种情况下，需要变更下tradeorder的状态
        # if clearGmOrderObj.status == 3:
        #     # 利用掘金的回测的order对象。来构造一个trade记录
        #     tradedict=createTradeRecordFromGmorder(clearGmOrderObj)
        #     # tradeo.fill(tradedict)
        #
        #     self.onTrade(tradedict)
        for aOP in self.orderPostions:
            aOP.onClearOrder(clearGmOrderObj,clearPositionSignalNames)

        
                
            
        