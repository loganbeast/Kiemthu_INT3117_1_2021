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

USERNAME = "18021087@vnu.edu.vn"
PASSWORD = "Nguyenthanhson18021087@"
WRONGPASSWORD = "123456789"
class FacebookLoginTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.driver.get("https://www.facebook.com/")
        self.facebook = FacebookPage(self.driver)
        print("FacebookLoginTest starts!")

    def test_login_wrong_password(self):
        assert self.facebook.login(USERNAME, WRONGPASSWORD) == False

    def test_login_facebook(self):
        assert self.facebook.login(USERNAME, PASSWORD) 
    
    def test_sign_up_facebook(self):
        kwargs = {"lastname": "Son", "firstname": "Nguyen", 
                    "email": "test18021087@gmail.com", "password": "ASDAS@12312gsd@",
                    "day": 18, "month": 9, "year": 2000}
        assert self.facebook.sign_up(**kwargs)

    def tearDown(self) -> None:
        print("Test login was finished successully!")
        self.driver.close
        self.driver.quit()

class FacebookFeatureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.facebook = FacebookPage(self.driver)
        print("FacebookFeatureTest starts!")
        self.facebook.login(USERNAME, PASSWORD)
        time.sleep(3)

    def test_posting_and_like(self):
        assert self.facebook.post("Test posting content!!")
        time.sleep(3)
        assert self.facebook.like()
    
    def test_search_friend(self):
        kwargs = {"name": "Nguyen Son", "city": "Ha Noi", "university": "Dai hoc cong nghe"}
        assert self.facebook.searching_friend(**kwargs)

    def test_send_friend_request(self):
        url = "https://www.facebook.com/oinfamous"
        assert self.facebook.send_friend_request(url)

    def test_send_message(self):
        assert self.facebook.send_message(100011308354722, "Test send message")

    def tearDown(self) -> None:
        print("Test posting finished successully!")
        self.driver.close
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

