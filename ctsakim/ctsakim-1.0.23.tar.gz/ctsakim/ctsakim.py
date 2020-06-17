      
import time
from datetime import datetime
import json
import requests
from threading import Thread

import math
import gpiozero
#import RPi.GPIO as GPIO
from gpiozero import MCP3008

def dpost(data1,path):
 #API_ENDPOINT =  "http://192.168.1.7/DataCollection/Api/DataAll"

 r=requests.post(url = path, json = data1)
 
 print(r.elapsed.total_seconds())
 if r.status_code==200:
      print("post success")
 else:
      print("post unsucessfull")
 print("Elapsed Time: ", r.elapsed.total_seconds())


def current():
    logTime=input("Enter your LogTime(default Logtime=3): ")   
  
    if logTime=="":
        logTime=3
    
    data = []
    val = input("Enter your API_ENDPOINT: ")
    #eğer değer girilmezse default değer gir
    if val=="":
        val="http://192.168.1.7/DataCollection/Api/DataAll"
    #r=requests.post(url = val, json = data)
    try:
      r=requests.post(url = val, json = data)
      
      if r.status_code!=200:
          print("error",r.status_code)
          current()
    except requests.exceptions.Timeout:
           print("TimeOutException") # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
           print("TooManyRedirects Exception")# Tell the user their URL was bad and try a different one
    
    except ConnectionError as e:    # This is the correct syntax
       print (e)
       r = ("No response")       
    except requests.exceptions.RequestException as e:
        
        print("Request exception")
        current()

 
    
    sendDate=datetime.now()
    
    offsetI=0   
    sumI=0
    
    y = 0 #veri kaybı kontrol değişkeni
    dataSayisi=0
    toplam = 0
    while True:
        for n in range(0,1480):
          adc=MCP3008(channel=0)
          sampleI=adc.value
          
          offsetI=offsetI+(sampleI-offsetI)/1024
          filteredI=sampleI-offsetI
          sql=filteredI*filteredI;
          sumI+=sql 
        loopDate = datetime.now()
        timedelta = loopDate - sendDate
        zaman=timedelta.days * 24 * 3600 + timedelta.seconds
        
        dataSayisi=dataSayisi+1
       
        toplam = toplam + 1
        I_RATIO = 30 *((3300/1000.0) /1024) #5v5000 supply voltage
                                            #100a-1v-->(100:1):33(33ohm ise)
                                            #100a-50ma--(100:0.050):33
        Irs=I_RATIO*math.sqrt(sumI/1480)
        print("Akim:%.5f A"%Irs )
        Power=Irs*220
        sumI=0
        
        data.append({'Datetime':loopDate.strftime("%m-%d-%Y %H:%M:%S.%f"),
          'Current':"{0:2f}".format(Irs),
          'Power':"{0:2f}".format(Power)})
        
        if zaman==int(logTime):
            print("\n",zaman,"saniyede okunan data:",dataSayisi )
            print(sendDate)
            
            dataSayisi=0

            dum = Thread(target = dpost, args = (data,val,))
            dum.start()
                
           
            sendDate=datetime.now()

            data = []
#current()