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

driver = None
@pytest.mark.usefixtures("setup")
@pytest.mark.parametrize("merch_user, merch_pass, admn_user, admn_pass, current_password, new_password, "
                             "wrong_confirm, merch_name, category, service, provider, start_date, end_date", read_data())
class TestAdminMerchLogin:
    # @pytest.mark.parametrize("merch_user, merch_pass, admn_user, admn_pass, current_password, new_password, "
    #                          "wrong_confirm, merch_name, category, service, provider, start_date, end_date", read_data())
    def test_login_admin(self, setup, get_logger, merch_user, merch_pass, admn_user, admn_pass, current_password, new_password,
                         wrong_confirm, merch_name, category, service, provider, start_date, end_date):
        global driver
        driver = setup
        self.driver = driver
        log = get_logger
        utils = BaseUtils(self.driver)
        title = self.driver.title
        exp_title = "Creditswitch Merchant Portal | Login"
        if title == exp_title:
            log.info("accurate website")
        else:
            utils.get_screenshot("wrong_site_admn")
            log.warning("invalid title")
        assert "Creditswitch" in title
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 1, 14, "Admn_Url_title")
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 2, 14, title)
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
            log.warning(f"Test failed: Element not found - {e}")
            utils.get_screenshot("login_error_No_element")
            utils.quit()
            sys.exit(1)
        except Exception as e:  # Catch any other unexpected errors
            log.warning(f"An unexpected error occurred: {e}")
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
        log.info("category list length is: ", len(cate_list))
        for cate in cate_list:
            cate_text = cate.text
            if cate_text == category:
                cate.click()
                time.sleep(1)
                break
        time.sleep(1)
        utils.double_click(servicesettings_page.click_service())
        serv_list = servicesettings_page.search_service()
        log.info("service list length is: ", len(serv_list))
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
        log.info("provider list length is: ", len(prov_list))
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

    @pytest.mark.new
    def test_login_merch(self, setup, get_logger, merch_user, merch_pass, admn_user, admn_pass, current_password, new_password,
                         wrong_confirm, merch_name, category, service, provider, start_date, end_date):
        log = get_logger
        utils = BaseUtils(self.driver)
        self.driver.get(readconfig("setup", "merch_url"))
        title = self.driver.title
        exp_title = "Creditswitch Merchant Portal | Login"
        if title == exp_title:
            log.info("correct title")
        else:
            utils.get_screenshot("wrong_site_merch")
            log.warning("invalid title")
        assert "Creditswitch" in title
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 1, 15, "Merch_Url_title")
        set_data((readconfig("data", "file")), (readconfig("data", "sheet_name")), 2, 15, title)
        login_page = LoginPage(self.driver)
        login_page.username_field().send_keys(merch_user)
        login_page.password_field().send_keys(merch_pass)
        time.sleep(3)  # delay to manually check recaptcha
        try:
            login_page.login_button()
        except NoSuchElementException as e:
            log.warning(f"Test failed: Element not found - {e}")
            utils.get_screenshot("login_error_No_element")
            utils.quit()
            sys.exit(1)
        except Exception as e:  # Catch any other unexpected errors
            log.warning(f"An unexpected error occurred: {e}")
            utils.get_screenshot("login_error_exception")
            utils.quit()
            sys.exit(1)

    @pytest.mark.new
    def test_airtime_balance(self, setup, get_logger, merch_user, merch_pass, admn_user, admn_pass, current_password, new_password,
                         wrong_confirm, merch_name, category, service, provider, start_date, end_date):
        from POM.dashboard_page import Dashboard
        log = get_logger
        log.info("airtime balance test running")
        utils = BaseUtils(self.driver)
        dashboard_page = Dashboard(self.driver)
        dashboard_page.view_balance().click()
        dashboard_page.servicereport_menu().click()
        airtimedata_page = dashboard_page.airtime_data_menu()
        airtimedata_page.start_datetext().click()
        airtimedata_page.start_datetext().send_keys(start_date)
        airtimedata_page.end_datetext().click()
        airtimedata_page.end_datetext().send_keys(end_date)
        airtimedata_page.search_button().click()
        utils.scroll_down()
        utils.double_click(airtimedata_page.generate_report())
        airtimedata_page.report_csv().click()
        side_bar = airtimedata_page.side_bar()
        utils.scroll_to_element_by_pixel(side_bar)
        airtimedata_page.log_out()

