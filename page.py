import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
PATH = "/home/logan/Desktop/selenium_test/chromedriver_linux64/chromedriver"
from helper.driver_helper import create_driver, wait_click, wait_until_visible, try_input

class BasePage(object):
    """
    Base page for initializing every page
    """
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

class FacebookPage(BasePage):
    """
    Through facebook page
    """
    user_name = '18021087@vnu.edu.vn'
    password = 'Nguyenthanhson18021087@'
    def login(self, user_name: str, password: str):
        self.driver.get("https://www.facebook.com/")
        try:
            username = self.driver.find_element_by_xpath('//input[@id="email"]')
            username.send_keys(user_name)
            time.sleep(1)

            username = self.driver.find_element_by_xpath('//input[@id="pass"]')
            username.send_keys(password)
            time.sleep(1)

            button_next = self.driver.find_element_by_xpath("//button[@name='login']")
            button_next.click()
            time.sleep(5)
            
            # check
            current_driver = self.driver.current_url
            if "welcome" in current_driver:
                return True
            return False
        except WebDriverException as e:
            print(e)
            return False
    
    def sign_up(self, **kwargs):
        SING_UP_BUTTON_XPATH = "//a[@role='button' and @data-testid='open-registration-form-button']"
        LASTNAME = "//input[@name='lastname']"
        FIRSTNAME = "//input[@name='firstname']"
        EMAIL = "//input[@name='reg_email__']"
        RECONFIRM_EMAIL = "//input[@name='reg_email_confirmation__']"
        PASSWORD = "//input[@name='reg_passwd__']"
        DAY = "//select[@id='day']"
        MONTH = "//select[@id='month']"
        YEAR = "//select[@id='year']"
        MALE = "//label[text()='Nam' or text()='Male']"
        SIGN_UP_SUBMIT = "//button[(text()='Đăng ký' or text()='Sign Up') and @name='websubmit']"

        msg_lastname = kwargs.get('lastname', '')
        msg_firstname = kwargs.get('firstname', '')
        msg_email = kwargs.get('email', '')
        msg_password = kwargs.get('password', '')
        msg_day = kwargs.get('day', '')
        msg_month = kwargs.get('month', '')
        msg_year = kwargs.get('year', '')
        if not wait_click(self.driver, [SING_UP_BUTTON_XPATH]):
            print("Can not click sign up button")
            return False
        time.sleep(3)
        driver = self.driver
        try_input(driver, msg_lastname, LASTNAME)
        try_input(driver, msg_firstname, FIRSTNAME)
        try_input(driver, msg_email, EMAIL)
        time.sleep(3)
        wait_until_visible(driver, RECONFIRM_EMAIL )
        try_input(driver, msg_email, RECONFIRM_EMAIL)
        try_input(driver, msg_password, PASSWORD)
        try_input(driver, msg_day, DAY)
        try_input(driver, msg_month, MONTH)
        try_input(driver, msg_year, YEAR)

        wait_click(driver, [MALE])
        time.sleep(2)

        if wait_click(driver, [SIGN_UP_SUBMIT]):
            time.sleep(5)
            print("Sign up successfully")
            return True
        return False

    def post(self, content: str):
        POST_AREA = "//div[@aria-label='Tạo bài viết']//div[@role='button']"
        DIALOG = "//div[@role='dialog']//form[@method='POST']"
        SUBMIT_BUTTON = f"{DIALOG}//div[@aria-label='Đăng' and @role='button']"
        
        try: 
            self.driver.get("https://www.facebook.com/")
            time.sleep(3)
            if not wait_until_visible(self.driver, POST_AREA):
                return False
            self.driver.find_element_by_xpath(POST_AREA).click()
            time.sleep(5)
            wait_until_visible(self.driver, f"{DIALOG}//div[@contenteditable='true']//div[@data-contents='true']")
            dialog_input_content = self.driver.find_elements_by_xpath(f"{DIALOG}//div[@contenteditable='true']//div[@data-contents='true']") 
            if not len(dialog_input_content):
                print("Can not find input area")
                return False
            dialog_input_content[0].send_keys(content)
            time.sleep(3)
            if wait_click(self.driver, [SUBMIT_BUTTON]):
                print("Post successfully!")
                return True
            else: 
                return False
        except Exception as e:
            print(e)
            return False
    
    def send_message(self, id:int, content: str):
        try: 
            # 100011308354722
            MESSAGE_INPUT = "//div[(@aria-label='Nhắn tin' or @aria-label='Message') and @contenteditable='true']"
            SEND_BUTTON = "//div[(@aria-label='Nhấn Enter để gửi' or @aria-label='Send') and @role='button']"
            driver = self.driver
            driver.get(f'https://www.facebook.com/messages/t/{id}')
            time.sleep(3)
            
            message_input = driver.find_element_by_xpath(MESSAGE_INPUT)
            message_input.click()
            try_input(driver, content, MESSAGE_INPUT)
            
            # send message click
            try:
                message_input.send_keys(Keys.ENTER)
                time.sleep(5)
                return True
            except Exception as e:
                print(e)
                wait_click(driver, SEND_BUTTON)
                time.sleep(5)
                return True
        except Exception as e:
            print(e)
            return False
            
