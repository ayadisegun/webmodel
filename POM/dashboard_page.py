from selenium.webdriver.common.by import By

from test_file.conftest import readconfig


class Dashboard:

    def __init__(self, driver):
        self.driver = driver

    serviceset = (By.XPATH, readconfig("dashboard_page", "service_setting"))
    sidebar = (By.XPATH, readconfig("dashboard_page", "side_bar"))
    changepasswrd = (By.XPATH, readconfig("dashboard_page", "change_password_menu"))
    sidebar2 = (By.XPATH, readconfig("dashboard_page", "side_bar2"))
    logout = (By.XPATH, readconfig("dashboard_page", "logout"))
    viewbalance = (By.XPATH, readconfig("dashboard_page", "view_balance"))
    airtimedata = (By.XPATH, readconfig("dashboard_page", "airtime_data"))
    serv_report = (By.XPATH, readconfig("dashboard_page", "service_report"))

    def side_bar(self):
        return self.driver.find_element(*Dashboard.sidebar)

    def servicereport_menu(self):
        return self.driver.find_element(*Dashboard.serv_report)

    def airtime_data_menu(self):
        self.driver.find_element(*Dashboard.airtimedata).click()
        from POM.airtimedata_page import AirtimeDataPage
        airtimeData = AirtimeDataPage(self.driver)
        return airtimeData

    def view_balance(self):
        hi = self.driver.find_element(*Dashboard.viewbalance)
        return hi

    def side_bar2(self):
        return self.driver.find_element(*Dashboard.sidebar2)

    def log_out(self):
        self.driver.find_element(*Dashboard.logout).click()
        from POM.login_page import LoginPage
        login = LoginPage(self.driver)
        return login

    def click_change_password_menu(self):
        self.driver.find_element(*Dashboard.changepasswrd).click()
        from POM.change_password_page import ChangePassword
        Chgpwdpage = ChangePassword(self.driver)
        return Chgpwdpage

    def service_setting(self):
        self.driver.find_element(*Dashboard.serviceset).click()
        from POM.service_settings_page import ServiceSetting
        service_settings = ServiceSetting(self.driver)
        return service_settings

