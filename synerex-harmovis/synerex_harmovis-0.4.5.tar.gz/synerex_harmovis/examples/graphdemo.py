import synerex_harmovis as sx

import random
import time

import asyncio


def drawRandomLine(count = 20):
    lines = sx.LineStore()
    for i in range(count):
        lines.addLine(
            lat0 = 34.8592285+0.02*random.random(),
            lon0 =136.816348+0.02*random.random(),
            lat1 = 34.8592285+0.02*random.random(),
            lon1 =136.816348+0.02*random.random(),
            color = 0xf0f0f0
        )
    sx.drawLines(lines)


def drawRandomGraph(n=3, count = 10):
    bars = sx.BGStore()
#    bars.colorType = sx.geo.BarColorType.VARCOLOR  # or FIXCOLOR
#    bars.shapeType = sx.geo.BarShapeType.BOX       # or HEX
    for i in range(count):
        bd = []
        for j in range(n):
            bd.append(int(100*random.random()))
        id = bars.addBarDataNow(
            label = "Sample"+str(i),
            lat = 34.8592285+0.01*random.random(),
            lon =136.816348+0.01*random.random(),
            barData = bd 
        )
    sx.sendBarGraphs(bars)
    return bars


def updateRandomGraph(bgstore):
    for bar in bgstore.bars:
        bd = bar['barData']
        for j in range(len(bd)):
            bd[j][0] = int(bd[j][0]*(0.90+random.random()*0.2))
        bgstore.updateBarDataNow(
            id = bar["id"],
            lat = bar["lat"],
            lon = bar["lon"],
            barData = bd 
        )
    sx.sendBarGraphs(bgstore)

def drawRandomArc(count = 20):
    arcs = sx.ArcStore()
    for i in range(count):
        arcs.addArc(
            lat0 = 34.8592285+0.02*random.random(),
            lon0 =136.816348+0.02*random.random(),
            lat1 = 34.8592285+0.02*random.random(),
            lon1 =136.816348+0.02*random.random(),
        )
    sx.drawArcs(arcs)


def main0():   #graph demo
    bars = drawRandomGraph(3,10)
    for i in range(20):
        time.sleep(1)
        updateRandomGraph(bars)

def main1():   #pitch demo
    drawRandomLine()

def main2():
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(sendBearing(0))
    b =0
    p = 0
    for i in range(72):
        sx.sendBearing(b)
        sx.sendPitch(p)
        p = (p % 60 )+ 3
        b +=5
        time.sleep(0.1)
        sx.send
    

if __name__ == "__main__":
    print("Start Graphdemo for Synerex-Harmovis")
    main0()

    main1()

    main2()
