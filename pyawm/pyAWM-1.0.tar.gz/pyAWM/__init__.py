from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver_path = None
media_loading_time = 60

def set_media_loading_time(time):
	set_media_loading_time = time

def send_whatsapp_msg(name_list , msg ,count, time_hour, time_min):
	if time_hour not in range(0,25) or time_min not in range(0,60):
		print("Invalid time format")
	if time_hour == 0:
		time_hour = 24
	callsec = (time_hour*3600)+(time_min*60) 
	curr = time.localtime()
	currhr = curr.tm_hour
	currmin = curr.tm_min
	currsec = curr.tm_sec
	currtotsec = (currhr*3600)+(currmin*60)+(currsec)
	lefttm = callsec-currtotsec
	print("Your message will be sent in", lefttm,"secs")
	if lefttm <= 0:
		lefttm = (3600*24)+lefttm
	if lefttm < 60:
		print("You must call before one minute as web.whatsapp.com takes some time to load")
		exit(0)
	time.sleep(lefttm-60)
	options = webdriver.ChromeOptions();
	options.add_argument('--user-data-dir=/pyAWM_User_Data')
	driver = webdriver.Chrome(r'F:/chromedriver_win32/chromedriver.exe', options=options)
	driver.get('https://web.whatsapp.com/')
	wait = WebDriverWait(driver = driver, timeout = 300).until(EC.presence_of_element_located((By.ID, 'pane-side')))
	time.sleep(59)
	for name in name_list:
		try:
			user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
		except:
			print("{} not found".format(name)," try again :(")
			continue
		time.sleep(1)
		user.click()
		wait = WebDriverWait(driver = driver, timeout = 600)
		msg_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="1"]')
		for i in range(count):
		        msg_box.send_keys(msg)
		        msg_box.send_keys(Keys.ENTER)
		wait = WebDriverWait(driver = driver, timeout = 600)
		time.sleep(2)
	time.sleep(media_loading_time)
	driver.close()
	del driver


def send_whatsapp_files(name_list , files_list , time_hour, time_min):
	if time_hour not in range(0,25) or time_min not in range(0,60):
		print("Invalid time format")
	if time_hour == 0:
		time_hour = 24
	callsec = (time_hour*3600)+(time_min*60)
	curr = time.localtime()
	currhr = curr.tm_hour
	currmin = curr.tm_min
	currsec = curr.tm_sec
	currtotsec = (currhr*3600)+(currmin*60)+(currsec)
	lefttm = callsec-currtotsec
	print("Your message will be sent in", lefttm,"secs")
	if lefttm <= 0:
		lefttm = (3600*24)+lefttm
	if lefttm < 60:
		print("You must call before one minute as web.whatsapp.com takes some time to load")
		exit(0)
	time.sleep(lefttm-60)
	options = webdriver.ChromeOptions();
	options.add_argument('--user-data-dir=/pyAWM_User_Data')
	driver = webdriver.Chrome(r'F:/chromedriver_win32/chromedriver.exe', options=options)
	driver.get('https://web.whatsapp.com/')
	wait = WebDriverWait(driver = driver, timeout = 600).until(EC.presence_of_element_located((By.ID, 'pane-side')))
	time.sleep(58)
	print("You have 1 minute to upload all files. You can always change by call function set_media_loading_time(secs)")
	for name in name_list:
		try: 
			user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
		except:
			print("{} not found".format(name))
			continue
		user.click()
		wait = WebDriverWait(driver = driver, timeout = 600)

		driver.find_element_by_xpath('//span[@data-icon="clip"]').click()

		attachment = driver.find_element_by_xpath('//input[@accept="*"]') #image/*,video/mp4,video/3gpp,video/quicktime
		for path in files_list:
			attachment.send_keys(path)
			time.sleep(2)
			driver.find_element_by_xpath('//span[@data-icon="send"]').click()	
		time.sleep(1)
	time.sleep(media_loading_time)
	driver.close()
	del driver

def send_whatsapp_media(name_list , files_list , msgs, time_hour, time_min):
	if time_hour not in range(0,25) or time_min not in range(0,60):
		print("Invalid time format")
	if time_hour == 0:
		time_hour = 24
	callsec = (time_hour*3600)+(time_min*60)
	curr = time.localtime()
	currhr = curr.tm_hour
	currmin = curr.tm_min
	currsec = curr.tm_sec
	currtotsec = (currhr*3600)+(currmin*60)+(currsec)
	lefttm = callsec-currtotsec
	if lefttm <= 0:
		lefttm = (3600*24)+lefttm
	if lefttm < 60:
		print("You must call before one minute as web.whatsapp.com takes some time to load")
		exit(0)
	print("Your message will be sent in", lefttm,"secs")
	time.sleep(lefttm-60)
	options = webdriver.ChromeOptions();
	options.add_argument('--user-data-dir=/pyAWM_User_Data')
	driver = webdriver.Chrome(r'F:/chromedriver_win32/chromedriver.exe', options=options)
	driver.get('https://web.whatsapp.com/')
	wait = WebDriverWait(driver = driver, timeout = 600).until(EC.presence_of_element_located((By.ID, 'pane-side')))
	time.sleep(56)
	print("You have 1 minute to upload all files. You can always change by call function set_media_loading_time()")
	for name in name_list:
		try: 
			user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
		except:
			print("{} not found".format(name))
			continue
		user.click()
		wait = WebDriverWait(driver = driver, timeout = 600)
		driver.find_element_by_xpath('//span[@data-icon="clip"]').click()

		attachment = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
		for path in files_list:
			attachment.send_keys(path)
			time.sleep(2)
			element = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="1"]')
			element.send_keys(msgs)
			time.sleep(2)
			driver.find_element_by_xpath('//span[@data-icon="send"]').click()
		time.sleep(2)		
	time.sleep(media_loading_time)
	driver.close()
	del driver

def add_driver_path(path):
	global driver_path
	driver_path = path
	try:
		options = webdriver.ChromeOptions();
		options.add_argument('--user-data-dir=/pyAWM_User_Data')
		driver = webdriver.Chrome(driver_path, options=options)
	except:
		print("Close all windows of Chrome. Check path of the driver.")

def scan_QR_Code():
	options = webdriver.ChromeOptions();
	options.add_argument('--user-data-dir=/pyAWM_User_Data')
	driver = webdriver.Chrome(driver_path, options=options)
	driver.get("https://web.whatsapp.com")
	while True:
		try:
			driver.find_element_by_xpath('//div[@id="pane-side"]')
			print("Successfully completed scanning and looged in.")
			driver.close()
			break
		except:
			pass

def users_manual():
	print("Steps for how to use this module: \n")
	print("Step 1: Download Google Chrome and see if it is working fine. If that works fine, go to step 2.\n")
	print("Step 2: Download Chrome Driver(latest and stable version) from https://chromedriver.chromium.org/ \n")
	print("Step 3: Extract the the downloaded file and copy the path of chromedriver\nExample: .../chromedriver.exe \n")
	print("Step 4: Call add_path_to_driver(path) where path is text that you copied. \n")
	print("Step 5: Call scan_QR_Code and open scanner in Whatsapp in your mobile and scan QR Code. \n")
	print("Step 6: Now you can use the functions to automate messages. \n")