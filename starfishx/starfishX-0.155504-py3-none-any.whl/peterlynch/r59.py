import re
import pandas as pd
import ssl
from urllib import request, parse
from bs4 import BeautifulSoup

import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime

from IPython.display import HTML

pd.set_option('display.max_colwidth',-1)

def filterThai(str_data):
    return re.sub(r'[^a-zA-Z]', "", str_data)

def getValueCompanyR59(wordSearch):
 '''
 wordSearch : str เช่น เจ มาร์ท , ท่าอากาศ เป็นต้น
              ใช้คำบางส่วนของชื่อบริษัท
 '''  
 context = ssl._create_unverified_context()
 url = 'https://market.sec.or.th/public/idisc/th/r59'
 
 #data = parse.urlencode(values).encode()
 req =  request.Request(url) # this will make the method "POST"
 resp = request.urlopen(req,context=context)
 
 soup = BeautifulSoup(resp.read() , "lxml")
 
 ct = soup.find_all("select")

 for i in ct[0].find_all('option'):
   if(wordSearch in i.text):
      print(i.text)
      print(i["value"])

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = "รายละเอียด"
    link = link
    return f'<a target="_blank" href="{link}">{text}</a>'

def getReportR59(dateFrom,dateTo,Company="",report=True):
  '''
  ใช้วันที่เป็น พ.ศ. #DD/MM/YYYY 
  ตัวอย่าง getReportR59(dateFrom="01/01/2563",dateTo="30/05/2563",Company="0000003725") 

  หากใช้งานไม่ได้ ทดลองติดตั้งเพิ่มเติมด้วยคำสั่ง
  conda install -c conda-forge geckodriver
  ''' 
  #dateFrom = "01/01/2563"
  #dateTo = "10/01/2563"
  #Company = "0000008180"  
  #dateFrom="01/01/2563"
  #dateTo="30/04/2563"
  #Company="0000028632"
  os.environ['MOZ_HEADLESS'] = '1'  
  driver = webdriver.Firefox()  #อาจต้องลง 
  # Grab the web page
    
  driver.get("https://market.sec.or.th/public/idisc/th/r59")
  #กำหนดค่าใน textbox
  k = driver.find_element_by_id("BSDateFrom")
  k.clear()
  k.send_keys(dateFrom)
  driver.find_element_by_id("BSDateFrom").get_attribute("value")
    
  ### Dateto
  k = driver.find_element_by_id("BSDateTo")
  k.clear()
  k.send_keys(dateTo)
  driver.find_element_by_id("BSDateTo").get_attribute("value")

  if(Company!=""):
   ### Select
   k = Select(driver.find_element_by_id("ctl00_CPH_ddlCompany"))
   k.select_by_value(Company)
   #driver.find_element_by_id("BSDateTo").get_attribute("value")


  ### หาปุ่ม submit และกด click
  btn_input = driver.find_element_by_id("ctl00_CPH_btSearch")
  # Then we'll fake typing into it
  btn_input.click()  

  ### เริ่ม parser
  # We can feed that into Beautiful Soup
  doc = BeautifulSoup(driver.page_source,"html.parser")  
  rows = doc.find('table', id='gPP09T01')  
  
   
  if("ไม่พบข้อมูล" in str(rows)):
    return 0
    #print(1)

  tr = []
  td = []
     
  for i in rows.find_all("tr"):
    td = []  
    cnt_td = 0
    k = i.find_all("td")
    for j in k:
     if(cnt_td==4): #หา date
        tmp = j.text.split("/")
        date_time_str = str(int(tmp[2])-543)+"-"+tmp[1]+"-"+tmp[0]
        dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        #print(date_time_str)
        td.append(dt) 
     
     elif(cnt_td==8):
        td.append(j.a['href'])
     else:   
        td.append(j.text)   
        
     cnt_td+=1
    tr.append(td.copy())
    
  #สร้าง DataFrame  
  df = pd.DataFrame(tr)
  #จัดทรง DataFrame  
  df = df.dropna()
  
   
  df.columns = ["Company","Management","Relationship","TypesAsset","Date","Amount","AvgPrice","Methods","Remark"] 
  df["Company"] = [filterThai(j) for j in df["Company"]]
  #del df['Remark']
  
  df["Amount"] = df["Amount"].str.replace(",","").astype(float)  
  df["AvgPrice"] = df["AvgPrice"].str.replace(",","").astype(float)
  driver.close()  

  #เพิ่ม link HTML รายละเอียด

  if(report==True):
   df['Remark'] = df['Remark'].apply(make_clickable)
   df = HTML(df.to_html(escape=False))
  return df  