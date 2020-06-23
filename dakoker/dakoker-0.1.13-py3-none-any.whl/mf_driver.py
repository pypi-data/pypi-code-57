# coding:utf-8
import os
import pickle
import getpass
import keyring

from src.utils.colors import Colors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class MFDriver(object):
    TIMEOUT = 3
    CORP_ID = 'CORP_ID'
    USER_ID = 'USER_ID'
    USER_PASS = 'USER_PASS'
    MF_SERVICE = 'MF_SERVICE'
    USER_INFO_PATH = os.environ['HOME'] + '/.local/share/dakoker'
    ROOT_URL = "https://attendance.moneyforward.com"
    LOGIN_URL = ROOT_URL + "/employee_session/new"
    MYPAGE_URL = ROOT_URL + "/my_page"

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)

    def login(self):
        user_info = self.get_user_info()
        if not user_info:
            user_info = {}
            user_info[self.CORP_ID] = input("company ID: ")
            user_info[self.USER_ID] = input("user ID or email address: ")
            user_info[self.USER_PASS] = getpass.getpass("password: ")
        else:
            print("Login cache loaded...")

        self.driver.get(self.LOGIN_URL)

        return self.login_with_user_info(user_info)

    def login_with_user_info(self, user_info):
        self.driver.find_element_by_id(
            "employee_session_form_office_account_name"
        ).send_keys(user_info[self.CORP_ID])
        self.driver.find_element_by_id(
            "employee_session_form_account_name_or_email"
        ).send_keys(user_info[self.USER_ID])
        self.driver.find_element_by_id(
            "employee_session_form_password"
        ).send_keys(user_info[self.USER_PASS])

        self.driver.find_element_by_class_name(
            "attendance-before-login-card-button"
        ).click()

        return self.check_login(user_info)

    def check_login(self, user_info):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "attendance-card-title")
                )
            )
            self.save_user_info(user_info)
            print("Login successful.")
            return True

        except TimeoutException:
            if self.driver.find_elements(By.CLASS_NAME, "is-error") != 0:
                Colors.print(
                    Colors.RED,
                    "Login Failed: company ID, user ID or password is wrong."
                )
                self.remove_user_info()
                return self.login()
            else:
                Colors.print(Colors.RED, "Login Timeout.")
                return False

    def get_user_info(self):
        if os.path.isfile(self.USER_INFO_PATH + '/user_info.pkl'):
            with open(self.USER_INFO_PATH + '/user_info.pkl', "rb") as f:
                info = pickle.load(f)
                passwd = keyring.get_password(
                    self.MF_SERVICE, info[self.USER_ID])
                if passwd:
                    info[self.USER_PASS] = passwd
                    return info

        return None

    def remove_user_info(self):
        if os.path.isfile(self.USER_INFO_PATH + '/user_info.pkl'):
            os.remove(self.USER_INFO_PATH + "/user_info.pkl")

    def save_user_info(self, user_info):
        if not os.path.isdir(self.USER_INFO_PATH):
            os.makedirs(self.USER_INFO_PATH)

        keyring.set_password(
            self.MF_SERVICE,
            user_info[self.USER_ID],
            user_info[self.USER_PASS])

        del user_info[self.USER_PASS]
        pickle.dump(user_info,
                    open(self.USER_INFO_PATH + "/user_info.pkl", "wb"))
