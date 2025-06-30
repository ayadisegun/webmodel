from selenium.webdriver.common.by import By

from test_file.conftest import readconfig


class ChangePassword:

    def __init__(self, driver):
        self.driver = driver

    currentpassword = (By.XPATH, readconfig("Change_pwd_page", "current_password"))
    nwpasword = (By.XPATH, readconfig("Change_pwd_page", "new_password"))
    confpassword = (By.XPATH, readconfig("Change_pwd_page", "confirm_new_password"))
    submit = (By.XPATH, readconfig("Change_pwd_page", "submit_button"))
    error = (By.XPATH, readconfig("Change_pwd_page", "error"))
    dashbd = (By.XPATH, readconfig("service_settings_page", "dashboard"))

    def current_password(self):
        return self.driver.find_element(*ChangePassword.currentpassword)

    def error_field(self):
        return self.driver.find_element(*ChangePassword.error)

    def new_password(self):
        return self.driver.find_element(*ChangePassword.nwpasword)

    def confirm_password(self):
        return self.driver.find_element(*ChangePassword.confpassword)

    def submit_button(self):
        return self.driver.find_element(*ChangePassword.submit)

    def click_dashboard(self):
        self.driver.find_element(*ChangePassword.dashbd).click()
        from POM.dashboard_page import Dashboard
        dashboard = Dashboard(self.driver)
        return dashboard
