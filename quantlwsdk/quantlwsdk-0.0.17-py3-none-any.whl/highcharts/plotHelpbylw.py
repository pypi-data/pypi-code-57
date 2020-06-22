# -*- coding: utf-8 -*-

from .version import version_info, __version__

from .highcharts.highcharts import Highchart
from .highmaps.highmaps import Highmap
from .highstock.highstock import Highstock

from . import ipynb

import sys
sys.path.append(r'..\..')
from pyalgotrade.utils import gmEnum


from pyalgotrade import gm3HelpBylw
import json



def dftounixTimestamp(arow):
    adt = arow.to_pydatetime()
    ats = int(adt.timestamp() * 1000)
    return ats


def plotLine(dataDf,symbol_):
    ###javascript  画图
    #date 列必须是datetime 类型

    dataDf.columns=['date','close']

    # atooltipValue = {"pointFormatter": "function() {\n\
    #             var seriesOptions = this.series.options,\n\
    #             str = '<b>MACD (26, 12, 9)</b><br>';\n\
    #             function getLine(color, name, value){\n\
    #                 return '<span style=\"color:' + color + '\">\\u25CF</span> ' + name + ': <b>' + value + '</b><br/>';\n\
    #     }\n\
    #     str += getLine(seriesOptions.macdLine.styles.lineColor, 'diff', this.MACD.toFixed(2));\n\
    #     str += getLine(seriesOptions.signalLine.styles.lineColor, 'dea', this.signal.toFixed(2));\n\
    #     str += getLine(seriesOptions.color, 'macd', this.y.toFixed(2));\n\
    #     return str;\n\
    # }"}


    sttt="'abc'cced"

    atooltipValue ={"pointFormat": "\'<span style=\"color:{series.color}\">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>\',changeDecimals: 2,valueDecimals: 2"}

    # 构造H
    H =createAHStock(symbol_)
    H.set_options('plotOptions',{'series':{'compare':'percent'}})
    addASeries(H, dataDf, symbol_,tooltip=atooltipValue,marker={'enabled':True,"radius":5})

    return H


def plotSingleLine(dataDf,symbol_):
    ###javascript  画图
    #date 列必须是datetime 类型

    dataDf.columns=['date','close']


    # 构造H
    H =createAHStock(symbol_)

    addASeries(H, dataDf, symbol_,marker={'enabled':True,"radius":5})

    return H
def plotPoint(dataDf,symbol_):
    dataDf.columns = ['date', 'pValue']
    i=1

def createAHStock(symbol_):
    options = {
        'global': {
            'timezoneOffset': -8 * 60  # +8 时区修正方法
        },
        'rangeSelector': {
            'selected': 1
        },

        'plotOptions': {
            'series': {
                'turboThreshold': 100000,
                "states": {"inactive": {'opacity': 1}},
                "dataGrouping":{"enabled":False}

            }


        },

        'title': {
            'text': symbol_
        },
        'tooltip': {
            'crosshairs': [True, True],
            'xDateFormat': '%Y-%m-%d %H:%M:%S',
            'shared': True

        },
    }

    from win32api import GetSystemMetrics
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    divStyle = "min-width:100%%;min-height:%dpx" % (int(height * 0.8))
    H = Highstock(divstyle=divStyle)
    H.set_dict_options(options)

    return  H


