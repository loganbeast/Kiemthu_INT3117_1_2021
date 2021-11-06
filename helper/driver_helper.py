import time
import traceback
from typing import List
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

#========
#===plz config correct path to Chrome driver when you run program. 
#========
PATH = "/home/logan/Desktop/selenium_test/chromedriver_linux64/chromedriver"
#========
#===plz config correct path to Chrome driver when you run program. 
#========
def create_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    # normal driver
    options.add_argument("--start-maximized")
    options.add_argument("--enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    return driver

def wait_until_visible(driver: WebDriver, selector: str, timeout=5, method=None):
    if method == None:
        if "//" in selector:
            method = 'xpath'
        else:
            method = 'css_selector'
    try:
        if method == 'xpath':
            return WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath(selector)) 
        else:
            return WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_css_selector(selector))
    except Exception as e:
        print(f"Element still not visible after timeout: {timeout} seconds")
        return None

def find(driver: WebDriver, selector: str, method=None):    
    if '//' in selector:
        method = By.XPATH
    else:
        method = By.CSS_SELECTOR
    if method == By.XPATH:
        return driver.find_elements_by_xpath(selector)
    else:
        return driver.find_elements_by_css_selector(selector)

def wait_click(driver: WebDriver, selectors: List[str], timeout=10, method: str = None):
    try:
        if WebDriverWait(driver, timeout).until(
                lambda d: any([any([x.is_enabled() for x in find(driver, i, method)]) for i in selectors])):
            found = [find(driver, i) for i in selectors]
            items = [item for sublist in found for item in sublist]
            if items:
                time.sleep(2)
                items[0].click()
                return True
    except Exception as e:
        print(f"Not found. {selectors} {e}")
    return False

def wait_until_clickable(driver: WebDriver, selector: str, timeout: int=5, method=None):
    if not method:
        if "//" in selector:
            method = By.XPATH
        else:
            method = By.CSS_SELECTOR
    try :
        _ = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(method, selector))
        return True
    except Exception as e:
        print(e)
    return False

def go_to_element(driver: WebDriver, selector, method=None, element=None, scroll_by="-300"):
    try:
        if method is None:
            if "//" in selector:
                method = "xpath"
            else:
                method = "css_selector"

        if not element:
            if method == "xpath":
                element = driver.find_element_by_xpath(selector)
            else:
                element = driver.find_element_by_css_selector(selector)

        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

        except Exception as err:
            print("Error scrolling to element using ActionChains!", selector)
            print(err)
            print(traceback.format_exc())

        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
        # print "Scrolled successfully to element using javascript!", selector

        except Exception as err:
            print("Error scrolling to element using javascript!", selector)
            print(err)
            print(traceback.format_exc())

        driver.execute_script("window.scrollBy(0, %s);" % scroll_by)

        return True

    except Exception as err:
        print("Could not scroll to element")
        print(err)
        print(traceback.format_exc())


def try_input(driver: WebDriver, msg, selector=""):
    try:
        element = driver.find_element_by_xpath(selector)
        element.send_keys(msg)
        time.sleep(2)
        return True
    except:
        return False