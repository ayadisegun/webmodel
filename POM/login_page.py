from selenium.webdriver.common.by import By

from test_file.conftest import readconfig


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    # , password_field, login_button
    UN_field = (By.XPATH, readconfig("login_page", "userbox"))
    PW_field = (By.XPATH, readconfig("login_page", "passbox"))
    log_but = (By.XPATH, readconfig("login_page", "login"))

    def goto_url(self):
        return self.driver.get(readconfig("setup", "url"))

    def username_field(self):
        return self.driver.find_element(*LoginPage.UN_field)

    def password_field(self):
        return self.driver.find_element(*LoginPage.PW_field)

    def login_button(self):
        self.driver.find_element(*LoginPage.log_but).click()  # the * is to de-serialise the shop variable in a python
        from POM.dashboard_page import Dashboard
        dashboard = Dashboard(self.driver)
        return dashboard

