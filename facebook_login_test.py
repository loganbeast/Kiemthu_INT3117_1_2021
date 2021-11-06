import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
PATH = "/home/logan/Desktop/selenium_test/chromedriver_linux64/chromedriver"
from helper.driver_helper import create_driver
from page import FacebookPage
from page import ZingNew

USERNAME = "sonnguyenthanh.uet18@gmail.com"
PASSWORD = "Nguyenthanhson18021087@"
WRONGPASSWORD = "123456789"


class FacebookLoginTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.driver.get("https://www.facebook.com/")
        self.facebook = FacebookPage(self.driver)

    def test_login_facebook(self):
        # wrong password case
        assert self.facebook.login(USERNAME, WRONGPASSWORD, True) == False
        # correct password case 
        assert self.facebook.login(USERNAME, PASSWORD, True) == True
        print('=== TEST LOGIN SUCCESS ===')
    
    def test_sign_up_facebook(self):
        kwargs = {"lastname": "Son", "firstname": "Nguyen", 
                    "email": "test18021087@gmail.com", "password": "ASDAS@12312gsd@",
                    "day": 18, "month": 9, "year": 2000}
        assert self.facebook.sign_up(**kwargs) == True
        print('=== TEST SIGNUP SUCCESS ===')

    def tearDown(self) -> None:
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()