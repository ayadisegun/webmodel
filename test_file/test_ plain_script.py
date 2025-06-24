import time

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium import webdriver
from conftest import readconfig, set_data, read_data
from Utilities.baseClass import BaseUtils


#method one: to declare the webdriver object
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#second method to declare the webdriver object without stating path
# driver = webdriver.Chrome()
# driver.get("http://176.58.99.160:2025/admn93i")
# driver.implicitly_wait(15)
# driver.maximize_window()


# login, dashboard, airtime, elect, changepwd, logout

# data_file = "C:\\Users\\Segun\\PycharmProjects\\model\\test_file\\ExcelFile.xlsx",
# sheet_name = "details"
# excl_data = read_data((readconfig("data", "file")), (readconfig("data", "sheet_name")))
@pytest.mark.usefixtures("setup")
class TestLogin:
    @pytest.mark.parametrize("merch_user, merch_pass, admn_user, admn_pass, check, make", read_data())
    def test_login_admin(self, setup, merch_user, merch_pass, admn_user, admn_pass, check, make):
        driver = setup
        self.driver = driver
        utils = BaseUtils(self.driver)
        title = self.driver.title
        exp_title = "Creditswitch Merchant Portal1 | Login"
        # assert title == exp_title
        if title == exp_title:
            pass
        else:
            utils.get_screenshot("login_error")
            print("invalid title")
        assert "Creditswitch" in exp_title
        self.driver.find_element(By.XPATH, readconfig("login_page", "userbox")).send_keys(admn_user)
        self.driver.find_element(By.XPATH, readconfig("login_page", "passbox")).send_keys(admn_pass)
        time.sleep(3)  # delay to manually check recaptcha
        self.driver.find_element(By.XPATH, readconfig("login_page", "login")).click()
        # dashboard_page - side_bar, change_password_menu, service_setting, side_bar2 , logout settings_label
        self.driver.find_element(By.XPATH, readconfig("dashboard_page", "service_setting")).click()
        service_setting_header = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "settings_label")).text
        assert "Switching Module" in service_setting_header
        element = self.driver.find_element(By.XPATH, readconfig("service_settings_page", "pageindex"))
        utils.scroll_to_view(element)
        element.click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, readconfig("service_settings_page", "dashboard"))
        # side_menu = self.driver.find_elements(By.XPATH, "(//ul[@class='kt-menu__nav'])[1]/li")
        # print("length is: ", len(side_menu))
        # for i, menu in enumerate(side_menu):
        #     try:
        #         self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", side_menu)
        #         time.sleep(3)
        #         menu_text = menu.text
        #         print(f"Menu {i + 1}: {menu_text}")
        #         if menu_text == "Change Password":
        #             menu.click()
        #             break
        #     except Exception as e:
        #         print(f"Error with menu item {i + 1}: {e}")
        #         continue

        # for menu in side_menu:
        #     print(menu.text)
        #     if menu.text == "Change Password":
        #         menu.click()
        #         break
        side_bar = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "side_bar"))
        utils.scroll_to_element_by_pixel(side_bar)
        time.sleep(2)
        cpwd = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "change_password_menu"))
        cpwd.click()
        self.driver.find_element(By.XPATH, readconfig("dashboard_page", "dashboard")).click()
        side_barr = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "side_bar2"))
        utils.scroll_to_element_by_pixel(side_barr)
        logout = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "logout"))
        logout.click()
        utils.delete_cookie()
        self.driver.get(readconfig("setup", "url"))

# def test_login():  # merch_user	merch_pass
#     driver.get("http://176.58.99.160:2025/login")
#     driver.find_element(By.XPATH, "//input[@id='username']").send_keys("17000")
#     driver.find_element(By.XPATH, "//input[@id='password']").send_keys("Cswtest1.")
#     time.sleep(5)
#     driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Login')]").click()
#     time.sleep(5)
#     actual_title = driver.title
#     print("actual title is: " + actual_title)
#     exp_title = "Creditswitch Merchant Portal | Dashboard"
#     if actual_title == exp_title:
#         pass
#     elif actual_title == "Creditswitch Merchant Portal | Home":
#         driver.get("http://176.58.99.160:2025/login")
#     else:
#         print("wrong webpage returned")
#
#
# def test_airtime():
#     driver.find_element(By.XPATH, "//span[contains(text(), 'View Balance')]").click()
#     driver.find_element(By.XPATH, "//span[contains(text(), 'Service Reports')]").click()
#     driver.find_element(By.XPATH, "(//span[contains(text(), 'Airtime')])[2]").click()
#     driver.find_element(By.XPATH, "//input[@placeholder='RECIPIENT NO']").send_keys("081242")
#
#
# def test_elect():
#     # global driver
#     # global wait
#     # driver = setup
#     driver.find_element(By.XPATH, "//span[contains(text(),'Electricity')]").click()
#     driver.find_element(By.XPATH, "//input[@id='meter_cus_number']").send_keys("081242")
#     disco = Select(driver.find_element(By.XPATH, "//select[@id='disco']"))
#     disco.select_by_visible_text("KanoPrepaid")
#     driver.find_element(By.XPATH, "//input[@id='myLocalDate1']").send_keys("20062025000001")
#     driver.find_element(By.XPATH, "//input[@id='myLocalDate2']").send_keys("2006202501324051")
#     # driver.find_element(By.XPATH, "//button[@id='submitbot' and contains(text(),'Search')]").click()
#
#
# def test_logout():
#     side_menu = driver.find_element(By.XPATH, "(// div[@ id='kt_aside_menu'])[1]")
#     driver.execute_script("arguments[0].scrollTop += 500;", side_menu)
#     driver.find_element(By.XPATH, "//span[contains(text(),'Logout')]").clic

