from datetime import datetime 
import asyncio
from grpclib.client import Channel

from .proto import api
from .proto import geography as geo

class SxHarmoVIS:
    ''' SxHarmoVIS: base class for Synerex-HarmoVIS integration
    '''
    def __init__(self, srvaddr='localhost:18000', channel=14, node_id = 100):
        hs = srvaddr.split(':')
        self.grpcChannel = Channel(host=hs[0], port=int(hs[1]))
        self.service = api.SynerexStub(self.grpcChannel)
        self.chan = channel
        self.node_id = node_id

    def close(self):
        self.grpcChannel.close()

    async def notifySupply(self, name, data):
        ts = datetime.now()
        cdata = api.Content(entity = data.SerializeToString())
        return await self.service.notify_supply(
            sender_id = self.node_id,
            channel_type = self.chan,
            supply_name = name,
            ts = ts,
            cdata = cdata
        )


    async def sendViewStateAsync(self, lat, lon, zoom = -1, pitch = -1, duration = 0):
        data = geo.ViewState(lat = lat, lon = lon , zoom= zoom, pitch=pitch, duration = duration) 
        return await self.notifySupply('ViewState',data)

    async def sendPitchAsync(self, pitch, duration  =0):
        data = geo.Pitch(pitch = pitch, duration = duration) 
        return await self.notifySupply('Pitch',data)

    async def sendBearingAsync(self, bearing, duration = 0):
        data = geo.Bearing(bearing = bearing, duration = duration) 
        return await self.notifySupply('Bearing',data)

    async def sendBarGraphsAsync(self, bs):
        mybars =[]
        for b in bs.bars:
            bd = []
            ct = 0
            for d in b["barData"]:
                if type(d) is list:
                    bd0=geo.BarData(value = d[0],color = d[1])
                else:
                    bd0=geo.BarData(value = d, color = bs.barColors[ct])
                    ct = ct + 1
                bd.append(bd0)
            mybars.append(geo.BarGraph(id=b["id"], ts=b["ts"],
                                       color_type= b["colorType"],
                                       shape_type=b["shapeType"],
                                       min = b["min"],
                                       max = b["max"],
                                       color = b["color"],
                                       width = b["width"],
                                       radius = b["radius"],
                                       area_color = b["areaColor"],
                                       text = b["text"],
                                       lat = b["lat"],
                                       lon = b["lon"],
                                       bar_data = bd ))
        data = geo.BarGraphs(bars = mybars)
        return await self.notifySupply('BarGraphs',data)

    async def drawLinesAsync(self, lines):
        mylines =[]
        colors = []
        for l in lines.lines:
            mylines.append(geo.Line(from_=[l[0][1],l[0][0]],to=[l[1][1],l[1][0]]))
            colors.append(l[2])
        data = geo.Lines(lines = mylines, width= lines.width, color = colors)
        return await self.notifySupply('Lines',data)

    async def drawArcsAsync(self, arcstore):
        src =[]
        tgt =[]
        srcCol = []
        tgtCol = []
        tilt = []
        for a in arcstore.arcs:
            src.append( geo.Point(lat=a[0],lon=a[1]))
            tgt.append( geo.Point(lat=a[2],lon=a[3]))
            srcCol.append( a[4])
            tgtCol.append( a[5])
            tilt.append( a[6])
        data = geo.Arcs(srcs = src, tgts = tgt, 
                        src_cols = srcCol, 
                        tgt_cols = tgtCol,
                        tilts = tilt
        )
        return await self.notifySupply('Arcs',data)

    async def drawScattersAsync(self, scstore):
        point =[]
        radius =[]
        fillCol = []
        lineCol = []
        for s in scstore.scs:
            point.append( geo.Point(lat=s[0],lon=s[1]))
            radius.append( s[2])
            fillCol.append( s[3])
            lineCol.append( s[4])
        data = geo.Scatters(points = point,
                        radiuses = radius, 
                        fill_colors = fillCol, 
                        line_colors = lineCol
        )
        return await self.notifySupply('Scatters',data)

    async def sendTopTextLabelAsync(self, label, style=""):
        data = geo.TopTextLabel(
            label = label,
            style = style
        )
        return await self.notifySupply('TopTextLabel',data)
    
    async def sendClearArcsAsync(self):
        data = geo.ClearArcs()
        return await self.notifySupply('ClearArcs',data)

    async def sendClearScattersAsync(self):
        data = geo.ClearScatters()
        return await self.notifySupply('ClearScatters',data)

    async def sendHarmoVISAsync(self,jsonStr):
        data = geo.HarmoVIS(jsonStr)
        return await self.notifySupply('HarmoVIS',data)

    async def sendMeshAsync(self, ms):
        return await self.sendHarmoVISAsync(ms.getJsonStr())


