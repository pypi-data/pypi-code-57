#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/24 10:53
# @Author : yangpingyan@gmail.com
import pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import os
from time import sleep
from selenium.webdriver import Remote, ActionChains
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException
import getpass
import subprocess

def chrome_open_mobile(chrome_options=[], userdata_path=r"c:\chrome_mobile"):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--disable-infobars')  # 关闭浏览器上方自动测试提示
    options.add_argument('--start-maximized')  # –start-maximized 启动就最大化
    # options.add_argument('--no-startup-window')  # 关闭启动弹窗 可能导致chrome无法启动，注释不再用
    options.add_argument('--disable-blink-features=AutomationControlled') # Modifying navigator.webdriver flag to prevent selenium detection
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'}) # 模拟手机浏览器

    # Modify chromedriver.exe $cdc to '$cdc_helloIamjameshowareyou_'
    options.add_experimental_option("excludeSwitches", ['enable-automation']) # Modifying navigator.webdriver flag to prevent selenium detection

    if not os.path.exists(userdata_path):
        os.mkdir(userdata_path)
    options.add_argument(rf"--user-data-dir={userdata_path}")
    for op in chrome_options:
        options.add_argument(op)
        if 'proxy-server' in op:
            print('使用前需开启代理： mitmdump -s addons_mitmproxy.py')

    prefs = {"profile.managed_default_content_settings.images":2,
             "profile.default_content_setting_values.notifications":2,
             "profile.managed_default_content_settings.popups":2,
             "profile.managed_default_content_settings.stylesheets":2,
             "profile.managed_default_content_settings.cookies":1,
             "profile.managed_default_content_settings.javascript":1,
             "profile.managed_default_content_settings.plugins":1,
             "profile.managed_default_content_settings.geolocation":2,
             "profile.managed_default_content_settings.media_stream":2,
             }# 0 ==> default, 1 ==> Allow, 2 ==> Block.
    options.add_experimental_option('prefs', prefs)

    capa = DesiredCapabilities().CHROME
    capa["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(options=options, desired_capabilities=capa)

    driver.set_page_load_timeout(10)

    window_size = driver.get_window_size()
    driver.set_window_rect(window_size['width'] - 530, 0, 520, window_size['height'])

    return driver


def chrome_open(chrome_options=[], userdata_path=None, download_path=r"C:\Users\james\Downloads"):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    # options.add_argument('--incognito')  #  隐身模式
    # options.add_argument('--headless')

    options.add_argument("--disable-extensions")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--disable-infobars')  # 关闭浏览器上方自动测试提示
    options.add_argument('--start-maximized')  # –start-maximized 启动就最大化
    # options.add_argument('--no-startup-window')  # 关闭启动弹窗 可能导致chrome无法启动，注释不再用
    options.add_argument('--disable-blink-features=AutomationControlled') # Modifying navigator.webdriver flag to prevent selenium detection
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("detach", True) # 程序结束后chrome保持打开状态
    # Modify chromedriver.exe $cdc to '$cdc_helloIamjameshowareyou_'
    options.add_experimental_option("excludeSwitches", ['enable-automation']) # Modifying navigator.webdriver flag to prevent selenium detection

    if userdata_path is None:
        # userdata_path = fr"C:/Users/{getpass.getuser()}/AppData/Local/Google/Chrome/User Data"
        pass
    else:
        if not os.path.exists(userdata_path):
            os.mkdir(userdata_path)
        options.add_argument(rf"--user-data-dir={userdata_path}")
    for op in chrome_options:
        options.add_argument(op)
        if 'proxy-server' in op:
            print('使用前需开启代理： mitmdump -s addons_mitmproxy.py')

    prefs = {"profile.managed_default_content_settings.images":0,
             "profile.default_content_setting_values.notifications":2,
             "profile.managed_default_content_settings.popups":2,
             "profile.managed_default_content_settings.stylesheets":2,
             "profile.managed_default_content_settings.cookies":1,
             "profile.managed_default_content_settings.javascript":1,
             "profile.managed_default_content_settings.plugins":1,
             "profile.managed_default_content_settings.geolocation":2,
             "profile.managed_default_content_settings.media_stream":2,
             'download.default_directory': download_path,
             }# 0 ==> default, 1 ==> Allow, 2 ==> Block.

    options.add_experimental_option('prefs', prefs)

    capa = DesiredCapabilities().CHROME
    capa["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(options=options, desired_capabilities=capa)
    driver.set_page_load_timeout(10) # 超时设置
    driver.set_script_timeout(10)
    window_size = driver.get_window_size()
    driver.set_window_rect(window_size['width'] - 1240, 0, 1230, window_size['height'])

    return driver


# 随机向下滚动若干
def chrome_scroll_down(driver, num=None):
    if num is None:
        num = random.randint(6, 14)

    print(f"scroll down {num}")
    driver.execute_script(f"var q=document.documentElement.scrollTop={num * 100}")

def chrome_scroll_by_arrow_down(driver, times=1):
    for i in range(times):
        driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_DOWN)
        sleep(0.3)

# 切换标签
def chrome_switch_window(driver, window_id=0):
    # print(f"switch to window {window_id}")
    driver.switch_to.window(driver.window_handles[window_id])


def chrome_switch_chrome_top(driver):
    # driver.minimize_window()
    # driver.maximize_window()
    pass

def chrome_stop_load_webpage(driver):
    driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
    sleep(1)


def chrome_get_url(driver, url, xpath_locator=None, do_stop=False):
    try:
        driver.get(url)
        if xpath_locator is None:
            sleep(2)
        else:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath_locator)))
            sleep(1)
            if do_stop:
                driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
    except:
        print('Warning: get url timeout...')
        driver.minimize_window()
        driver.maximize_window()
        driver.get(url)


