from mcpi_e.minecraft import Minecraft
from mcpi_e import block
from time import sleep
from random import *

address="192.168.1.155"#if not pass address, it will be localhost
port=4712 #default port for RaspberryJuice plugin
name="stoneskinkknn"
#mc = Minecraft.create()
mc=Minecraft.create(address,port,name)

(x,y,z)=mc.player.getTilePos()
#mc.setBlock(x+1,y,z,0)
#wmc.setBlock(x+1,y,z,217)

id=mc.getBlock(x+1,y,z)
print("blockid get"+str(id))

#     print("set "+str(i))
i=0
for a in range(1,3):
    print(a)
    for b in range(1,13):       
        # if(i>252):
        #     break
        print("set blocke {} at {},{},{}".format(i,x+a,y+b,z))
        #mc.setBlock(x+a,y,z+b,0)
        mc.setBlock(x+a,y,z+b,4)
        i=i+1
        #id=mc.getBlock(x+a,y,z+b)
   

# print("done")