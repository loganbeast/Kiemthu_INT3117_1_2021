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

class ZingNewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.zingnews = ZingNew(self.driver)

    def test_zingnew_search_from_google(self):
        content = 'Pháp luật'
        content_1 = "FAILED TEST"
        #check search zing new from google
        assert self.zingnews.search()
        #check search article form Zingnew
        assert self.zingnews.search_zingnews(content)
        #check search failed case
        assert self.zingnews.search_fail(content_1)
        print('=== TEST ZING SEARCH SUCCESS ===')
    
    def tearDown(self) -> None:
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()