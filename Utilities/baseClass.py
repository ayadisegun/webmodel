import datetime
import os
from datetime import datetime
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ElementNotInteractableException
)
import openpyxl
import pytest
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from test_file import conftest
from selenium.webdriver.remote.webdriver import WebDriver


class BaseUtils:
    def __init__(self, driver):
        self.driver = driver

    def get_screenshot(self, filename: str):
        screenshot_dir = conftest.readconfig("setup", "screenshot_dir")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshot_dir, f"{filename}_{timestamp}.png")
        self.driver.get_screenshot_as_file(path)

    def scroll_to_element(self, element):
        """Scroll to a specific element"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down(self):
        """Scroll by specific pixel amount"""
        self.driver.execute_script("window.scrollBy(0, 300);")

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by_pixels(self, x=0, y=800):
        """Scroll by specific pixel amount"""
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_to_element_by_pixel(self, element):
        self.driver.execute_script("arguments[0].scrollTop += 600;", element)

    def wait_and_click(self, locator, timeout=10):
        """Wait for element and click"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def wait_until_present(self, locator):
        mywait = WebDriverWait(self.driver, 10)
        mywait.until(EC.presence_of_element_located(locator))

    # def hover_over_element(self, element):
    #     """Hover over an element"""
    #     ActionChains(self.driver).move_to_element(element).perform()

    def selectoption_bytext(self, locator, text):
        driver = self.driver
        optns = Select(driver.find_element(locator))
        optns.select_by_visible_text(text)

    def mouse_over(self, element):
        ele = self.driver.find_element(element)
        ActionChains(self.driver).move_to_element(ele).perform()

    def double_click(self, element):
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()

    def delete_cookie(self):
        self.driver.delete_all_cookies()

    def delete_session(self):
        self.driver.execute_script("window.sessionStorage.clear();")

    def delete_localstorage(self):
        self.driver.execute_script("window.localStorage.clear();")

    def quit(self):
        self.driver.quit()






class HomepageData:
    homepagetestData = [{"firstname": "segun", "email": "xyz@gmail.com", "password": "password123", "gender": "Male"}, {"firstname": "Ade", "email": "abc@gmail.com", "password": "passwordfemale", "gender": "Female"}]

# Android Keycodes
# 0 - 7
# 1 - 8
# 2 - 9
# 3 - 10
# 4 - 11
# 5 - 12
# 6 - 13
# 7 - 14
# 8 - 15
# 9 -16
# 10 -
# 11 - 227
# 12 - 228
# Shift - 59
# back - 4
# home - 3
# recent app - 187
# driver.launch_app()  # Reopen the app
# driver.background_app(5)  # Minimize the app for 5 seconds
# power key 26
# volume up 24
# volume down 25
#delete - 67
#Enter - (66)