class LineStore:
    def __init__(self):
        self.lines = []
        self.width = 1
    
    def setWidth(self, wid):
        self.width = wid

    def addLine(self,lat0,lon0,lat1,lon1, color = 0x708080):
        self.lines.append([[lat0,lon0],[lat1,lon1], color])

class ArcStore:
    def __init__(self):
        self.arcs = []
    
    def addArc(self,lat0,lon0,lat1,lon1, srcCol = 0xd0c000, tgtCol = 0xb0a000, tilt = 0):
        self.arcs.append([lat0,lon0,lat1,lon1, srcCol, tgtCol, tilt])

class ScatterStore:
    def __init__(self):
        self.scs = []
    
    def addScatter(self,lat,lon,radius, fillCol = 0xd000f0, lineCol = 0x200020):
        self.scs.append([lat,lon,radius, fillCol, lineCol])

class MeshStore:
    def __init__(self):
        self.timestamp = int(datetime.now().timestamp())
        self.id = 1000000
        self.count = 0
        self.meshItems = {}

    def setTimestamp(self, ts):
        self.timestamp = ts

    def setTimestampNow(self):
        self.timestamp = int(datetime.now().timestamp())

    def setMeshID(self, id):
        self.id = id

    def addMeshItem(self,lat,lon,value,color="[0,200,0]", itemId = -1):
        if( itemId < 0):
            itemId = self.count
            self.count += 1
            while (itemId in self.meshItems):
                itemId = self.count
                self.count += 1
        self.meshItems[itemId]=[lat,lon,value,color]

    def updateMeshValue(self,itemId,value,color="[0,200,0]"):
        last = self.meshItems[itemId]
        self.meshItems[itemId]=[last[0],last[1],last[2],last[3]]

    def getItemIds(self):
        return self.meshItems.keys()

    def getJsonStr(self):
        mistr = ""        
        for s in self.meshItems.values():
            mistr = mistr + "{" + ('\"pos\":[{},{}],\"val\":{},\"col\":{}'.format(s[1],s[0],s[2], s[3])) +"},"
        meshData = '\"id\":{},\"timestamp\":{}, \"meshItems\":[{}]'.format(self.id, self.timestamp, mistr[:-1])
        jsonConf = '{\"addMesh\":{'+meshData+'}}'
        return jsonConf

