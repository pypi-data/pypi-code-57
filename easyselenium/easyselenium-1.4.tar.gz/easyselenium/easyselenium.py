"""Copyright [2020] [Ankit Kothari(step2success.in)]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

www.step2success.in
"""


"""import json
import sys
from urllib import request    
from pkg_resources import parse_version    


url = f'https://pypi.python.org/pypi/{"easyselenium"}/json'
releases = json.loads(request.urlopen(url).read())['releases']
print( sorted(releases, key=parse_version, reverse=True)  )  
"""

#import subprocess
#subprocess.call(["pip","install","--upgrade","easyselenium"])


print('documentation & Examples: \n\nhttps://pypi.org/project/easyselenium/  \nhttps://www.step2success.in/easyselenium/               \n \n')
print('')


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import concurrent.futures

import time
global driver

###############################################################################
def autoupgrade():
		
	import os
	stdout=os.popen("pip install --upgrade easyselenium").read()
	if debugs:
		print('Checking for easyselenium updates')
#####################################################################################################



with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor:
	a=executor.submit(autoupgrade)

#####################################################################################################
def open_browser(headless=False,path="",browser='chrome',debug=True,auto_upgrade=True):
	global driver
	global debugs

	debugs=debug


	if browser.lower()=='chrome':
		chrome_options = webdriver.ChromeOptions()
		from easyselenium.webdriver_manager.chrome import ChromeDriverManager


		if headless:
			chrome_options.add_argument('--headless')
		#chrome_options.add_argument('window-size=1920x1080');
		chrome_options.add_argument("--start-maximized")
		chrome_options.add_argument('ignore-certificate-errors')
		driver=webdriver.Chrome(ChromeDriverManager(path=path).install(),chrome_options=chrome_options)
		
	

	elif browser.lower()=='firefox':
		from selenium.webdriver.firefox.options import Options
		options = Options()

		from easyselenium.webdriver_manager.firefox import GeckoDriverManager
		if headless:
			options.headless = True
		driver = webdriver.Firefox(executable_path=GeckoDriverManager(path=path).install(),options=options)
		driver.maximize_window()

		
	elif browser.lower()=='ie':
		
		from easyselenium.webdriver_manager.microsoft import IEDriverManager
		driver = webdriver.Ie(IEDriverManager(path=path).install())
		driver.maximize_window()
		

	elif browser.lower()=='edge':
		from easyselenium.webdriver_manager.microsoft import EdgeChromiumDriverManager
		driver = webdriver.Edge(EdgeChromiumDriverManager(path=path).install())


	


	url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
	session_id = driver.session_id
	print("\nuse this to connect_exisitng_browser(url='{}',session_id='{}')\n\n".format(url,session_id))
	return(driver)
		


#############################################################################


def connect_exisitng_browser(url,session_id,debug=True):
	global driver
	global debugs
	debugs=debug=True
	driver = webdriver.Remote(command_executor=url,desired_capabilities={})
	driver.session_id = session_id
	print("connecting existing browser")
	return(driver)





###############################################################################
def open_url(url='https://step2success.in',new_tab=False,debug=True):
	
	debugs=debug=True
	if new_tab:
		url=str(url)
		driver.execute_script("window.open('{}','_blank');".format(url))
		print("opening url in new tab Title: ",driver.title,'\n')
		return()
	else:
		driver.get(url)
		if debugs:
			print("opening url \n** for New Tab use: new_tab=True\n")

	


###########################################################################

def found_window(name):
	def predicate(driver):
		try:
			#print('FINDING WINDOW')
			a=driver.window_handles[name]
			driver.switch_to_window(a)
			if debugs:
				print("Switch to window ",name)
		except Exception as e:
			#print ('window not found',e)
			return False
		else:
			return True # found window
	return predicate


'''def select_option(id,value,my_option):
    def predicate(driver):
        try:
            if id=='na':
            	a=driver.find_element_by_xpath('{}'.format(value))
            else:
            	a=driver.find_element_by_xpath('//select[@{}="{}"]'.format(id,value))
            a=Select(a)
            for o in a.options:
            	#print(o.text)
            	if my_option.lower() in o.text.lower():
            		a.select_by_visible_text(o.text)
            		if debugs:
            			print("Select option",o.text)
            		return True 
           
        except Exception as e:
            
            return False
        else:
            return True 
    return predicate'''

