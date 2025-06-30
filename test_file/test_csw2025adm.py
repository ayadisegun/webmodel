import sys
import time

import pytest
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ElementNotInteractableException
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.select import Select


from POM.login_page import LoginPage
from test_file.conftest import readconfig, set_data, read_data
from Utilities.baseClass import BaseUtils


@pytest.mark.usefixtures("setup")
class TestLogin1:
    @pytest.mark.parametrize("merch_user, merch_pass, admn_user, admn_pass, current_password, new_password, "
                             "wrong_confirm, merch_name, category, service, provider", read_data())
    def test_login_admin(self, setup, merch_user, merch_pass, admn_user, admn_pass, current_password, new_password,
                         wrong_confirm, merch_name, category, service, provider):
        driver = setup
        self.driver = driver
        utils = BaseUtils(self.driver)
        title = self.driver.title
        exp_title = "Creditswitch Merchant Portal | Login"
        if title == exp_title:
            pass
        else:
            utils.get_screenshot("wrong_site")
            print("invalid title")
        assert "Creditswitch" in title
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 1, 12, "Url_title")
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 2, 12, title)
        login_page = LoginPage(self.driver)
        utils.get_screenshot("login_page")
        login_page.username_field().send_keys(admn_user)
        login_page.password_field().send_keys(admn_pass)
        time.sleep(3)  # delay to manually check recaptcha
        dashboard_page = login_page.login_button()
        try:
            servicesettings_page = dashboard_page.service_setting()
            servicesettings_page.set_service().click()
        except NoSuchElementException as e:
            print(f"Test failed: Element not found - {e}")
            utils.get_screenshot("login_error_No_element")
            utils.quit()
            sys.exit(1)
        except Exception as e:  # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            utils.get_screenshot("login_error_exception")
            utils.quit()
            sys.exit(1)
        service_setting_headertext = servicesettings_page.servicesetting_header().text
        assert "Switching Module" in service_setting_headertext
        utils.double_click(servicesettings_page.set_merchant())
        servicesettings_page.search_merchant().send_keys(merch_name)
        servicesettings_page.selectfetched_merchant().click()
        utils.double_click(servicesettings_page.click_category())
        cate_list = servicesettings_page.search_category()
        print("category list length is: ", len(cate_list))
        for cate in cate_list:
            cate_text = cate.text
            if cate_text == category:
                cate.click()
                time.sleep(1)
                break
        time.sleep(1)
        utils.double_click(servicesettings_page.click_service())
        serv_list = servicesettings_page.search_service()
        print("service list length is: ", len(serv_list))
        for serv in serv_list:
            serv_text = serv.text
            if serv_text == service:
                serv.click()
                time.sleep(1)
                break
        servicesettings_page.servicesetting_header().click()
        time.sleep(1)
        utils.double_click(servicesettings_page.click_provider())
        prov_list = servicesettings_page.search_provider()
        print("provider list length is: ", len(prov_list))
        for prov in prov_list:
            prov_text = prov.text
            if prov_text == provider:
                prov.click()
                break
        dashboard_page = servicesettings_page.click_dashboard()
        side_bar = dashboard_page.side_bar()
        utils.scroll_to_element_by_pixel(side_bar)
        time.sleep(1)
        changepassword_page = dashboard_page.click_change_password_menu()
        changepassword_page.current_password().send_keys(current_password)
        changepassword_page.new_password().send_keys(new_password)
        changepassword_page.confirm_password().send_keys(new_password)
        changepassword_page.submit_button().click()
        dashboard_page = changepassword_page.click_dashboard()
        side_barr = dashboard_page.side_bar2()
        utils.scroll_to_element_by_pixel(side_barr)
        login_page = dashboard_page.log_out()
        utils.delete_cookie()
        login_page.goto_url()