class BGStore:
    def __init__(self):
        self.bars = []
        self.barColors = [0xf00000, 0x00f000, 0x0000f0, 0xe0e000, 0xe000e0, 0x00e0e0]
        self.idbase = 0
        self.colorType = geo.BarColorType.VARCOLOR
        self.shapeType = geo.BarShapeType.HEX
        self.areaColor = 0x0f0f0f
        self.color = 0x000d60
        self.radius = 100
        self.width = 30
        

    def addBarData(self,ts, label, lat,lon,barData):
        self.bars.append({
            'id': self.idbase,
            'ts': ts,
            'colorType': self.colorType,
            'shapeType': self.shapeType,
            'min' : 0,
            'max' : 100,
            'color': self.color,
            'width': self.width,
            'radius': self.radius,
            'areaColor': self.areaColor,
            'text' : label,
            'lat':lat,
            'lon':lon,
            'barData':barData
        })
        self.idbase = self.idbase+1
        return self.idbase-1

    def addBarDataNow(self,label,lat,lon, barData):
        ts = datetime.now()
        return self.addBarData(ts, label, lat,lon, barData)

    def updateBarData(self, id, ts, lat, lon, barData):
        self.bars[id].update({
            'ts': ts,
            'lat':lat,
            'lon':lon,
            'barData':barData
        })

    def updateBarDataNow(self,id, lat,lon, barData):
        ts = datetime.now()
        self.updateBarData(id, ts, lat,lon, barData)

async def sendBearingAx(b, duration = 0):
    srv = SxHarmoVIS()
    res = await srv.sendBearingAsync(b, duration)
    srv.close()
    return res

async def sendPitchAx(p, duration = 0):
    srv = SxHarmoVIS()
    res = await srv.sendPitchAsync(p, duration)
    srv.close()
    return res

async def sendViewStateAx(lat,lon,zoom=-1, pitch=-1, duration = 0):
    srv = SxHarmoVIS()
    res = await srv.sendViewStateAsync(lat,lon,zoom,pitch, duration)
    srv.close()
    return res

async def sendBarGraphsAx(bg):
    srv = SxHarmoVIS()
    res = await srv.sendBarGraphsAsync(bg)
    srv.close()
    return res

async def drawLinesAx(ln):
    srv = SxHarmoVIS()
    res = await srv.drawLinesAsync(ln)
    srv.close()
    return res

async def drawArcsAx(ln):
    srv = SxHarmoVIS()
    res = await srv.drawArcsAsync(ln)
    srv.close()
    return res

async def drawScattersAx(ln):
    srv = SxHarmoVIS()
    res = await srv.drawScattersAsync(ln)
    srv.close()
    return res

async def clearArcsAx():
    srv = SxHarmoVIS()
    res = await srv.sendClearArcsAsync()
    srv.close()
    return res

async def clearScattersAx():
    srv = SxHarmoVIS()
    res = await srv.sendClearScattersAsync()
    srv.close()
    return res

async def sendTopTextLabelAx(label, style=""):
    srv = SxHarmoVIS()
    res = await srv.sendTopTextLabelAsync(label, style)
    srv.close()
    return res

async def sendHarmoVISAx(jsonStr):
    srv = SxHarmoVIS()
    res = await srv.sendHarmoVISAsync(jsonStr)
    srv.close()
    return res

async def sendMeshAx(mesh):
    srv = SxHarmoVIS()
    res = await srv.sendMeshAsync(mesh)
    srv.close()
    return res


def sendBearing(b, duration = 0):
    return asyncio.run(sendBearingAx(b, duration))

def sendPitch(p, duration = 0):
    return asyncio.run(sendPitchAx(p, duration))

def sendViewState(lat,lon,zoom=-1, pitch=-1, duration = 0):
    return asyncio.run(sendViewStateAx(lat,lon,zoom,pitch, duration))

def sendBarGraphs(bg):
    return asyncio.run(sendBarGraphsAx(bg))

def drawLines(ln):
    return asyncio.run(drawLinesAx(ln))

def drawArcs(ln):
    return asyncio.run(drawArcsAx(ln))

def drawScatters(ln):
    return asyncio.run(drawScattersAx(ln))

def sendTopTextLabel(label, style=""):
    return asyncio.run(sendTopTextLabelAx(label,style))

def clearArcs():
    return asyncio.run(clearArcsAx())

def clearScatters():
    return asyncio.run(clearScattersAx())

def sendHarmoVIS(jsonStr):
    return asyncio.run(sendHarmoVISAx(jsonStr))

def sendMesh(mesh):
    return asyncio.run(sendMeshAx(mesh))