def chrome_get_random_search_url(driver, search_word, window_id=0):
    chrome_switch_window(driver, window_id)
    url_search_list = ["https://cn.bing.com/search?q={}", "https://m.baidu.com/s?wd={}",
                       "https://m.so.com/s?ie=utf-8&q={}", "https://m.sogou.com/web/searchList.jsp?query={}",
                       "http://so.m.jd.com/ware/search.action?keyword={}", "http://search.m.dangdang.com/search.php?keyword={}",
                      ]

    chrome_get_url(driver, url_search_list[random.randint(0,len(url_search_list)-1)].format(search_word))



def chrome_close(driver):
    driver.quit()



def wait_find_element(driver, xpath_locator, wait_time=20, sleep_time = 1):
    element = WebDriverWait(driver, wait_time).until(lambda x: x.find_element(By.XPATH, xpath_locator))
    sleep(sleep_time)

    return element

def wait_disappear_element(driver, locator, wait_time=10):
    if '//' in locator:
        locator_strategy = By.XPATH
    else:
        locator_strategy = By.CSS_SELECTOR

    WebDriverWait(driver, wait_time).until_not(EC.visibility_of_element_located((locator_strategy, locator)))





def reconnect_chrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # options.add_argument('--incognito')  #  隐身模式
    # options.add_argument('--headless')

    options.add_argument("--disable-extensions")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--disable-infobars')  # 关闭浏览器上方自动测试提示
    options.add_argument('--start-maximized')  # –start-maximized 启动就最大化
    # options.add_argument('--no-startup-window')  # 关闭启动弹窗 可能导致chrome无法启动，注释不再用
    options.add_argument('--disable-blink-features=AutomationControlled') # Modifying navigator.webdriver flag to prevent selenium detection
    options.add_argument(rf'--user-data-dir="C:/Users/{getpass.getuser()}/AppData/Local/Google/Chrome/User Data"')




    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("detach", True) # 程序结束后chrome保持打开状态
    # Modify chromedriver.exe $cdc to '$cdc_helloIamjameshowareyou_'
    # options.add_experimental_option("excludeSwitches", ['enable-automation']) # Modifying navigator.webdriver flag to prevent selenium detection
    #
    # prefs = {"profile.managed_default_content_settings.images":0,
    #          "profile.default_content_setting_values.notifications":2,
    #          "profile.managed_default_content_settings.popups":2,
    #          "profile.managed_default_content_settings.stylesheets":2,
    #          "profile.managed_default_content_settings.cookies":1,
    #          "profile.managed_default_content_settings.javascript":1,
    #          "profile.managed_default_content_settings.plugins":1,
    #          "profile.managed_default_content_settings.geolocation":2,
    #          "profile.managed_default_content_settings.media_stream":2,
    #          }# 0 ==> default, 1 ==> Allow, 2 ==> Block.
    #
    # options.add_experimental_option('prefs', prefs)

    capa = DesiredCapabilities().CHROME
    capa["pageLoadStrategy"] = "none"
    # capa["os_version"] = "11"
    # capa["device"] = "iPhone 8 Plus"
    # capa["real_mobile"] = "true"
    # capa["browserstack.local"] = "false"
    try:
        driver = webdriver.Chrome(options=options, desired_capabilities=capa)
    except:
        print("can't find a chrome open in port 9222, open it automaticly")

        cmd = '''"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222"'''
        subprocess.Popen(cmd)

        driver = webdriver.Chrome(options=options, desired_capabilities=capa)

    driver.set_page_load_timeout(10) # 超时设置
    driver.set_script_timeout(10)

    return driver