#############################################################################

def select_option(id,value,my_option):
    def predicate(driver):
        try:
            if id=='na':
            	a=driver.find_element_by_xpath('{}'.format(value))
            else:
            	a=driver.find_element_by_xpath('//select[@{}="{}"]'.format(id,value))
            a=Select(a)
            for o in a.options:
            	#print(o.text)
            	if my_option.lower() in o.text.lower():
            		a.select_by_visible_text(o.text)
            		if debugs:
            			print("Select option",o.text)
            		return True
            return False
           
        except Exception as e:
            
            return False
        else:
            return True 
    return predicate

    ##############################################################################


def window_handle(no=1,title=False,timeout=50):

	if title:
		handles = driver.window_handles
		size = len(handles)
		for x in range(size):
		  
		    driver.switch_to.window(handles[x])
		   
		    if title.lower() in str(driver.title).lower():
		    	if debugs:
		    		print('window handle no' ,no,driver.title)
		    	return(driver.title)

	WebDriverWait(driver, timeout=timeout).until(found_window(no))
	if debugs:
		print('window handle no' ,no,driver.title)
	driver.maximize_window()
	return(driver.title)

#####################################################################################################

def switch_frame(no=-1,timeout=50,xpath=False,**kwargs):
	if no>=0:
		driver.switch_to.frame(no)
		if debugs:
			print("Switch to frame no",no)
		return()
	elif xpath:
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
		else:
			element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '{}'.format(xpath))))
	else:
		key=(list(kwargs.keys())[0])
		value=kwargs[key]
		element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
	driver.switch_to.frame(element)
	if debugs:
			print("Switch to frame",kwargs[key])
	print('switched to frame')



#####################################################################################################


def click_on(text=False,image=False,xpath=False,repeat_click=False,timeout=50,**kwargs):
	if xpath:
		if debugs:
			print("Click on Xpath",xpath)
		
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			cl= WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
			
		else:
			cl= WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '{}'.format(xpath))))
		
	 
	elif image:
		
		if debugs:
			print("Click on image",image)
		cl=WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//a[img/@src="{}"]'.format(image))))
		
	

	elif text:
		cl=WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text)))
		if debugs:
			print("Click on text",text)
		

	else:
		key=(list(kwargs.keys())[0])
		cl=WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
		if debugs:
			print("click on",kwargs[key])
	#ActionChains(driver).move_to_element(cl).perform()
	cl.click()
	if repeat_click:
		try:
			cl=WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
		except:
			pass




#####################################################################################################



def mouse_hover(text=False,image=False,xpath=False,repeat_click=False,timeout=50,**kwargs):
	if xpath:
		if debugs:
			print("Click on Xpath",xpath)
		
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			cl= WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
			
		else:
			cl= WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '{}'.format(xpath))))
		
	 
	elif image:
		
		if debugs:
			print("Click on image",image)
		cl=WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//a[img/@src="{}"]'.format(image))))
		
	

	elif text:
		cl=WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text)))
		if debugs:
			print("Click on text",text)
		

	else:
		key=(list(kwargs.keys())[0])
		cl=WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
		if debugs:
			print("click on",kwargs[key])
	ActionChains(driver).move_to_element(cl).perform()
	




#####################################################################################################


def send_text(xpath=False,text='',with_enter=False,timeout=50,**kwargs):
	if xpath:
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
		else:
			element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '{}'.format(xpath))))
	else:
		key=(list(kwargs.keys())[0])
		value=kwargs[key]
		
		element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,value))))


	element4.send_keys(str(text))
	if debugs:
			print("Send text",text)
	if with_enter:
		element4.send_keys(Keys.ENTER)
	



#####################################################################################################


def select_dropdown(option,xpath=False,timeout=50,**kwargs):
	if xpath:
		
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			WebDriverWait(driver, timeout=timeout).until(select_option(key,value,option))
			
		else:
			WebDriverWait(driver, timeout=timeout).until(select_option('na',xpath,option))
			
	else:

		key=(list(kwargs.keys())[0])
		WebDriverWait(driver, timeout=timeout).until(select_option(key,kwargs[key],option))
		print('selelct')
	



#####################################################################################################