# @pytest.mark.usefixtures("setup")
# class TestLogin1:
#     @pytest.mark.parametrize("merch_user, merch_pass, admn_user, admn_pass, current_password, new_password, "
#                              "wrong_confirm, merch_name, category, service, provider", read_data())
#     def test_login_admin(self, setup, merch_user, merch_pass, admn_user, admn_pass, current_password, new_password,
#                          wrong_confirm, merch_name, category, service, provider):
#         driver = setup
#         self.driver = driver
#         utils = BaseUtils(self.driver)
#         title = self.driver.title
#         exp_title = "Creditswitch Merchant Portal | Login"
#         if title == exp_title:
#             pass
#         else:
#             utils.get_screenshot("wrong_site")
#             print("invalid title")
#         assert "Creditswitch" in title
#         login = LoginPage(self.driver)
#         login.username_field().send_keys(admn_user)
#         login.password_field().send_keys(admn_pass)
#         # self.driver.find_element(By.XPATH, readconfig("login_page", "userbox")).send_keys(admn_user)
#         # self.driver.find_element(By.XPATH, readconfig("login_page", "passbox")).send_keys(admn_pass)
#         time.sleep(3)  # delay to manually check recaptcha
#         login.login_button()
#         # self.driver.find_element(By.XPATH, readconfig("login_page", "login")).click()
#         try:
#             self.driver.find_element(By.XPATH, readconfig("dashboard_page", "service_setting")).click()
#         except NoSuchElementException as e:
#             print(f"Test failed: Element not found - {e}")
#             utils.get_screenshot("login_error_No_element")
#             utils.quit()
#             sys.exit(1)
#         except Exception as e:  # Catch any other unexpected errors
#             print(f"An unexpected error occurred: {e}")
#             utils.get_screenshot("login_error_exception")
#             utils.quit()
#             sys.exit(1)
#
#         # dashboard_page - side_bar, change_password_menu, service_setting, side_bar2 , logout settings_label
#         # select_merchant, search_merchant, merchant_list
#         service_setting_header = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "settings_label"))
#         service_setting_pageheader = service_setting_header.text
#         assert "Switching Module" in service_setting_pageheader
#         utils.double_click(self.driver.find_element(By.XPATH, readconfig("service_settings_page", "select_merchant")))
#         self.driver.find_element(By.XPATH, readconfig("service_settings_page", "search_merchant")).send_keys(merch_name)
#         self.driver.find_element(By.XPATH, readconfig("service_settings_page", "select_fetched_text")).click()
#         utils.double_click(self.driver.find_element(By.XPATH, readconfig("service_settings_page", "select_category")))
#         cate_list = self.driver.find_elements(By.XPATH, readconfig("service_settings_page", "category_list"))
#         print("category list length is: ", len(cate_list))
#         for cate in cate_list:  # service_settings, merchant_name, fetched_list,
#             cate_text = cate.text
#             if cate_text == category:
#                 cate.click()
#                 time.sleep(1)
#                 break
#         # select_service,service_list,
#         time.sleep(1)
#         utils.double_click(self.driver.find_element(By.XPATH, readconfig("service_settings_page", "select_service")))
#         serv_list = self.driver.find_elements(By.XPATH, readconfig("service_settings_page", "service_list"))
#         print("service list length is: ", len(serv_list))
#         for serv in serv_list:
#             serv_text = serv.text
#             if serv_text == service:
#                 serv.click()
#                 time.sleep(1)
#                 break
#         # select_provider, search_provider, provider_list, submit_button, SHAGO
#         service_setting_header.click()
#         time.sleep(1)
#         utils.double_click(self.driver.find_element(By.XPATH, readconfig("service_settings_page", "select_provider")))
#         prov_list = self.driver.find_elements(By.XPATH, readconfig("service_settings_page", "provider_list"))
#         print("provider list length is: ", len(prov_list))
#         for prov in prov_list:
#             prov_text = prov.text
#             if prov_text == provider:
#                 prov.click()
#                 break
#         self.driver.find_element(By.XPATH, readconfig("service_settings_page", "submit_button")).click()
#         time.sleep(2)
#         self.driver.find_element(By.XPATH, readconfig("service_settings_page", "dashboard"))
#         # side_menu = self.driver.find_elements(By.XPATH, "(//ul[@class='kt-menu__nav'])[1]/li")
#         # print("length is: ", len(side_menu))
#         # for i, menu in enumerate(side_menu):
#         #     try:
#         #         self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", side_menu)
#         #         time.sleep(3)
#         #         menu_text = menu.text
#         #         print(f"Menu {i + 1}: {menu_text}")
#         #         if menu_text == "Change Password":
#         #             menu.click()
#         #             break
#         #     except Exception as e:
#         #         print(f"Error with menu item {i + 1}: {e}")
#         #         continue
#
#         # for menu in side_menu:
#         #     print(menu.text)
#         #     if menu.text == "Change Password":
#         #         menu.click()
#         #         break
#         side_bar = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "side_bar"))
#         utils.scroll_to_element_by_pixel(side_bar)
#         time.sleep(2)
#         cpwd = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "change_password_menu"))
#         cpwd.click()
#         # [Change_pwd_page], current_password, new_password, confirm_new_password, submit_button
#         self.driver.find_element(By.XPATH, readconfig("Change_pwd_page", "current_password")).send_keys(current_password)
#         self.driver.find_element(By.XPATH, readconfig("Change_pwd_page", "new_password")).send_keys(new_password)
#         self.driver.find_element(By.XPATH, readconfig("Change_pwd_page", "confirm_new_password")).send_keys(new_password)
#         self.driver.find_element(By.XPATH, readconfig("Change_pwd_page", "submit_button")).click()
#         try:
#             error_locator = (By.XPATH, readconfig("Change_pwd_page", "error"))
#             error = utils.wait_until_present(error_locator)
#             print(f"Error Message is: {error}")
#         except NoSuchElementException as e:
#             print(f"Test failed: Element not found - {e}")
#             utils.get_screenshot("login_error_No_element")
#             utils.quit()
#             sys.exit(1)
#         except Exception as e:  # Catch any other unexpected errors
#             print(f"An unexpected error occurred: {e}")
#             utils.get_screenshot("login_error_exception")
#             utils.quit()
#             sys.exit(1)
#
#         self.driver.find_element(By.XPATH, readconfig("dashboard_page", "dashboard")).click()
#         side_barr = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "side_bar2"))
#         utils.scroll_to_element_by_pixel(side_barr)
#         logout = self.driver.find_element(By.XPATH, readconfig("dashboard_page", "logout"))
#         logout.click()
#         utils.delete_cookie()
#         self.driver.get(readconfig("setup", "url"))


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