def configure_as_mobile(options, mobile_type='IPHONE_8'):
    # height, width, pixel_ratio, user_agent
    mobile_dict = {'IPHONE_8': [1334, 750, 2.0, "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"],
                   'IPHONE_XS_MAX': [2688, 1242, 3.0, "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"],
                   'GALAXY_S8': [2960, 1440, 4.0, "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36"],
                   'IPAD_MINI': [2048, 1536, 2.0, "Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"],
                   'GALAXY_TAB_10_1': [1920, 1200, 1.0, "Mozilla/5.0 (Linux; Android 8.1.0; SM-T580) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"],
                   }
    options.add_argument(f"--user-agent={mobile_dict[mobile_type][-1]}")
    return options

class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False

def reuse_chrome_example_test():
    driver = chrome_open()

    executor_url = driver.command_executor._url
    session_id = driver.session_id
    driver.get("https://login.taobao.com/member/login.jhtml")

    print(session_id)
    print(executor_url)

    driver2 = ReuseChrome(command_executor=executor_url, session_id=session_id)
    driver2.session_id = session_id
    print(driver2.current_url)
    driver2.get("https://www.baidu.com")

def save_cookies(driver, cookie_file):
    # pickle.dump(driver.get_cookies() , open(cookie_file,"wb"))
    cookies_src  = driver.get_cookies()
    cookies = {}
    for item in cookies_src:
        cookies[item['name']] = item['value']
    with open(cookie_file,'wb') as f:
        pickle.dump(cookies,f)

    return cookies


def restore_cookies(driver, cookie_file, path = '/', domain = '.mercari.com'):
    cookies = None
    if os.path.exists(cookie_file):
        with open(cookie_file,'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie({
                "domain": domain,
                "name":cookie,
                "value":cookies[cookie],
                "path": path,
                "expires":None
            })
        print("restore_cookies success")
    return cookies




def chrome_login(login_dict):

    username = login_dict.get('username', None)
    password = login_dict.get('password', None)
    userdata_path = login_dict.get('userdata_path', None)
    login_url = login_dict.get('login_url', None)
    login_el = login_dict.get('login_el', None)
    login_success_url = login_dict.get('login_success_url', None)
    login_success_el = login_dict.get('login_success_el', None)
    login_button_el = login_dict.get('login_button_el', None)
    username_el = login_dict.get('username_el', None)
    password_el = login_dict.get('password_el', None)
    recaptcha_el = login_dict.get('recaptcha_el', None)
    cookie_file = login_dict.get('cookie_file', None)
    cookie_path = login_dict.get('cookie_path', '/')
    cookie_domain = login_dict.get('cookie_domain', None)
    username_login_button_el = login_dict.get('username_login_button_el', None)

    login_done = False
    driver = chrome_open(userdata_path=userdata_path)
    if os.path.exists(cookie_file):
        chrome_get_url(driver, login_url, login_el)
        restore_cookies(driver,  cookie_file, path=cookie_path, domain=cookie_domain)
        print("Check whether has login")
        driver.get(login_success_url)
        for i in range(9):
            sleep(1)
            try:
                driver.find_element_by_xpath(login_success_el) #我的页面
                login_done = True
                save_cookies(driver, f'{username}_cookie.pickle')
                print("login succeed")
                break
            except:
                pass

            try:
                driver.find_element_by_xpath(login_button_el) # 登录按钮
                login_done = False
                break
            except:
                pass
        else:
            raise Exception("cant open url")



    if login_done is False:
        driver.get(login_url)
        if username_login_button_el is not None:
            wait_find_element(driver, username_login_button_el).click()
        wait_find_element(driver, username_el).clear()
        wait_find_element(driver, username_el).send_keys(username)
        wait_find_element(driver, password_el).clear()
        wait_find_element(driver, password_el).send_keys(password)
        try:
            # check whether there is recaptcha
            driver.find_element_by_xpath(recaptcha_el)
            # iframe=driver.find_element_by_tag_name('iframe')
            # driver.switch_to.frame(iframe)
            # ActionChains(driver).click(driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]')).perform()
            # driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[4]')
            # wait_find_element(driver, '//*[@id="recaptcha-anchor"]/div[4]')
            # driver.switch_to.default_content()
            print("Please try to login manually")
        except:
            wait_find_element(driver, '/html/body/div[1]/main/div/form/div/button').click()
        while 'login' in driver.current_url or 'passport' in driver.current_url:
            sleep(4)
            print("Waiting to login")
        save_cookies(driver, cookie_file)

    return driver

# %%
if __name__ == '__main__':
    print("Mission start!")
    driver = chrome_open()
    driver.get("https://www.taobao.com")
    # save_cookies(driver, 'tb_cookie.pickle')
    restore_cookies(driver, 'tb_cookie.pickle', ".taobao.com")

    print("Mission complete!")








