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

class FacebookFeatureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.facebook = FacebookPage(self.driver)
        self.facebook.login(USERNAME, PASSWORD)
        time.sleep(3)

    def test_posting_and_like(self):
        assert self.facebook.post("Test posting content!!")
        time.sleep(3)
        assert self.facebook.like()
        print('=== TEST CREATE & LIKE POST SUCCESS ===')
        
    
    def test_search_friend(self):
        kwargs = {"name": "Nguyen Son", "city": "Ha Noi", "university": "Dai hoc cong nghe"}
        assert self.facebook.searching_friend(**kwargs)
        print('=== TEST SEARCH FRIEND SUCCESS ===')

    def test_send_friend_request(self):
        url = "https://www.facebook.com/oinfamous"
        assert self.facebook.send_friend_request(url)
        print('=== TEST SEND FRIEND REQUEST SUCCESS ===')

    def test_send_message(self):
        assert self.facebook.send_message(100011308354722, "Test send message")
        print('=== TEST SEND MESSAGE SUCCESS ===')

    def tearDown(self) -> None:
        self.driver.close
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()