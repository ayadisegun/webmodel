from selenium.webdriver.common.by import By

from test_file.conftest import readconfig


class ServiceSetting:

    def __init__(self, driver):
        self.driver = driver

    serviceset = (By.XPATH, readconfig("dashboard_page", "service_setting"))
    header = (By.XPATH, readconfig("dashboard_page", "settings_label"))
    merchant = (By.XPATH, readconfig("service_settings_page", "select_merchant"))
    merchantsearch = (By.XPATH, readconfig("service_settings_page", "search_merchant"))
    fetchedmerchant = (By.XPATH, readconfig("service_settings_page", "select_fetched_text"))
    category = (By.XPATH, readconfig("service_settings_page", "select_category"))
    categorysearch = (By.XPATH, readconfig("service_settings_page", "category_list"))
    service = (By.XPATH, readconfig("service_settings_page", "select_service"))
    servicesearch = (By.XPATH, readconfig("service_settings_page", "service_list"))
    provider = (By.XPATH, readconfig("service_settings_page", "select_provider"))
    providersearch = (By.XPATH, readconfig("service_settings_page", "provider_list"))
    submitbut = (By.XPATH, readconfig("service_settings_page", "submit_button"))
    dashbd = (By.XPATH, readconfig("service_settings_page", "dashboard"))

    def set_service(self):
        return self.driver.find_element(*ServiceSetting.serviceset)

    def click_dashboard(self):
        self.driver.find_element(*ServiceSetting.dashbd).click()
        from POM.dashboard_page import Dashboard
        dashboard = Dashboard(self.driver)
        return dashboard

    def switchsubmit_button(self):
        return self.driver.find_element(*ServiceSetting.submitbut)

    def search_provider(self):
        return self.driver.find_elements(*ServiceSetting.providersearch)

    def click_provider(self):
        return self.driver.find_element(*ServiceSetting.provider)

    def search_service(self):
        return self.driver.find_elements(*ServiceSetting.servicesearch)

    def click_service(self):
        return self.driver.find_element(*ServiceSetting.service)

    def search_category(self):
        return self.driver.find_elements(*ServiceSetting.categorysearch)

    def click_category(self):
        return self.driver.find_element(*ServiceSetting.category)

    def servicesetting_header(self):
        service_setting_header = self.driver.find_element(*ServiceSetting.header)
        return service_setting_header

    def set_merchant(self):
        return self.driver.find_element(*ServiceSetting.merchant)

    def search_merchant(self):
        return self.driver.find_element(*ServiceSetting.merchantsearch)

    def selectfetched_merchant(self):
        return self.driver.find_element(*ServiceSetting.fetchedmerchant)

