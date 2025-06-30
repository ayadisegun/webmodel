import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from POM.login_page import Homepage
from Utilities.baseClass import Baseclass, HomepageData


# @pytest.mark.usefixtures("setup")
class Testformpage(Baseclass):
    def test_formdetails(self, getdataset):
        homep = Homepage(self.driver)
        homep.getname().send_keys(getdataset["firstname"])
        homep.getemail().send_keys(getdataset["email"])
        homep.getpword().send_keys(getdataset["password"])
        self.selectoptionbytext(homep.getgender(), getdataset["gender"])
        homep.submit().click()
        msgtxt = homep.getmsg().text

        log = self.get_logger()
        if msgtxt == "Success! The Form has been successfully!.":
            log.info("submission is successful")
        else:
            log.error("submission failed")

        assert "submitted successfully!" in msgtxt

        self.driver.refresh()

    # this fixture is created in order to pass data into the test dynamically, the first is a tuple () for passing data
    # and callign with index, while the second is dictionary{} to make data set called in pairs
    # @pytest.fixture(params=[("segun", "xyz@gmail.com", "password123", "Male"), ("Ade", "abc@gmail.com", "passwordfemale", "Female")])
    # @pytest.fixture(params=[{"firstname":"segun", "email":"xyz@gmail.com", "password":"password123", "gender":"Male"},{"firstname":"Ade", "email":"abc@gmail.com", "password":"passwordfemale", "gender":"Female"}])
    # def getdataset(self, request):
    #     return request.param

    # in order to be able to call the data's from another class, we move this dictionary to another class

    @pytest.fixture(params=HomepageData.homepagetestData)
    def getdataset(self, request):
        return request.param





