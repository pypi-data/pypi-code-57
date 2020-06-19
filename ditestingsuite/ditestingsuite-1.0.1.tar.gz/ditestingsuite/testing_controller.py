import inspect
import time
from pprint import pprint

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ditestingsuite.action_enum import actionEnum

class testingController:
    MAX_ATTEMPT = 120
    WAITING_TIME = 5
    RESULT_PATH = './results/'

    def __init__(self):

        self.action_enum = actionEnum()
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.headless=True
        WINDOW_SIZE = "1920,1080"
        # chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.set_script_timeout(self.WAITING_TIME)

        self.driver.implicitly_wait(self.WAITING_TIME)
        # self.username = username
        # self.password = password
        # self.usertype = usertype

    def __find_elements(self, location):
        try:
            return self.driver.find_elements_by_css_selector(location)
        except TimeoutException:
            return None

    def __check_if_exists(self, location):
        try:
            return self.driver.find_element_by_css_selector(location)
        except Exception:
            return None

    def __click_buttons(self, location):
        try:
            for elem in self.__find_elements(location):
                elem.click()
        except TypeError:
            pass

    def __click_button(self, location):
        button = WebDriverWait(driver=self.driver, timeout= self.MAX_ATTEMPT* self.WAITING_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, location))
        )
        self.__scroll_shim(location=location)
        button.click()

    def __type_content(self, location, content,waited_time=None):
        if waited_time is not None:
            time.sleep(waited_time)
        # time.sleep(self.WAITING_TIME)
        text_box = self.__find_element(location=location)
        text_box.clear()
        # time.sleep(5)
        text_box.send_keys(content)

    def __wait_time(self, waited_time=None):
        if waited_time is None:
            waited_time = self.WAITING_TIME
        time.sleep(waited_time)

    def __visit(self, url):
        self.driver.get(url=url)

    def __send_key(self, location, key):
        self.__find_element(location).send_keys(key)

    def __click_if_exists(self, location):
        if self.__check_if_exists(location) is not None:
            self.__click_button(location)

    def __scroll_shim(self, location,elem=None):
        if elem is None:
            elem = self.__find_element(location)
        self.driver.execute_script("arguments[0].scrollIntoView()", elem)

    def __scroll_screenshot(self, location, file_name=None):
        calframe = inspect.stack()[3][3]
        pprint(calframe)
        if file_name is None:
            file_name = self.RESULT_PATH + calframe + '.png'
        else:
            file_name = self.RESULT_PATH + file_name + '.png'
        elem = self.__find_element(location)
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        self.driver.set_window_size(S('Width'), S(
            'Height'))  # May need manual adjustment
        elem.screenshot(file_name)


    def __normal_screen_shot(self, location=None, file_name=None,waited_time=None):
        if waited_time is None:
            waittime = self.WAITING_TIME
        else:
            waittime = waited_time
        calframe = inspect.stack()[3][3]
        if location is not None:
            self.__find_element(location)
            self.__scroll_shim(location)
        time.sleep(waittime)
        if file_name is None:
            self.driver.save_screenshot(self.RESULT_PATH + calframe + '.png')
        else:
            self.driver.save_screenshot(self.RESULT_PATH + calframe + file_name + '.png')

    def act_performance_list(self, performance_list):
        performance_list = performance_list
        self.__perform_actions(performance_list=performance_list)

    def get_current_url(self):
        return self.driver.current_url

    def get_url_by_text(self, content):
        return self.driver.find_element_by_link_text(content)

    def __perform_actions(self, performance_list):
        for performance in performance_list:
            action = performance['action']
            location = None
            content = None
            url = None
            file_name = None
            waited_time = None
            key = None
            try:
                location = performance['location']
            except Exception as exception:
                pass
            try:
                content = performance['content']
            except Exception as exception:
                pass
            try:
                url = performance['url']
            except Exception as exception:
                pass
            try:
                file_name = performance['file_name']
            except Exception as exception:
                file_name = None
                pass
            try:
                waited_time = performance['waited_time']
            except Exception as exception:
                waited_time = None
                pass
            try:
                key = performance['key']
            except Exception as exception:
                pass

            if action == self.action_enum.CLICK_ELEMENT:
                self.__click_button(location=location)
            elif action == self.action_enum.CLICK_ELEMENTS:
                self.__click_buttons(location=location)
            elif action == self.action_enum.TYPE:
                self.__type_content(location=location, content=content,waited_time=waited_time)
            elif action == self.action_enum.VISIT:
                self.__visit(url=url)
            elif action == self.action_enum.CHECK_ELEM_EXISTS:
                if self.__check_if_exists(location) is None:
                    break
            elif action == self.action_enum.NORMAL_SCREEN_SHOT:
                self.__normal_screen_shot(location=location, file_name=file_name,waited_time=waited_time)
            elif action == self.action_enum.CLICK_IF_EXISTS:
                self.__click_if_exists(location)
            elif action == self.action_enum.WAIT_ELEM:
                self.__find_element(location)
            elif action == self.action_enum.SCROLL_SCREEN_SHOT:
                self.__scroll_screenshot(location, file_name)
            elif action == self.action_enum.WAIT_TIME:
                self.__wait_time(waited_time=waited_time)
            elif action == self.action_enum.SCROLL_TO_ELEM:
                self.__scroll_shim(location)
            elif action == self.action_enum.SEND_KEY:
                self.__send_key(location, key)
            elif action == self.action_enum.CLICK_TEXT:
                self.__click_link_by_text(content)
            elif action == self.action_enum.REFRESH:
                self.driver.refresh()
            elif action == self.action_enum.CLICK_INTO_IFRAME:
                self.__click_buttons_by_class(location)
            elif action == self.action_enum.UNCHECK_BOX:
                self.__uncheck_box(location)

    def __fine_button(self,location):
        try:
            return WebDriverWait(self.driver, self.MAX_ATTEMPT *  self.WAITING_TIME).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, location)))
        except TimeoutException:
            print("Location: " + location + " is not searchable")
        return None


    def __find_element(self, location):
        try:
            return WebDriverWait(self.driver, self.MAX_ATTEMPT * self.WAITING_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, location)))
        except TimeoutException:
            print("Location: " + location + " is not searchable")
        return None

    def __find_elem_by_class_name(self, location):
        try:
            return WebDriverWait(self.driver, self.MAX_ATTEMPT * self.WAITING_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, location)))
        except TimeoutException:
            print("Location: " + location + " is not searchable")
        return None

    def __click_elements(self, location):
        elems = self.__find_elements(location)
        for elem in elems:
            self.__scroll_shim(elem)
            elem.click()

    def __click_buttons_by_class(self, location):
        self.driver.execute_script("""
        var checkExist = setInterval(function(){
            if($('""" + location + """').length){
                $('""" + location + """').click()
            }
        },100);
        
        """)
        # iframes = self.driver.find_elements_by_tag_name('iframe')
        # print (len(iframes))
        # for i in range(len(iframes)):
        #     self.driver.switch_to.default_content()
        #     iframe = iframes[i]
        #     self.driver.switch_to.frame(iframe)
        #     self.driver.find_element_by_class_name(location).click()
        #     # self.driver.find_element_by_class_name('button.save').click()
        #
        # self.driver.switch_to.default_content()

    def __click_link_by_text(self, content):
        elem = WebDriverWait(driver=self.driver, timeout=self.WAITING_TIME).until(
            EC.element_to_be_clickable((By.LINK_TEXT, content))
        )
        elem.click()

        # self.driver.find_element_by_link_text(content).click()

    def delete_schema(self,url, table_location,name_location,project_key,button_location_format,confirm_delete_location):
        self.__visit(url)
        while self.__has_item_start_with_name(table_location,name_location,project_key):
            lists = self.driver.find_elements_by_css_selector(table_location)
            for i in range(1, len(lists) + 1):
                name = self.driver.find_element_by_css_selector(name_location.format(str(i))).text
                if name.startswith(project_key):
                    button = self.driver.find_element_by_css_selector(button_location_format.format(str(i)))
                    self.__scroll_shim(location=None, elem=button)
                    print ("Deleting: " +name)
                    button.click()
                    self.__click_button(confirm_delete_location)
                    break

    def get_elements_by_css_selector(self, css_selector):
        return self.driver.find_elements_by_css_selector(css_selector)

    # def __delete_schema(self,name,table_selector):
    #     table_row = self.driver.find_elements_by_css_selector(table_selector)
    #     for i in range(1, len(table_row)+1):
    #         if(self.driver.find_element_by_css_selector())

    def __has_item_start_with_name(self, table_location, name_location, project_key):
        table_row_list = self.driver.find_elements_by_css_selector(table_location)
        for i in range(1, len(table_row_list) + 1):
            name = self.driver.find_element_by_css_selector(name_location.format((str(i)))).text
            if self.driver.find_element_by_css_selector(name_location.format((str(i)))).text.startswith(project_key):
                return True
        return False

    def __uncheck_box(self,location):
        check_box = self.__find_element(location)
        if (check_box.is_selected()):
            check_box.click()