# -*- coding: utf-8 -*-
"""
20200410 lw

"""
from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday


import pymongo
from datetime import timezone
from datetime import timedelta


#这个类从rqalpha搬过来的
class Positions(dict):
    def __init__(self, position_cls):
        super(Positions, self).__init__()
        self._position_cls = position_cls
        self._cached_positions = {}

    def __missing__(self, key):
        if key not in self._cached_positions:
            self._cached_positions[key] = self._position_cls(key)
        return self._cached_positions[key]

    def get_or_create(self, symbol,positionSide):

        key=symbol+'_'+str(positionSide)
        if key not in self:
            self[key] = self._position_cls(symbol,positionSide)
        return self[key]

    def getAPosition(self, symbol,positionSide):

        key=symbol+'_'+str(positionSide)
        if key not in self:
            return None
        return self[key]

    def add(self,position):
        key= position.getSymbol()+'_'+str(position.getPositionSide())
        self[key]=position

#lw 李文 添加
###委托的持仓，即某笔开仓委托  对应的持仓。

class cusHoldingPostion():

    def __init__(self, symbol, positionSide):

        self._symbol = symbol
        self._positionSide = positionSide  #int
        self._volume = 0
        self._vwap = 0

        #这2个时间限制为datetime形式。
        self._created_at = None
        self._updated_at = None

        # 这个是可用持仓，比如原始持仓4收，被平仓order占了3收，但是还没成交，此时虽然总手数还是4收，但是可用的只有1手
        #这个参数暂时不自己计算，外部来赋值把
        self._available=None
    # @classmethod
    # def __from_create__(cls, symbol, positionSide, volume,vwap,created_at,updated_at):
    #     aorderPosition = cls()
    #
    #     aorderPosition.positionSide = positionSide
    #
    #     aorderPosition.symbol = symbol
    #     aorderPosition.volume = volume
    #     aorderPosition.vwap = vwap
    #
    #     aorderPosition.created_at = created_at
    #     aorderPosition.updated_at = updated_at
    #     return aorderPosition
    def set_state(self, state):
        self._volume = state.get("volume", 0)
        self._vwap = state.get("vwap",0)
        self._created_at = state.get("created_at")
        self._updated_at = state.get("updated_at")
        self._available = state.get("available")


    def getAvailableVolume(self):
        return self._available

    def getVolume(self):
        return self._volume

    def getSymbol(self):
        return self._symbol
    def getPositionSide(self):
        return self._positionSide
    def getVwap(self):
        return self._vwap
    def getUpdateTime(self):
        return self._updated_at
    def ontrade(self,cusTrade):

        symbol_ = cusTrade.getSymbol()
        side_ = cusTrade.getSide()
        vol_ = cusTrade.getVolume()
        price_ = cusTrade.getPrice()
        time_ = cusTrade.getTradeTime()

        if self._created_at is None:
            self._created_at=cusTrade.getTradeTime()
        self._updated_at = cusTrade.getTradeTime()


        # 如果是平仓指令，则需要减去持仓
        if cusTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
                                      PositionEffect_CloseYesterday]:

            assert self._symbol==symbol_
            if side_==1:
                assert self._positionSide==2
            if side_==2:
                assert self._positionSide==1


            assert self._volume>=vol_

            self._volume=self._volume-vol_

        if cusTrade.getPositionEffect() in [PositionEffect_Open]:

            assert self._symbol == symbol_
            assert self._positionSide == side_

            if self._volume < 0:
                print('error in positions class')
            else:
                self._vwap = (self._vwap * self._volume+ price_ * vol_) / (self._volume + vol_)
                self._volume=self._volume+vol_