def plotCandle(H,dataDf,symbol_):
    ###画蜡烛图

    #提供时间开高低收5个字段，最后转换成highchart中的 二维数组方式。这种方式在数据组织格式中有介绍。
    #dataDf中的date 列必须是 pandas中的timestamp的格式。即是pandas中的datetime



    dataDf.columns=['date','open','high','low','close']

    # options = {
    #     'global': {
    #          'timezoneOffset': -8 * 60  # +8 时区修正方法
    #     },
    #     'rangeSelector': {
    #         'selected': 1
    #     },
    #
    #     'plotOptions':{
    #         'series':{
    #             'turboThreshold':100000,
    #             "states": {"inactive": {'opacity': 1}}
    #
    #         }
    #     },
    #
    #     'title': {
    #         'text': symbol_
    #     },
    #     'tooltip': {
    #         'crosshairs': [True, True],
    #         'xDateFormat': '%Y-%m-%d %H:%M:%S',
    #         'shared': True
    #
    #     },
    # }
    #
    # from win32api import GetSystemMetrics
    # width=GetSystemMetrics(0)
    # height=GetSystemMetrics(1)
    #
    # divStyle="min-width:100%%;min-height:%dpx"%(int(height*0.8))
    # H = Highstock(divstyle=divStyle)

    adjustPE = dataDf.reset_index()

    # tzEST8 = datetime.timezone(datetime.timedelta(hours=8))
    # tzUTC = datetime.timezone(datetime.timedelta(hours=0))

    def afun(arow):
        adt = arow.to_pydatetime()
        ats = int(adt.timestamp() * 1000)
        return ats

    adjustPE['eobTstamp'] = adjustPE['date'].apply(afun)
    adjustPE = adjustPE[['eobTstamp', 'open','high','low','close']]
    peData = adjustPE.values.tolist()



    for alist in peData:
        alist[0] = int(alist[0])

    H.add_data_set(peData, 'candlestick', symbol_,
                   tooltip={'valueDecimals': 3},
                   allowPointSelect=True,
                   color='green',
                   upColor='red',
                   # dataGrouping={'enabled':False},
                   #states={'inactive':False}
                   )




    # 配置横坐标的初始的最大范围，在highchart中，又xais的min和max来指定。
    xAxis ={}
    options = {}
    if adjustPE.shape[0] > 400:
        xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
        xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
        options['xAxis']=xAxis

    H.set_dict_options(options)


def setAxisMinMax(H,adjustPE):
    # 配置横坐标的初始的最大范围，在highchart中，又xais的min和max来指定。
    xAxis = {}
    options = {}
    if adjustPE.shape[0] > 400:
        xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
        xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
        options['xAxis'] = xAxis

    H.set_dict_options(options)

#
# def plotCandle(H,dataDf):
#     ###画蜡烛图
#
#     #提供时间开高低收5个字段，最后转换成highchart中的 二维数组方式。这种方式在数据组织格式中有介绍。
#     #dataDf中的date 列必须是 pandas中的timestamp的格式。即是pandas中的datetime
#
#
#
#     # dataDf.columns=['date','open','high','low','close']
#     dataDf.columns = ['date', 'open', 'high', 'low', 'close','symbol']
#     adjustPE = dataDf.reset_index()
#
#     # tzEST8 = datetime.timezone(datetime.timedelta(hours=8))
#     # tzUTC = datetime.timezone(datetime.timedelta(hours=0))
#
#     def afun(arow):
#         adt = arow.to_pydatetime()
#         ats = int(adt.timestamp() * 1000)
#         return ats
#
#     adjustPE['eobTstamp'] = adjustPE['date'].apply(afun)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#     symlist=adjustPE['symbol'].drop_duplicates().values
#     for aSymbol in symlist:
#         aData = adjustPE.loc[adjustPE['symbol'] == aSymbol]
#         aData = aData[['eobTstamp', 'open', 'high', 'low', 'close']]
#         peData = aData.values.tolist()
#
#         for alist in peData:
#             alist[0] = int(alist[0])
#
#         H.add_data_set(peData, 'candlestick', aSymbol,
#                        tooltip={'valueDecimals': 2},
#                        allowPointSelect=True,
#                        color='green',
#                        upColor='red',
#                        dataGrouping={'enabled':False},
#                        #states={'inactive':False}
#                    )
#
#
#





def addMA(H,mainDataId,period=14,index=0):

    #index这个参数值见highcharts 笔记


    parDict={"period":period,"index":index}

    anameStr="sma(%d)"%(period)
    H.add_data_set([], 'sma', name=anameStr,linkedTo=mainDataId,params=parDict)



def addAIndictor(H,mainDataId,indicatorType,period=14,index=0,yaxisIndex=0,**kwargs):

    # index是指标中params属性的属性，具体见highcharts 笔记
    #yaxisIndex 是用来给  series属性中yaxis属性的。指标类型的series 都有yaxis这个属性的。具体见series 笔记

    parDict = {"period": period, "index": index}

    anameStr = "%s(%d)" % (indicatorType,period)


    H.add_data_set([], indicatorType, name=anameStr, linkedTo=mainDataId, params=parDict,yAxis=yaxisIndex,**kwargs)



