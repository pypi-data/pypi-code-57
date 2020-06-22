# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 22:56:21 2020

@author: antoi
"""


import bs4
from bs4 import BeautifulSoup
import requests
import threading
import time
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"


import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from win10toast import ToastNotifier 
import yfinance as yf


limit_up = []
limit_down = []

class Stocks():
    
    def __init__(self):
        
        self.Airbus = {'RealTime':self.RealTime('https://www.boursorama.com/cours/1rPAIR/', 'Airbus',"c-faceplate__price"), 'Historic':self.Historic('https://finance.yahoo.com/quote/AIR.PA/')}
        self.Total = {'RealTime':self.RealTime('https://finance.yahoo.com/quote/TOT/', 'Total'), 'Historic':self.Historic('https://finance.yahoo.com/quote/TOT/')}
        self.CAC40 = {'RealTime':self.RealTime('https://fr.finance.yahoo.com/quote/%5EFCHI/', 'CAC40'), 'Historic':self.Historic('https://fr.finance.yahoo.com/quote/%5EFCHI/')}
        self.Bnp = {'RealTime':self.RealTime('https://fr.finance.yahoo.com/quote/BNP.PA/', 'Bnp'), 'Historic':self.Historic('https://fr.finance.yahoo.com/quote/BNP.PA/')}
        self.Renault = {'RealTime':self.RealTime('https://finance.yahoo.com/quote/RNO.PA/', 'Renault'), 'Historic':self.Historic('https://finance.yahoo.com/quote/RNO.PA/')}
        self.SocieteGenerale = {'RealTime':self.RealTime('https://finance.yahoo.com/quote/GLE.PA/', 'SocieteGenerale'), 'Historic':self.Historic('https://finance.yahoo.com/quote/GLE.PA/')}
        self.FaceBook = {'RealTime':self.RealTime('https://finance.yahoo.com/quote/FB?p=FB', 'FaceBook'), 'Historic':self.Historic('https://finance.yahoo.com/quote/FB?p=FB')}
        self.Sanofi = {'RealTime':self.RealTime('https://fr.finance.yahoo.com/quote/san.pa/', 'Total'), 'Historic':self.Historic('https://fr.finance.yahoo.com/quote/san.pa/')}
        

    class RealTime():
        
        flag = 0

        
        def __init__ (self, Url, name, divclass = None, position = None):
            
            self.Url = Url
            self.divclass = divclass
            self.position = position
            self.name = name
                        
        def value(self, print_disable = False):
           
            r = requests.get(self.Url)
            soup=bs4.BeautifulSoup(r.text,"lxml")
            
            if print_disable is False:
                print('divclass: ',self.divclass,'position: ',self.position)
            
            try:
               
                if self.divclass == None and self.position == None:
                    price = soup.findAll('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
                    
                    if print_disable is False:
                        print('value: '+ str(price))
                
                elif self.divclass != None and self.position == None:
                    price = soup.findAll('div',{'class':self.divclass})[0].find('span').text
                    
                    if print_disable is False:
                        print('value: '+ str(price))
                
                elif self.divclass != None and self.position != None:
                    price = soup.findAll('div',{'class':self.divclass})[0].find('span').text[self.position[0]:self.position[1]]
                    
                    if print_disable is False:
                        print('value: '+ str(price))
               
                elif self.divclass == None and self.position != None:
                    price = soup.findAll('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text[self.position[0]:self.position[1]]
                    if print_disable is False:
                        print('value: '+ str(price))
                
    
                return price.replace('\xa0','').replace(',','.').replace(' ','')

            
            except:
                
                print('miss, try again, Or verify anymistake in divclass,span or position. Make sure that print_disable is False to see what you are doing')
                
                return None            
            
        
        def plot(self):
            
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            
            global limit_down
            global limit_up
            
            price = self.value()
            
            x = [0]
            y = [float(price)]
            
            
            def animate(i):
            
                price = self.value()
                x.append(x[-1]+1)
                y.append(float(price))

                
                #redraw of ax1
                ax1.clear()
                
                new_title = "Live value of {:s} stock at t = {:.1f} seconds".format(self.name, x[-1])
                ax1.set_title(new_title, size = 15, color='navy', weight='bold', family='serif')
                
                #horizontal line of the current value
                ax1.axhline(float(price), color='seagreen', ls='--', lw=1.5, alpha=0.4)
                
                #printing the price value with a box around it
                bbox_props = dict(boxstyle="round,pad=0.3", fc="moccasin", ec="b", lw=2)
                ax1.annotate('val: {:.2f}'.format(float(price)),  # Your string
                    # The point that we'll place the text in relation to 
                    xy=(0.061, 0.5), 
                    # Interpret the x as axes coords, and the y as figure coords
                    xycoords=('figure fraction', 'figure fraction'),
                    # The distance from the point that the text will be at
                    xytext=(0, 0),  
                    #color
                    color = 'r',
                    # Interpret `xytext` as an offset in points...
                    textcoords='offset points',
                    # Any other text parameters we'd like
                    ha='center', va='bottom', size = 10,
                    #bbox
                    bbox = bbox_props)
            
                
                ax1.plot(x, y, alpha=0.8, lw=2, color='blue')
                
                if len(limit_up) != 0:
                    if limit_up[-1] != None:
                        ax1.axhline(limit_up[-1], color='r', ls='-.', lw=1.5, alpha=0.4)
                if len(limit_down) != 0:
                    if limit_down[-1] != None:
                        ax1.axhline(limit_down[-1], color='r', ls='-.', lw=1.5, alpha=0.4)
                
                return ax1,
            
            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()
            
            return(ani)
            

        def alertlimit(self, Lower_limit = None,  Uper_limit= None):
            setattr(self, 'flag', 0)
            limit_down.clear()
            limit_up.clear()
            
            def alert_thread(self, Lower_limit = None, Uper_limit = None):
               
                global limit_down
                global limit_up
                
                limit_up.append(Uper_limit)
                limit_down.append(Lower_limit)
                
                while True:
                    
                    if self.flag == 1:
                        break
                    
                    if Lower_limit == None and Uper_limit == None:
                        setattr(self, 'flag', 1)
                        print('you need to choose a limit')
                        
                    
                    
                    
                    
                    price = self.value(print_disable = True)
                    if price != None:
                        
                        toaster = ToastNotifier()
                        
                        if Uper_limit != None:
                            
                            if float(price) > float(Uper_limit):
                                toaster.show_toast('ALERT!', 'higher limit broke at: ' + price)
                                time.sleep(60)
                                
                        
                        if Lower_limit != None:
                            if float(price) < float(Lower_limit):
                                toaster.show_toast('ALERT!', 'lower limit broke at: ' + price)
                                time.sleep(60)
                    
                    time.sleep(1)
                return

            thread = threading.Thread(target = alert_thread, args=(self,Lower_limit,Uper_limit))
            thread.start()          
            
        def stopalert(self):
            
            setattr(self, 'flag', 1)
            
            limit_down.clear()
            limit_up.clear()
            
    class Historic():
        def __init__(self, Url):
            self.Url = Url
            
        def ID(self):
            
            r = requests.get(self.Url)
            soup=bs4.BeautifulSoup(r.text,"lxml")
            ID = soup.findAll('div',{'class':'Mt(15px)'})[0].find('h1').text
            id_list = ID.split('-')[0].replace(' ','')
            ID = ''
            
            for i in range(len(id_list)):
                ID = ID + id_list[i]
            return ID
            
            
        def plot(self):
            
            ID = self.ID()
            df = yf.Ticker(ID).history(period='max')
            fig = px.line(df, x=df.index, y='High', title='Time Series with Range Slider and Selectors')
            
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            fig.show()
                
    
    def add(self, Name, Url_real, Url_hist = None, divclass = None, position = None):
        setattr(self,Name,{'RealTime':self.RealTime(Url_real, Name, divclass, position), 'Historic':self.Historic(Url_hist)})
        return