def read_text(xpath=False,timeout=50,**kwargs):
	if xpath:
		if '='in xpath and "@"not in xpath:
			xpath=xpath.split("=")
			key=xpath[0]
			value=xpath[1].replace('"','')
			element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
			elements4=driver.find_elements_by_xpath('//*[@{}="{}"]'.format(key,value))
		else:
			element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '{}'.format(xpath))))
			elements4=driver.find_elements_by_xpath('{}'.format(xpath))
	else:
		key=(list(kwargs.keys())[0])
		value=kwargs[key]
		element4 = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,value))))
		elements4=driver.find_elements_by_xpath('//*[@{}="{}"]'.format(key,value))


	length=(len(elements4))
	

	output=[]
		
	if elements4[0].get_attribute('value')!=None:
		for i in elements4:
			temp=(i.text,i,i.get_attribute('value'))
			output.append(temp)
	else:
		for i in elements4:
			output.append((i.text,i))
	#print('output',output)
	

	if debugs:
		print('\n\nTotal elements found',length,'\n')
		

		c=0
		print('[\n')
		if elements4[0].get_attribute('value')!=None:
			for i in output:
				print(c,"( '{}' ,<selenium.webdriver.remote..... ), value '{}'".format(i[0],i[2]))
				c+=1
			
		else:
			for i in output:
				print(c,"('{}' ,<selenium.webdriver.remote..... )".format(i[0]))
				c+=1
		print('\n]')
	return(output)



#####################################################################################################


def close_window(no=0,title=False,switch_to=0):
	try:

		if title:
			window_handle(title=title)
			if debugs:
				print('close window title',title)
		else:
			window_handle(no=no)
			if debugs:
				print('close window no',no)
		driver.close()
		
		if no>0:
			window_handle(switch_to)
	except:
 		print('No such window')



#####################################################################################################


def alerts(text=''):

	try:


		 WebDriverWait(driver, 15).until(EC.alert_is_present(),'Timed out waiting for PA creation ' +'confirmation popup to appear.')
		 alert = driver.switch_to.alert
		 a=alert.text
		 if debugs:
		 	print('Alerts box text:',a)
		 if text.lower()=='yes' or text.lower()=='accept':
		 	alert.accept()
		 elif text.lower()=='no' or text.lower()=='cancel':
		 	alert.dismiss()
		 elif text!="":
		 	alert.send_keys(text)
		 else:
		 	print(a)
		 	return(a)
	except Exception as e:
		print(e,'no alert present')



#####################################################################################################

def window_alert(text='NA',with_enter=False):
	
	import win32com.client
	shell = win32com.client.Dispatch("WScript.Shell")  
	shell.Sendkeys(text)
	shell.Sendkeys("{TAB}")
	time.sleep(1)
	if with_enter:
		shell.Sendkeys("{ENTER}")
		return()



#####################################################################################################
def page_source():
	x=driver.page_source
	#print(x)
	return(x)
####################################################################################################

def easyselenium_help():
	help1='''

from easy selenium import *
open_browser()
with optional arguments

headless = True/False (to work without browser)
path = 'your drirectory by default is default directory'
browser = 'chrome'/'firefox'/ie
debug = True/False (to print what is happening inside the code)

Example
This is by default arguments

## open_browser(headless=False,path="chromedriver.exe",browser='chrome',debug=False)
open_url(url='www.google.in')
with optional arguments

url = 'your web url'
new_tab = True/False (open in new tab or same)
Example
This is by default arguments

## open_url(url='www.step2success.in',new_tab=True)
window_handle(no=1)
To switch to your popup or another tab window ()
by default time to wait is 50 sec
switch_frame (no=1 or name='mainframe')
To switch to iframe or frame with no or name
by default time to wait is 50 sec
click_on (text='submit'or image='imagepath' or id='submit' or css='send' or xpath='this')
To Click on buton based on iamge/Text or xpath by default time to wait is 50 sec

with optional arguments

repeat=True/False (True-To double click on item)
send_text (text='your text' with id='submit' or css='send' or xpath='this')
by default time to wait is 50 sec
```sh
with optional arguments

with_enter=True/False (True-To enter after type text)
select_dropdown (option ='option to select' with id='submit' or css='send' or xpath='this')
	'''

	print(help1)
	 