class mongoPosition():
    #=dbname='real_short_period',collectionname='holding'
    def __init__(self, dbname,collectionname,host='localhost'):
        client = pymongo.MongoClient(host=host, port=27017,tz_aware=True)
        db = client[dbname]
        self.collection = db[collectionname]

    def ontrade(self,gmTrade):

        symbol_ = gmTrade.getSymbol()
        side_ = gmTrade.getSide()
        vol_ = gmTrade.getVolume()
        price_ = gmTrade.getPrice()
        time_ = gmTrade.getTradeTime()
        #如果是平仓指令，则需要减去持仓

        psitionSide=gmTrade.getTargetPositionSide()
        idstr = symbol_ + '_' + str(psitionSide)


        if gmTrade.getPositionEffect() in [PositionEffect_Close, PositionEffect_CloseToday,
                                      PositionEffect_CloseYesterday]:

            # symbol_ = gmTrade['symbol']
            # side_ = gmTrade['side']
            # vol_=gmTrade['volume']

            # if side_==1: #说明是买平.就需要查找空头持仓
            #     idstr=symbol_+'_2'
            # if side_==2: #说明是卖平.就需要查找多头 持仓
            #     idstr = symbol_ + '_1'



            # self.collection.update({'_id':idstr},{'$inc':{"vol":-vol_},'$set':{'updated_at':time_}})
            self.collection.update({'_id': idstr}, {'$inc': {"vol": -vol_}})
            self.collection.remove({'vol': 0})  #如果持仓为0了，就剔除掉该持仓。

        if gmTrade.getPositionEffect() in [PositionEffect_Open]:


            # if side_ == 1:  # 说明是买开.就需要查找多头持仓
            #     idstr = symbol_ + '_1'
            # if side_ == 2:  # 说明是卖开.就需要查找空头 持仓
            #     idstr = symbol_ + '_2'

            currHolding=self.collection.find_one({'_id':idstr})

            if currHolding is not None:
                newVwap=(currHolding['vwap']*abs(currHolding['vol'])+ price_*vol_)/(abs(currHolding['vol'])+vol_)
                self.collection.update({'_id': idstr}, {'$set': {"vwap": newVwap,'updated_at':time_},'$inc':{'vol':vol_,'available':vol_}})
            else:
                adoc={}
                adoc['_id']=idstr
                adoc['vwap'] = price_
                adoc['vol'] = vol_
                adoc['created_at'] = time_
                adoc['updated_at'] = time_
                adoc['available'] = vol_
                self.collection.insert(adoc)

        # if 'CZCE.CF009' == symbol_:
        #     print(symbol_,' ',side_,' ',gmTrade.getPositionEffect(),' ',vol_,' ',time_)
        #     long_=self.getHolding(symbol_,'1')
        #     if long_ is not None:
        #         print('持仓',' ',long_.getSymbol(),' ',long_.getPositionSide(),' ',long_.getVolume(),' ',long_.getUpdateTime())
        #     short_ = self.getHolding(symbol_, '2')
        #     if short_ is not None:
        #         print('持仓',' ',short_.getSymbol(), ' ', short_.getPositionSide(), ' ', short_.getVolume(),' ',short_.getUpdateTime())
    def clearAll(self):
        self.collection.delete_many({})
    #获取单个持仓
    def getHolding(self,symbol,poside,timeZoneNum=8):
        #poside 必须是字符串的1或者2
        idstr = symbol + '_'+poside
        currHolding = self.collection.find_one({'_id': idstr})
        if currHolding is not None:
            idstr=currHolding['_id']

            symbol_,positionSide=idstr.split('_')
            positionSide=int(positionSide)
            volume=currHolding['vol']
            vwap = currHolding['vwap']
            if currHolding['created_at'] is not None:
                created_at = currHolding['created_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
                updated_at = currHolding['updated_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            else:
                created_at = currHolding['created_at']
                updated_at = currHolding['updated_at']
            available=currHolding['available']
            state={}
            state["volume"]=volume
            state["vwap"]=vwap
            state["created_at"] = created_at
            state["updated_at"] = updated_at
            state["available"] = available
            ahol=cusHoldingPostion(symbol,positionSide)
            ahol.set_state(state)
            return ahol
     #内部函数，从mongo的持仓转换为内存中通用的持仓对象。
    def _trasfer(self,mongoHolding,timeZoneNum):
        idstr = mongoHolding['_id']

        symbol_, positionSide = idstr.split('_')
        positionSide = int(positionSide)
        volume = mongoHolding['vol']
        vwap = mongoHolding['vwap']
        if mongoHolding['created_at'] is not None:
            created_at = mongoHolding['created_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            updated_at = mongoHolding['updated_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
        else:
            created_at = currHolding['created_at']
            updated_at = currHolding['updated_at']
        available=mongoHolding['available']
        state = {}
        state["volume"] = volume
        state["vwap"] = vwap
        state["created_at"] = created_at
        state["updated_at"] = updated_at
        state["available"] = available
        ahol = cusHoldingPostion(symbol_, positionSide)
        ahol.set_state(state)
        return ahol
    #获取全部持仓
    def getPositions(self,timeZoneNum=8):
        holdings = self.collection.find()
        positionsObj=Positions(cusHoldingPostion)
        for ahol in holdings:
            commonHolding=self._trasfer(ahol,timeZoneNum)
            positionsObj.add(commonHolding)
        return  positionsObj

    # 获取全部持仓 返回df
    def getPositionsDf(self, timeZoneNum=8):
        cursor = self.collection.find()
        import  pandas as pd
        df = pd.DataFrame(list(cursor))

        df = df.sort_values(by='created_at')
        return  df

    def setAvailableVolume(self, symbol,poside,availVol):
        idstr = symbol + '_' + str(poside)
        self.collection.update({'_id': idstr}, {'$set': {'available': availVol}})

    def addPositions(self,positionsList):
        if len(positionsList)>0:
            self.collection.insert(positionsList)
