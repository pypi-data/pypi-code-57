# coding:utf-8
import os
import pickle
import getpass

from src.utils.colors import Colors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


class MFDriver(object):
    TIMEOUT = 3
    COOKIE_PATH = os.environ['HOME'] + '/.local/share/dakoker'
    ROOT_URL = "https://attendance.moneyforward.com"
    LOGIN_URL = ROOT_URL + "/employee_session/new"
    MYPAGE_URL = ROOT_URL + "/my_page"

    def __init__(self):
        self.cookies = self.load_cookies()

        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)

    def login(self):
        if self.cookies:
            self.driver.get(self.ROOT_URL)
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
            self.driver.get(self.MYPAGE_URL)
            return self.check_login()
        else:
            self.driver.get(self.LOGIN_URL)
            return self.stdin_login()

    def stdin_login(self):
        company_id = input("company ID: ")
        user_id = input("user ID or your email address: ")
        user_pass = getpass.getpass("password: ")

        self.driver.find_element_by_id(
            "employee_session_form_office_account_name"
        ).send_keys(company_id)
        self.driver.find_element_by_id(
            "employee_session_form_account_name_or_email"
        ).send_keys(user_id)
        self.driver.find_element_by_id(
            "employee_session_form_password"
        ).send_keys(user_pass)

        self.driver.find_element_by_class_name(
            "attendance-before-login-card-button"
        ).click()

        return self.check_login()

    def check_login(self):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "attendance-card-title")
                )
            )
            self.save_cookie()
            print("Login successful.")

            return True
        except TimeoutException:
            if self.driver.find_elements(By.CLASS_NAME, "is-error") != 0:
                Colors.print(
                    Colors.RED,
                    "Login Failed: company ID, user ID or password is wrong."
                )
            else:
                Colors.print(Colors.RED, "Login Timeout")

            return False

    def load_cookies(self):
        if os.path.exists(self.COOKIE_PATH + "/cookie.pkl"):
            print("cookie loading...")
            with open(self.COOKIE_PATH + "/cookie.pkl", "rb") as f:
                return pickle.load(f)

        return None

    def save_cookie(self):
        if not os.path.exists(self.COOKIE_PATH):
            os.makedirs(self.COOKIE_PATH)
        pickle.dump(self.driver.get_cookies(),
                    open(self.COOKIE_PATH + "/cookie.pkl", "wb"))