def addMacd(H,mainDataId,speriod=12,longperiod=26,signalperiod=9,yaxisIndex=1,index=3):
    parDict = {"shortPeriod": speriod,"longPeriod": longperiod, "signalPeriod":signalperiod,"period":longperiod,"index":index}

    atooltipValue={"pointFormatter": "function() {\n\
            var seriesOptions = this.series.options,\n\
            str = '<b>MACD (26, 12, 9)</b><br>';\n\
            function getLine(color, name, value){\n\
                return '<span style=\"color:' + color + '\">\\u25CF</span> ' + name + ': <b>' + value + '</b><br/>';\n\
    }\n\
    str += getLine(seriesOptions.macdLine.styles.lineColor, 'diff', this.MACD.toFixed(2));\n\
    str += getLine(seriesOptions.signalLine.styles.lineColor, 'dea', this.signal.toFixed(2));\n\
    str += getLine(seriesOptions.color, 'macd', this.y.toFixed(2));\n\
    return str;\n\
}"}




    tststr="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    macdLineValue={"styles":{"lineColor":"blue","lineWidth":1}}  #所谓的diff
    signalLineValue={"styles":{"lineColor":"red","lineWidth":1}}
    # markerValue={"fillColor":"lightblue"}
    color="lightblue"

    # anameStr = "sma(%d)" % (period)
    # H.add_data_set([], 'macd', name=anameStr, linkedTo=mainDataId, params=parDict,macdLine=macdLineValue,signalLine=signalLineValue,marker=markerValue)
    H.add_data_set([], 'macd',  name='macdIndicator',linkedTo=mainDataId, params=parDict, macdLine=macdLineValue,
                   signalLine=signalLineValue, color=color,yAxis=yaxisIndex,tooltip=atooltipValue)

def plotSingal(H,signalDf,symbol):
    #date列必须是datetime类型
    #必须有一列的名字是ginalname

    signalDf['TStamp'] = signalDf['date'].apply(dftounixTimestamp)

    # 按照highcharts中的flag 序列的 数据要求，每一个标记要合成一个dict
    aList = []
    for index_, row in signalDf.iterrows():

        adict = {}
        # 构造flag 序列中的data标签下的 title 标签

        title=row['signalname']

        adict['title'] = title

        # 构造data标签下的text属性

        adict['text'] = title

        # 构造flag序列中的data标签下的x标签
        x = row['TStamp']
        adict['x'] = x

        aList.append(adict)
    H.add_data_set(aList, 'flags', 'flag-'+symbol, onSeries=symbol,allowOverlapX=True,stackDistance=20)

def plotBuySell(H,buysellData,symbol):

    # addMA(H,symbol,period=120)
    i=1
    #画买卖点
    #['symbol','positionEffect','positionSide','price','volume','date']

    buysellData['TStamp']=buysellData['date'].apply(dftounixTimestamp)



    #按照highcharts中的flag 序列的 数据要求，每一个比较要合成一个dict
    aList=[]
    for index_,row in buysellData.iterrows():

        adict={}
        #构造flag 序列中的data标签下的 title 标签

        if row['positionEffect']==gmEnum.PositionEffect_Open and row['positionSide']==gmEnum.PositionSide_Long:
            title='openlong'

        if row['positionEffect']==gmEnum.PositionEffect_Open and row['positionSide']==gmEnum.PositionSide_Short:
            title='openshort'

        if row['positionEffect'] == gmEnum.PositionEffect_Close and row['positionSide'] == gmEnum.PositionSide_Long:
            title = 'clearlong'

        if row['positionEffect'] == gmEnum.PositionEffect_Close and row['positionSide'] == gmEnum.PositionSide_Short:
            title = 'clearshort'

        adict['title']=title


        #构造data标签下的text属性
        text="price:%f,volumne:%d"%(row['price'],row['volume'])
        adict['text']=text

        #构造flag序列中的data标签下的x标签
        x=row['TStamp']
        adict['x']=x


        aList.append(adict)
    H.add_data_set(aList,'flags', symbol,onSeries= symbol,allowOverlapX=True)

    i=1


