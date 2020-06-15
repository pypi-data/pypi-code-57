# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 16:12:37 2018

@author: SH
"""

# from sqlalchemy import create_engine
import pandas as pd



import sys
#sys.path.append('E:\myquant\gm3')
sys.path.append("E://sihuanlw4SVN//framework")
#sys.path.append("E://sh")


#import gm3HelpBylw
#import commonHelpBylw

import logging
import re
import numpy as np
from pyalgotrade import calendayBylw


#国内期货的 每日结束时间，每日开始时间
# FUTURES_CN_Day_STARTTIME_ENDTIME={
#     "SHFE.RB":("21:00:00","15:00:00"),
#     "CZCE.TA":("21:00:00","15:00:00"),
# "DCE.M":("21:00:00","15:00:00"),
# "CZCE.MA":("21:00:00","15:00:00"),
# "SHFE.AG":("21:00:00","15:00:00"),
# "SHFE.NI":("21:00:00","15:00:00"),
# "SHFE.BU":("21:00:00","15:00:00"),
# "SHFE.FU":("21:00:00","15:00:00")
# }

# FUTURES_CN_Day_STARTTIME_ENDTIME=("21:00:00","15:00:00")
FUTURES_CN_Day_STARTTIME_N001="21:00:00" #正常情况下，品种的日内开始时间
FUTURES_CN_Day_STARTTIME_N002="09:00:00" #那种节假日（不是双休的节假日，是那种国庆，中秋的节假日），品种的日内开始时间9点。

FUTURES_CN_Day_ENDTIME="15:00:00"



FUTURES_CN_SYMNAME_MAP_SYMID={
    '沪深主连':'CFFEX.IF',
    '上证主连':'CFFEX.IH',
    '中证主连':'CFFEX.IC',
    '债五主连':'CFFEX.TF',
    '债十主连':'CFFEX.T',

    '债二主连':'CFFEX.TS',
    '沪铜主连':'SHFE.CU',
    '沪金主连':'SHFE.AU',
    '沪银主连':'SHFE.AG',
    '沪锌主连':'SHFE.ZN',

    '沪铝主连':'SHFE.AL',
    '橡胶主连':'SHFE.RU',
    '螺纹主连':'SHFE.RB',
    '燃油主连':'SHFE.FU',
    '热卷主连':'SHFE.HC',

    '沥青主连':'SHFE.BU',
    '沪铅主连':'SHFE.PB',
    '沪镍主连':'SHFE.NI',
    '沪锡主连':'SHFE.SN',
    '线材主连':'SHFE.WR',

    '原油主连':'INE.SC',
    '豆一主连':'DCE.A',
    '豆二主连':'DCE.B',
    '玉米主连':'DCE.C',
    '淀粉主连':'DCE.CS',

    '纤板主连':'DCE.FB',
    '铁矿主连':'DCE.I',
    '焦炭主连':'DCE.J',
    '鸡蛋主连':'DCE.JD',
    '焦煤主连':'DCE.JM',

    '塑料主连':'DCE.L',
    '豆粕主连':'DCE.M',
    '棕榈主连':'DCE.P',
    'PP主连':'DCE.PP',
    'PVC主连':'DCE.V',
    
    '豆油主连':'DCE.Y',
    '棉花主连':'CZCE.CF',
    '棉纱主连':'CZCE.CY',
    '白糖主连':'CZCE.SR',
    'PTA主连':'CZCE.TA',

    '菜油主连':'CZCE.OI',
    '甲醇主连':'CZCE.MA',
    '玻璃主连':'CZCE.FG',
    '菜粕主连':'CZCE.RM',
    '郑煤主连':'CZCE.ZC',

    '粳稻主连':'CZCE.JR',
    '晚稻主连':'CZCE.LR',
    '硅铁主连':'CZCE.SF',
    '锰硅主连':'CZCE.SM',
    '苹果主连':'CZCE.AP',

    '铁矿':'DCE.I',
    '苹果':'CZCE.AP',
    '甲醇':'CZCE.MA',
    '螺纹':'SHFE.RB',
    '镍':'SHFE.NI',
    '白糖':'CZCE.SR',
    'PTA':'CZCE.TA',
    '棉花':'CZCE.CF',
    '橡胶':'SHFE.RU',
    '豆油':'DCE.Y',
    '燃料油':'SHFE.FU',
    '原油':'INE.SC',
    'PP':'DCE.PP',
    'EG':'DCE.EG',
    '焦炭':'DCE.J',
    '冶金焦炭':'DCE.J',
    '白银':'SHFE.AG',
    '纸浆':'SHFE.SP',
    '沥青':'SHFE.BU',
    '鸡蛋':'DCE.JD',
    '豆粕':'DCE.M',
    '玉米':'DCE.C',
    '动力煤':'CZCE.ZC',
    '锰硅':'CZCE.SM',
    'IC':'CFFEX.IC',
    'IF':'CFFEX.IF',
    'IH':'CFFEX.IH'

}



STOCKS_CN_SYMNAME_MAP_SYMID={
    '300ETF':'SHSE.510300',
    '500ETF':'SHSE.510500',
    '标普500':'SHSE.513500',
    '纳指ETF':'SHSE.513100',
    '创业板50':'SZSE.159949'
}


def splitASymbol(aSymbol):
     
    atemp=aSymbol.split('.')
    exchange=atemp[0]
    secID=atemp[1]
    secSymbol=''
    secYear=''
    secMonth=''
    secDict={}
 
    if exchange=='CZCE' or exchange=='SHFE':
        secSymbol=secID[0:2]
        secMonth=secID[-2:]
        
        
 
    if exchange=='DCE':
        if secID[0:2] in ['jm','jd','cs','pp']:

            secSymbol=secID[0:2]
            secMonth=secID[-2:]
        elif  secID[0:1] in ['a','c','i','j','l','m','p','v','y']:
            secSymbol=secID[0:1]
            secMonth=secID[-2:]

    if exchange == 'CFFEX':
        if secID[0:2] in ['IC', 'IH', 'IF','TF']:

            secSymbol = secID[0:2]
            secMonth = secID[-2:]
        elif secID[0:1] in ['T']:
            secSymbol = secID[0:1]
            secMonth = secID[-2:]

#        if row['exchange']=='SHFE':
#            i=1
#            
#        if  currVirtualContract in month159CZCE+month159DCE+month159SHFE:
#            if row['sec_id'][-2:] in ['01','05','09']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month123456SHFE:
#            if row['sec_id'][-2:] in ['01','02','03','04','05','06']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month1510SHFE:
#            if row['sec_id'][-2:] in ['01','05','10']:
#                finalContract.append(row['symbol'])
#        if  currVirtualContract in month612SHFE:
#            if row['sec_id'][-2:] in ['06','12']:
#                finalContract.append(row['symbol'])

    secYear=secID.replace(secSymbol,'').replace(secMonth,'')
    
#    secList.append(exchange+'.'+secSymbol)
#    secList.append(secYear)
#    secList.append(secMonth)
    
    secDict['secSymbol']=exchange+'.'+secSymbol
    secDict['secYear']=secYear
    secDict['secMonth']=secMonth
    import datetime
    strtime=datetime.datetime.now().strftime('%Y-%m-%d')
    if exchange=='CZCE':

        strNext1Year=str(int(strtime[0:4])+1)
        strNext2Year = str(int(strtime[0:4]) + 2)


        if strtime[3]==secYear:
            secDict['secRealYear']=strtime[2]+secYear
        if strNext1Year[3]==secYear:
            secDict['secRealYear']=strNext1Year[2]+secYear
        if strNext2Year[3] == secYear:
            secDict['secRealYear'] = strNext2Year[2] + secYear

    else:
        secDict['secRealYear']=secYear
    return secDict




def juejinSymbol(x):
	return 'SHSE.'+x if x[0] in ['5','6'] else 'SZSE.'+x 





# 将不太合规的代码，补充完整 
def adjustSymbol(aSym):
    
    #.表示存在交易所写法
    
    if '.' in aSym:
        
        splitSym=aSym.split('.')
        if 'DCE' in aSym or 'SHFE' in aSym:
            adjustSym=splitSym[0]+'.'+splitSym[1].lower()
            return adjustSym
        if 'CZCE' in aSym or 'CFFEX' in aSym:
            adjustSym=splitSym[0]+'.'+splitSym[1].upper()
            return adjustSym 
        
        if 'SHF' in aSym:
            adjustSym=splitSym[0]+'E.'+splitSym[1].lower()
            return adjustSym
        if 'CZC' in aSym:
            adjustSym=splitSym[0]+'E.'+splitSym[1].upper()
            return adjustSym


def reverseExchangeAndSecID(aSymbol):
    splitSym=aSymbol.split('.')
    return splitSym[1]+'.'+splitSym[0]

def adjustExchangeName(oldName):
    if oldName=='郑商所':
        return 'CZCE'
    if oldName=='大商所':
        return 'DCE'
    if oldName=='上期所':
        return 'SHFE'
    if oldName=='中金所':
        return 'CFFEX'
    if oldName=='能源中心':
        return 'INE'
    assert 2==1,'strage exchangeName'
    
def symNameToSymID(symName):
    adict={}
    adict.update(FUTURES_CN_SYMNAME_MAP_SYMID)
    adict.update(STOCKS_CN_SYMNAME_MAP_SYMID)
    return adict[symName]


# 只有合约，没有交易所代码，所以增加下交易所代码
def addExchange(aSymbol):
     #26个

    instruments4CZCE=['TA','SR','CF','OI','MA',
                      'FG','RM','ZC','SF','SM','AP',
                      'ER','RO','WS','ME','WH',
                      'TC','WT','PM','RI','LR',
                      'JR','CY','RS','GN','UR']
    
    #18个
    instruments4DCE=['A','B','C','CS','I','J',
                      'JD','JM','L','M','P',
                      'PP','V','Y','FB','EG',
                     'EB','RR']
    
    #14个
    instruments4SHFE=['AL','BU','CU','SN','ZN',
                      'HC','NI','PB','RB','RU',
                      'AG','AU','FU','WR','SP']

     # 2个
    instruments4INE=['SC','NR']
     # 5个
    instruments4CFFEX=['IC','IH','IF','T','TF']
    
    adjustSym=aSymbol.upper()
    
    fianSymbol=aSymbol
    if adjustSym[0:2] in instruments4CZCE:
        if len(adjustSym[2:])==4:#如果数字部分有4位，比如cf1305这种，必须去掉1，变成cf305
            fianSymbol='CZCE.'+aSymbol[0:2].upper()+adjustSym[3:]
        else: 
            
            fianSymbol='CZCE.'+aSymbol.upper()
    else:
        if adjustSym[0:2] in instruments4SHFE:
            fianSymbol='SHFE.'+aSymbol.lower()
        else:
            if adjustSym[0:2] in instruments4INE:
                fianSymbol='INE.'+aSymbol.lower()
            else:
               if adjustSym[0:2] in instruments4CFFEX:
                   fianSymbol='CFFEX.'+aSymbol.upper() 
               else:
                   if adjustSym[0:1] in instruments4CFFEX:
                       fianSymbol='CFFEX.'+aSymbol.upper() 
                   else:
                       if adjustSym[0:2] in instruments4DCE:
                           fianSymbol='DCE.'+aSymbol.lower() 
                       else:
                           if adjustSym[0:1] in instruments4DCE:
                               fianSymbol='DCE.'+aSymbol.lower() 
    return fianSymbol



def removeExchange(aSymbol):
    adjSymbol=aSymbol.split('.')
    return adjSymbol[1]

'''

获取指定时间段内，在 上市交易的 期权品种。

'''

def getOptionContractsBylw(sDateTime,eDateTime):
    
    
    
    engine = create_engine('mysql+pymysql://admin:admin@192.168.10.81:3306/option?charset=utf8',encoding='utf-8')


    optionSymbolsINfo=pd.read_sql("SELECT * FROM optionContractBasicInfo",engine)
    
    
    if sDateTime and eDateTime:
        optionSymbolsINfo=optionSymbolsINfo\
        [~((optionSymbolsINfo['listed_date']>eDateTime)|\
         (optionSymbolsINfo['expire_date']<sDateTime))]

    return list(optionSymbolsINfo['wind_code'].values)
    
                 
                 



def contracts4wangzong():
    
    #准备品种数据
    
     #王总指定的33个交易品种
    
         #王总指定的33个交易品种
        
    #11个
    instruments4CZCE=['CZCE.TA','CZCE.SR','CZCE.CF','CZCE.OI','CZCE.MA',
                      'CZCE.FG','CZCE.RM','CZCE.ZC','CZCE.SF','CZCE.SM','CZCE.AP']
    
    #13个
    instruments4DCE=['DCE.A','DCE.B','DCE.C','DCE.CS','DCE.I','DCE.J',
                      'DCE.JD','DCE.JM','DCE.L','DCE.M','DCE.P',
                      'DCE.PP','DCE.V','DCE.Y']
    
    #12个
    instruments4SHFE=['SHFE.AL','SHFE.BU','SHFE.CU','SHFE.SN','SHFE.ZN',
                      'SHFE.HC','SHFE.NI','SHFE.PB','SHFE.RB','SHFE.RU','SHFE.AG','SHFE.AU']
    
    
    instruments4INE=['INE.SC']
    
    instruments4CFFEX=['CFFEX.IC','CFFEX.IH','CFFEX.IF','CFFEX.T','CFFEX.TF']
    
    return instruments4CZCE+instruments4DCE+instruments4SHFE+instruments4INE+instruments4CFFEX


# 获取连续合约的的代码
def getFullSymbolName(astrList):
    
    resuList=[]
    cList=contracts4wangzong()
    for acStr in astrList:
        for aSy in cList:
            if  acStr in aSy:
                resuList.append(aSy)
                break
    return resuList


#返回 标的类别

# SEC_TYPE_STOCK = 1                          # 股票
# SEC_TYPE_FUND = 2                           # 基金
# SEC_TYPE_INDEX = 3                          # 指数
# SEC_TYPE_FUTURE = 4                         # 期货
# SEC_TYPE_OPTION = 5                         # 期权
# SEC_TYPE_CONFUTURE = 10                     # 虚拟合约
def getSecType(asymbol):

    secID=asymbol.split('.')[0]
    if secID=='SHSE' or secID=='SZSE':
        return 'stock_cn'
    if secID=='DCE' or secID=='CZCE' or secID=='SHFE':
        return 'future_cn'
    i=1


# 将DCE.a1901的这种具体合约 变换成 DCE.A这种主力合约表示法。   
def getMainContinContract(aSymbol):
    
    
#    cList=contracts4wangzong()
#    adjustSymbol=aSymbol.upper()
#    ss=adjustSymbol.split('.')
#    exchange=ss[0]
#    contract=ss[1]
#    
#    
#    concateStr1=exchange+'.'+contract[0:1]
#    concateStr2=exchange+'.'+contract[0:2]
#    
#    if concateStr1 in cList:
#        return concateStr1
#    else:
#        if concateStr2 in cList:
#            return concateStr2
    if aSymbol ==np.nan:
        return np.nan
    noDigit=re.sub(r'\d+','',aSymbol)
    
    return noDigit.upper()


'''

指定日期 回溯n 个bar的数据

如果是取掘金中的数据，其提供了个函数直接调用
history_n - 查询历史行情最新n条


'''
#current_date = datetime.datetime.now().strftime('%Y-%m-%d')
#
##current_date='2018-05-16'
#
#astartTime=current_date
#aendTime=current_date
#
#
#lenShort=5
#
#currDT=datetime.datetime.strptime(current_date, "%Y-%m-%d")
#aPlotStartTime=(currDT+DateOffset(years=-5)).to_pydatetime()
#aPlotEndTime=currDT
#
#
#
#optionInfo=commonHelpBylw.getOptionContractsBylw(astartTime,aendTime)
#
#
#i=0
#for aOption in optionInfo:
##   
#    #这个sql语句是关键语句
##    
#    
#    optionSymbolsINfo=pd.read_sql("SELECT * FROM optionHistDayHQ where TRADE_CODE='%s' and Date<='%s' order by Date desc limit %d"%(aOption,aendTime,lenShort),engine)
#    optionSymbolsINfo.sort_values(by=['Date'], ascending=[True], inplace=True)
#    
#    close = optionSymbolsINfo['CLOSE'].values
#    maShort=  talib.MA(optionSymbolsINfo['CLOSE'].values, timeperiod=lenShort, matype=0)
#    
#    
#    optionSymbolsINfo=pd.read_sql("SELECT * FROM optionContractBasicInfo where wind_code='%s'"%(aOption),engine)
#    
#    optionName=optionSymbolsINfo.iloc[0]['sec_name']
#    if close[-1]-maShort[-1]>4*maShort[-1]:
#        print(aOption,' ',optionName,' higher 5 times ma')
#    if close[-1]-maShort[-1]<-4*maShort[-1]:
#        print(aOption,' ',optionName,' lower 5 times ma')
    





def runAQQ(who,msg):
    import win32gui
    import win32con
    import win32clipboard as w
    
    def getText():
        """获取剪贴板文本"""
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_UNICODETEXT)
        w.CloseClipboard()
        return d
    
    def setText(aString):
        """设置剪贴板文本"""
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        w.CloseClipboard()
    
    
    # QQ群发送消息
#    to_who1 =   'Dominique'
    #to_who1 = u'QQ好友的备注名称'  # 接收消息qq的备注名称(该好友对话框单独打开，最小化)
#    content = u"流氓！"#要发送的消息
    to_who1 =who
    content = '机器人信息:'+msg
    
    setText(content)
    qqhd = win32gui.FindWindow(None, to_who1)
    print(qqhd)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qqhd, 258, 22, 2080193)
    win32gui.SendMessage(qqhd, 770, 0, 0)
    # 模拟按下回车键
    win32gui.SendMessage(qqhd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qqhd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)







"""

