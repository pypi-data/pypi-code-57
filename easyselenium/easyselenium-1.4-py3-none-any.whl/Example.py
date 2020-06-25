#############################
#                            #
#      Step2success.in       #
#        copyright           #
##############################           
# Selenium is used for Gui testing as well as we can use it for web scrapping and web automation to fill up forms in complex sites and tools.
#pip install selenium        


import time

from easyselenium import *
import time
open_browser(browser='firefox',debug=True)
#open_broswer(browser='firefox')
#open_broswer(browser='ie')
#open_broswer(browser='chrome',headless=True)

open_url(url="https://step2success.in/registration-page-demo/")
open_url(url="https://step2success.in/iframe-demo/",new_tab=True)
window_handle(no=0)
send_text(text='Ankit',id='first_name')
send_text(text='Kothari',id='last_name',with_enter=True)
select_dropdown(option='What is your Birthdate?',id='dropdown')
#click_on(text='REGISTER')
#click_on(id='register')


time.sleep(3)

window_handle(no=1)
switch_frame(no=0)
read_text(href ='#')
click_on(text='Follow On Twitter')

window_handle(no=2)

#close_window(no=2)