def addASeries(H,aSeriesData,sName,yaxisIndex=0,seriesType='line',setMax=False,**kwargs):
    #第一列必须是datetime类型
    aSeriesData.columns = ['date', sName]
    adjustPE = aSeriesData.copy()
    adjustPE['eobTstamp'] = adjustPE['date'].apply(dftounixTimestamp)
    adjustPE = adjustPE[['eobTstamp',sName]]
    peData = adjustPE.values.tolist()
    for alist in peData:
        alist[0] = int(alist[0])




    if setMax:
        # 配置横坐标的初始的最大范围，在highchart中，又xais的min和max来指定。
        xAxis = {}
        options = {}
        if adjustPE.shape[0] > 400:
            xAxis['min'] = int(adjustPE['eobTstamp'].iloc[0])
            xAxis['max'] = int(adjustPE['eobTstamp'].iloc[400])
            options['xAxis'] = xAxis

        H.set_dict_options(options)





    H.add_data_set(peData, seriesType, sName,
                   # tooltip={'valueDecimals': 2},
                   allowPointSelect=True,
                   yAxis=yaxisIndex,
                   # dataGrouping={'enabled': False},
                   # states={'inactive':False}
                   **kwargs
                   )

    i=1


def plotMainContractCandle(underlyingAsset,sDateTime,eDateTime,fre='60s'):

    #构造H
    H = createAHStock(underlyingAsset)


    #画k线
    hqDF=gm3HelpBylw.getHQDataOfMainContract_Fade([underlyingAsset], sDateTime, eDateTime,fre)
    aPlotData = hqDF[['eob', 'open', 'high', 'low', 'close']]
    plotCandle(H, aPlotData, underlyingAsset)


    #补具体合约标记.用标识线。
    #1、先准备数据，2、构造具体标识线的格式
    hqDF['symbolShift1'] = hqDF['symbol'].shift(1)
    newDf=hqDF.loc[hqDF['symbolShift1']!=hqDF['symbol']]
    newDf=newDf.dropna()
    newDf['TStamp'] = newDf['eob'].apply(dftounixTimestamp)

    for index_, row in newDf.iterrows():

        title = row['symbol']
        x = row['TStamp']
        plotLinedict={"value":x,
                      "width":2,
                      "color":'red',
                      "id":underlyingAsset,
                      "label":{"text":title,"align":'left', "x": 10 }
        }
        astr=json.dumps(plotLinedict)
        jsStript="chart.xAxis[0].addPlotLine(%s)"%(astr)


        H.add_JSscript(jsStript,'end')


    return H


#ADJUST_NONE or 0: 不复权, ADJUST_PREV or 1: 前复权, ADJUST_POST or 2: 后复权
def plotAContractCandle(underlyingAsset,sDateTime,eDateTime,fre='60s',adjust=1):

    #构造H
    H = createAHStock(underlyingAsset)


    #画k线
    hqDF=gm3HelpBylw.getHQData_Fade([underlyingAsset], sDateTime, eDateTime,fre,adjust=adjust)
    aPlotData = hqDF[['eob', 'open', 'high', 'low', 'close']]
    plotCandle(H, aPlotData, underlyingAsset)


    return H



def plotTradeSigByOrderRecord(H,orderRecord):
    orderRecord.columns = ['date','委托方向', '成交数量','成交均价']


    #画交易的点标记
    aSeriesData=orderRecord[['date','成交均价']]

    str11="function() {\n\
                        return this.y.toFixed(3);\n\
                    }"
    addASeries(H, aSeriesData, 'tradePrice', yaxisIndex=0, seriesType='line', setMax=False, lineWidth=0,\
               marker={'enabled':True,"radius":5},dataLabels={'enabled': True,"formatter":str11})

    #将委托信息标上

    orderRecord['signalname']=orderRecord['委托方向']+':'+orderRecord['成交数量'].astype(str)
    sigDF=orderRecord[['date','signalname']]
    plotSingal(H, sigDF, 'tradePrice')
    return H