存储一些不适合做成函数的代码



1 取交易日的某一年第一个交易日，最后 一个交易日
businessday_list = rdataFetch.get_businessday()
daySeries=pd.Series(businessday_list)
daySeries=daySeries.sort_values()
astartdt=daySeries.loc[daySeries>'2017'].iloc[0]
aenddt=daySeries.loc[daySeries<'2018'].iloc[-1]





2  掘金中的交易的 固定逻辑

#交易1  不能开空头仓位

#如果某个品种要求开多，本来如果有空头，要先平仓空头，再开多，但是股票里面不能有空头，所以直接就开多
#如果某个品种要求开空 ，本来如果有多头，则先平多头，再开空，股票不能有空头，所以一般都是直接平多。
for aCode in tradeDict:
    if tradeDict[aCode]>0:
        order_target_volume(symbol=aCode, volume=tradeDict[aCode], \
                            position_side=PositionSide_Long, \
                            order_type=OrderType_Market, price=13)
    else:
        # 
        order_target_volume(symbol=aCode, volume=0, \
                            position_side=PositionSide_Long, \
                            order_type=OrderType_Market, price=13)
        
                
                
#交易2 可以开空头仓位

for aCode in tradeDict:
    if tradeDict[aCode]>0:
        
        if context.account().position(symbol=aCode, side=PositionSide_Short):
            order_target_volume(symbol=aCode, volume=0, \
                            position_side=PositionSide_Short, \
                            order_type=OrderType_Market, price=13)
            
        order_target_volume(symbol=aCode, volume=tradeDict[aCode], \
                            position_side=PositionSide_Long, \
                            order_type=OrderType_Market, price=13)
    else:
        # 
        if context.account().position(symbol=aCode, side=PositionSide_Long):
            order_target_volume(symbol=aCode, volume=0, \
                            position_side=PositionSide_Long, \
                            order_type=OrderType_Market, price=13)
        order_target_volume(symbol=aCode, volume=-tradeDict[aCode], \
                            position_side=PositionSide_Short, \
                            order_type=OrderType_Market, price=13)
        




