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
from helper.driver_helper import create_driver, go_to_element, wait_click, wait_until_visible, try_input

class BasePage(object):
    """
    Base page for initializing every page
    """
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

class ZingNew(BasePage):

    def search(self):
        GOOGLE_SEARCH = "//input[@aria-label='Search' or @aria-label='Tìm kiếm' or @name='q']"
        driver = self.driver
        driver.get('https://www.google.com/')
        
        wait_until_visible(driver, GOOGLE_SEARCH, 10)
        # driver.find_element_by_xpath(GOOGLE_SEARCH).click()
        try_input(driver, "Zing New", GOOGLE_SEARCH)
        try_input(driver, Keys.ENTER, GOOGLE_SEARCH)
        time.sleep(3)

        wait_click(driver, ["//a[@href='https://zingnews.vn/']"])
        return "ZINGNEWS.VN" in driver.title

    def search_zingnews(self, content: str):
        driver = self.driver
        SEARCH_INPUT= "//input[@id='search_keyword']"
        SEARCH_RESULT = "//section[@id='search-result']//p//strong"
        driver.find_element_by_xpath("//button[@id='search_button']").click()
        time.sleep(3)
        try_input(driver, content, SEARCH_INPUT)
        try_input(driver, Keys.ENTER, SEARCH_INPUT)
        time.sleep(5)

        return 0 != driver.find_element_by_xpath(SEARCH_RESULT).text
    
    def search_fail(self, content: str):
        SEARCH_BOX = "//div[@class='search-box']//input"
        search_box = self.driver.find_element_by_xpath(SEARCH_BOX)
        search_box.clear()
        time.sleep(3)
        search_box.send_keys(content)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)
        return "Không tìm thấy kết quả" in self.driver.find_element_by_xpath("//p[@class='message-not-found']").text





        


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
                time.sleep(5)
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
            try_input(driver, "Testing successfully!")
            try_input(driver, "End testing")
            
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
    
    def like(self):
        try:
            time.sleep(5)
            LIKE_XPATH = "//div[@aria-label='Thích' or @aria-label='Like']"
            LIKE_ICON_XPATH = "//div[@aria-label='Thích' or @aria-label='Like']//span[text()='Thích' or text()='Like']"
            # go to first like button
            go_to_element(self.driver, LIKE_ICON_XPATH)
            
            like_button_els = self.driver.find_elements_by_xpath(LIKE_XPATH)
            if not len(like_button_els):
                print('Like button not found!')
                return False
            like_button_els[0].click()
            icon = self.driver.find_element_by_xpath(LIKE_ICON_XPATH)
            icon_color = icon.get_attribute('style')
            print(icon_color)
            time.sleep(5)
            return True 
        except Exception as e:
            print(f"Failed here: {e}")
            return False
    def send_friend_request(self, url: str):
        # https://www.facebook.com/oinfamous
        try:
            self.driver.get(url)
            ADD_FRIEND = "//div[@aria-label='Thêm bạn bè' and @role='button']"
            DELETE_FRIEND = "//div[@aria-label='Hủy lời mời' and @role='button']"
            if not wait_click(self.driver, [ADD_FRIEND]):
                print('Add friend request not found!')
                return False
            if len(self.driver.find_elements_by_xpath(DELETE_FRIEND)) > 0:
                print("Send friend request successfully!")
                time.sleep(7)
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def searching_friend(self, **kwargs):
        try:
            driver = self.driver
            SEARCH_INPUT = "//input[@aria-label='Tìm kiếm trên Facebook' and @type='search']"
            SEARCH_RESULT = "//div[@aria-label='Kết quả tìm kiếm']//div[@role='feed']/div/div"
            PEOPLE_SEARCH = "//span[text()='Mọi người']"

            FRIEND_XPATH = "//a[contains(@aria-label, 'Nguyễn Sơn (Logan)')]"
            # CITY_SEARCH = "//span[text()='Tỉnh/Thành phố']"
            # STUDY_SEARCH = "//span[text()='Học vấn']"
            name = kwargs.get('name', '')
            city = kwargs.get('city', '')
            university = kwargs.get('university', '')
            
            wait_until_visible(driver, SEARCH_INPUT)
            search_els = driver.find_element_by_xpath(SEARCH_INPUT)
            # try to input search content
            search_els.click()
            try_input(driver, name, SEARCH_INPUT)
            try_input(driver, Keys.ENTER, SEARCH_INPUT)

            time.sleep(5)
            wait_click(self.driver, [PEOPLE_SEARCH])

            # wait_click(self.driver, [CITY_SEARCH])
            # try_input(driver, city, CITY_SEARCH)
            # time.sleep(2)
            # try_input(driver, Keys.TAB, CITY_SEARCH)

            # wait_click(self.driver, [STUDY_SEARCH])
            # try_input(driver, university, STUDY_SEARCH)
            # time.sleep(2)
            # try_input(driver, Keys.TAB, STUDY_SEARCH)
            
            #time sleep
            time.sleep(3)
            search_result_els = driver.find_elements_by_xpath(SEARCH_RESULT)
            if len(search_result_els) > 0:
                friend_test = driver.find_elements_by_xpath(FRIEND_XPATH)
                if len(friend_test) > 0:
                    print("Find Nguyen Son successfully!")
                    time.sleep(7)
                    return True
            return False
        except Exception as e:
            print(e)
            return False


        