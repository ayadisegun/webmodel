from selenium.webdriver.common.by import By

from test_file.conftest import readconfig


class AirtimeDataPage:

    def __init__(self, driver):
        self.driver = driver

    sidebar = (By.XPATH, readconfig("airtimedata_page", "side_bar"))
    startdate = (By.XPATH, readconfig("airtimedata_page", "startdate_field"))
    enddate = (By.XPATH, readconfig("airtimedata_page", "enddate_field"))
    searchbut = (By.XPATH, readconfig("airtimedata_page", "search"))
    genrep = (By.XPATH, readconfig("airtimedata_page", "gen_rep"))
    gencsv = (By.XPATH, readconfig("airtimedata_page", "get_csv"))
    logout = (By.XPATH, readconfig("airtimedata_page", "logout"))


    def side_bar(self):
        return self.driver.find_element(*AirtimeDataPage.sidebar)

    def start_datetext(self):
        return self.driver.find_element(*AirtimeDataPage.startdate)

    def generate_report(self):
        return self.driver.find_element(*AirtimeDataPage.genrep)

    def report_csv(self):
        return self.driver.find_element(*AirtimeDataPage.gencsv)

    def end_datetext(self):
        return self.driver.find_element(*AirtimeDataPage.enddate)

    def search_button(self):
        return self.driver.find_element(*AirtimeDataPage.searchbut)

    def log_out(self):
        self.driver.find_element(*AirtimeDataPage.logout).click()
        from POM.login_page import LoginPage
        login = LoginPage(self.driver)
        return login