3准备合法的起始时间 和结束时间


# 准备回测要求的起始时间和结束时间。
currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
currDate = currDateTime[0:10]

aSTimeStr='08:00:00'
aeTimeStr='16:00:00'

# aSTimeStr=currDateTime[10:]
# aeTimeStr=currDateTime[10:]

m1dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
       + DateOffset(years=-1,months=-3)
m1dtStr = m1dt.strftime('%Y-%m-%d')

m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
       + DateOffset(days=-2)
m2dtStr = m2dt.strftime('%Y-%m-%d')




# 建立一个假期日历
nextYearofToday= datetime.datetime.strptime(currDate, '%Y-%m-%d') \
       + DateOffset(years=1)
nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)


backTestsDateT = aNewTradeCalendar.mDatesOffset(m1dtStr, yoffset=0) + ' '+aSTimeStr
backTesteDateT = aNewTradeCalendar.mDatesOffset(m2dtStr, yoffset=0) + ' '+aeTimeStr



#时间间隔
具体见笔记
datetime.datetime.now() - datetime.timedelta(minutes=15)


"""




def btStartEndDates():
    import time
    import datetime

    # 准备回测要求的起始时间和结束时间。
    currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDate = currDateTime[0:10]

    aSTimeStr = '08:00:00'
    aeTimeStr = '16:00:00'

    # aSTimeStr=currDateTime[10:]
    # aeTimeStr=currDateTime[10:]

    m1dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
           + DateOffset(years=-1, months=-3)
    m1dtStr = m1dt.strftime('%Y-%m-%d')

    m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
           + DateOffset(days=-2)
    m2dtStr = m2dt.strftime('%Y-%m-%d')

    # 建立一个假期日历
    nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
                      + DateOffset(years=1)
    nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
    aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
    aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)

    backTestsDateT = aNewTradeCalendar.mDatesOffset(m1dtStr, yoffset=0) + ' ' + aSTimeStr
    backTesteDateT = aNewTradeCalendar.mDatesOffset(m2dtStr, yoffset=0) + ' ' + aeTimeStr

    # hisDataSDateT=aNewTradeCalendar.mDatesOffset(m2dtStr,yoffset=0)+currDateTime[10:]
    maxLen = 60
    barsNum = 3






#concretePositionDict 这玩意必须是明细持仓，及不是传统的那种将相同品种，相同
#方向 合并一起算的那种，而是每笔开仓交易 导致的持仓，当然有些开仓交易 还会因为平仓交易被删除掉
def updateMFE(aOrderMFEdict,basicBar_):
    assert aOrderMFEdict is not None
    assert basicBar_ is not None

    posi=aOrderMFEdict['orderPosition']



    if posi.barsSinceEntry>0:
        if posi.barsSinceEntry==1:
            aOrderMFEdict['HH']=basicBar_.getHigh()
            aOrderMFEdict['LL'] = basicBar_.getLow()
        else:
            aOrderMFEdict['HH'] = max(aOrderMFEdict['HH'],basicBar_.getHigh())
            aOrderMFEdict['LL'] = min(aOrderMFEdict['LL'],basicBar_.getLow())


        if posi.positionSide == 'long':
            aOrderMFEdict['MFE'] = aOrderMFEdict['HH'] - posi.cost

        if posi.positionSide == 'short':
            aOrderMFEdict['MFE'] = posi.cost-aOrderMFEdict['LL']




#
#
# class customTradeCalendar:
#
# 	#tradingDays 必须是字符串 list。即使一个list ，然后每个成员都是一个字符串
#     def __init__(self,tradingDays):	# 重载构造函数
#         sTradingDays = pd.Series(tradingDays,name='tradingDays')
#         sTradingDays=sTradingDays.sort_values()
#         self.sTradingDays = sTradingDays			# 创建成员变量并赋初始值
#     def __del__(self):      		# 重载析构函数
#         pass				# 空操作
#
#
# #    def getMonthDays(self,date,offset):
# #        rdataFetch = rdata.RData()
# #        businessday_list = rdataFetch.get_businessday()
# #        daySeries=pd.Series(businessday_list)
# #        daySeries=daySeries.sort_values()
# #        astartdt=daySeries.loc[daySeries>'2013'].iloc[0]
# #        aenddt=daySeries.loc[daySeries<'2014'].iloc[-1]
#
#     #date 必须是字符串形式
#     def mDatesOffset(self,date,yoffset=0,moffset=0,doffset=0):
#
#
#         from pandas.tseries.offsets import DateOffset
#         import datetime
#         newDate=datetime.datetime.strptime(date,'%Y-%m-%d')\
#             + DateOffset(years=yoffset,months=moffset, days=doffset)
#         strNewDate=newDate.strftime('%Y-%m-%d')
#
#
#
#         # 即表示，如果当前日期date  要找一个偏移日期
#         #如果是左偏的日期，那么就是往日期大的选，如果是右偏日期，就往日期小的选，总之，要让日期更靠近基准日期date
#         if strNewDate<date:
#
#             aRDate=self.sTradingDays.loc[self.sTradingDays>=strNewDate].iloc[0]
#         else:
#             aRDate=self.sTradingDays.loc[self.sTradingDays<=strNewDate].iloc[-1]
# #        print(aRDate)
#         return aRDate
#
#
#     #本函数用来 推断 交易日的上一个交易日，下一个交易日等行为。
#     def tradingDaysOffset(self,date,aoffset):
#
#         if aoffset>0:
#
#             return self.sTradingDays.loc[self.sTradingDays>date].iloc[0]
#         if aoffset<0:
#
#             return self.sTradingDays.loc[self.sTradingDays<date].iloc[-1]
#         if aoffset==0:
#
#             return date
#
#
#     def getADateTimeSeries(self,startDt,endDt):
#         return self.sTradingDays.loc[(self.sTradingDays>=startDt)&(self.sTradingDays<=endDt)]
#
#     import os
#     import shutil




def copyFiles2(sourceDir, targetDir,filename=None):
    import os
    import shutil

    if sourceDir.find("exceptionfolder") > 0:
        return

    if filename:
        sourceFile = os.path.join(sourceDir, filename)
        targetFile = os.path.join(targetDir, filename)

        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (os.path.exists(targetFile) and (os.path.getsize(targetFile) !=
                                                                                  os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
                print(targetFile + " copy succeeded")

        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)
    else:
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, file)
            targetFile = os.path.join(targetDir, file)

            if os.path.isfile(sourceFile):
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                if not os.path.exists(targetFile) or (os.path.exists(targetFile) and (os.path.getsize(targetFile) !=
                                                                                      os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
                    print(targetFile + " copy succeeded")

            if os.path.isdir(sourceFile):
                copyFiles(sourceFile, targetFile)



def cusCopyFile(sourceDir, targetDir,filename=None):
    import os
    import shutil

    # if sourceDir.find("exceptionfolder") > 0:
    #     return

    ss=os.path.dirname(sourceDir)
    abDir=os.path.abspath(sourceDir)



    if filename:
        sourceFile = os.path.join(abDir, filename)
        # targetFile = os.path.join(targetDir, filename)
        # shutil.copy2(sourceFile, targetDir)
        os.system("copy %s %s" % (sourceFile, targetDir))
    else:
        for file in os.listdir(sourceDir):
            abDirFile = os.path.join(abDir, file)
            if os.path.isfile(abDirFile):
                # shutil.copy(file, targetDir)


                # os.system("copy /Y %s %s"%(dirFile,targetDir))
                os.system("copy %s %s" % (abDirFile, targetDir))




#日志

def writeLog2console(logInstance='aLogger',msg=None):
    import logging
    # 获取logger实例，如果参数为空则返回root logger
    loggerCons = logging.getLogger(logInstance)

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器
    loggerCons.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    loggerCons.setLevel(logging.INFO)

    loggerCons.info(msg)

def writeLog2File(logInstance='aLogger',logfile=None,msg=None):
    import logging
    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger(logInstance)

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # logfile = r'ma60AndBarslog\ma60Close_' + datetime.datetime.now().strftime('%Y-%m-%d %H%M%S') + '.txt'
    file_handler = logging.FileHandler(logfile, mode='w')

    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


    # msg="barStartTime:%s barEndTime:%s barSymbol %s close crossUP ma60 and %sbars",\
    #                                                 cBarSDateTime, cDateTime, self.symbol,str(self.barsNum)
    logger.info(msg)



def splitDates(sDateTime,eDateTime,step_=3000,moreDataFlag=False):
    #这玩意只能拆分日期，不能拆分出来时间。因为没有具体的时间日期 序列表。
    #sDateTime 可以只是日期。有可以是日期带时间


# def getSymboInfoDataFromGm(symbolList,sDateTime,eDateTime,fields=None,step_=3000):

    #aGmAPIfun 是掘金的提取数据的函数，可以是history，也可以是get_history_instruments，等等。反正是一次提取历史数据
    #不能太长的话，都可以用这里的这个函数包一层。



    from gm.api import get_trading_dates
    import time
    import datetime
    from pandas.tseries.offsets import DateOffset
    #准备一个 日历对象。
    currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDate = currDateTime[0:10]
    nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
                      + DateOffset(years=1)
    nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
    aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
    aNewTradeCalendar = calendayBylw.customTradeCalendar(aTradingDays)



    #起始日期 和 结束日期 分别往前 和 往后扩展一下。
    sDate=sDateTime[0:10]
    eDate=eDateTime[0:10]



    if moreDataFlag:
        #取数据多取了上下2天，为啥，其实就是比原始数据夺取了2天，不影响啥，还能解决掉各种边界问题，比如
        #可能你当前交易日的动作，需要下一个交易日来处理。但是按照规矩取数据，下一个交易日没取出来。
        ssDate=aNewTradeCalendar.mDatesOffset(sDate,doffset=-1,leftOrright=-1)
        eeDate = aNewTradeCalendar.mDatesOffset(eDate, doffset=1, leftOrright=1)
    else:
        #后来有用的时候，发现多取数据不好。带个标记，如果特别想要多取，则用标记来说明

        ssDate = aNewTradeCalendar.mDatesOffset(sDate, doffset=0, leftOrright=1)
        eeDate = aNewTradeCalendar.mDatesOffset(eDate, doffset=0, leftOrright=-1)

    atradeDateSerial=aNewTradeCalendar.getADateTimeSeries(ssDate,eeDate)

    datesList=[]

    sIndex=0
    eIndex=sIndex+step_-1
    while True:
        cSdate=atradeDateSerial.iloc[sIndex]
        if eIndex>=atradeDateSerial.shape[0]:
            cEdate=atradeDateSerial.iloc[-1]
        else:
            cEdate=atradeDateSerial.iloc[eIndex]

        datesList.append((cSdate,cEdate))
        if eIndex>=atradeDateSerial.shape[0]:
            break
        else:
            sIndex = sIndex+step_
            eIndex = eIndex + step_


    #如果是日期时间格式，即带有时间，那么首尾两个日期，最好加上各自的时间。


    atuple=datesList[0]
    datesList[0]=(atuple[0]+sDateTime[10:],atuple[1])

    atuple=datesList[-1]
    datesList[-1]=(atuple[0],atuple[1]+eDateTime[10:])

    return datesList





def dtToUnixTimeStamp(adt):
    ats = int(adt.timestamp() * 1000)
    return ats


def round_up(value,y):
    import math
    ss=math.pow(10, y)
    vs=round(value*ss)/float(ss)
    return vs

def isCrossDay(symbol,lastDT,currDT):


    #本来想，如果当前日期大于上一个日期，则肯定跨日了。但是
    #后来还想不对，比如周五到周一，周五的夜盘是周一的行情的一部分，此时周一的日期肯定大于
    #周五的日期，但是这个不能算跨日。
    # if currDT[0:10]>lastDT[0:10]:
    #     return True
    # else:

    lastDate=lastDT[0:10]
    currDate=currDT[0:10]

    lastTime=lastDT[11:]
    nowTime=currDT[11:]
    # mainContract=getMainContinContract(symbol)
    # symbolDaySDt,symbolDayEDt=SYMBOL_Day_STARTTIME_ENDTIME[mainContract]
    # symbolDaySDt, symbolDayEDt = FUTURES_CN_Day_STARTTIME_ENDTIME

    if lastDate==currDate and (lastTime <= FUTURES_CN_Day_ENDTIME and nowTime >=FUTURES_CN_Day_STARTTIME_N001) :  # 21:00的跨日
        return True


    #中秋等假日的9：00的跨日
    if lastDate<currDate and (lastTime <= FUTURES_CN_Day_ENDTIME and nowTime >=FUTURES_CN_Day_STARTTIME_N002) :  # 21:00的跨日
        return  True

    return False
    # i=1



# 读取csv文件的最后一行。csv文件可以是最后一行是空行的情况。
def readLastLine(filename,encoding='gbk'):
    # with open('hisRecord.CSV', 'rb') as hisRecordFile:
    with open(filename,'rb') as hisRecordFile:
        import os

        first = hisRecordFile.readline()
        nextbyte=hisRecordFile.read(1)
        if nextbyte==b'':
           last=first

        else:


            hisRecordFile.seek(-2, os.SEEK_END)  # Jump to the second last byte.


            while nextbyte!=b"\n":  # Until EOL is found...

                hisRecordFile.seek(-2, os.SEEK_CUR)  # ...jump back the read byte plus one more.
                nextbyte=hisRecordFile.read(1)



              
            last = hisRecordFile.readline()

        lastStr = last.decode(encoding)
        return lastStr.strip('\r\n')



def rangeLeftAndRight(avalue,step,stepCount):
#step 是步长
#stepcount 是需要几个步长

    aList=[]
    for i in range(1,stepCount+1):
        aList.append(avalue-i*step)
        aList.append(avalue + i * step)
    aList.append(avalue)
    return  sorted(aList)





import os
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是,当父目录不存在的时候os.mkdir(path)不会创建，os.makedirs(path)则会创建父目录
        '''
        #此处路径最好使用utf-8解码，否则在磁盘中可能会出现乱码的情况
        # os.makedirs(path.decode('utf-8'))

        os.makedirs(path)


