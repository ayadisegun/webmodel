import inspect
import logging
import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.chrome.options import Options
from configparser import ConfigParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import openpyxl

# from Utilities.baseClass import setup


# def pytest_addoption(parser):
#     parser.addoption(
#         "--browser_name", action="store", default="chrome"
#     )


@pytest.fixture(scope="class")
def setup(request):
    preferences = {"download.default_directory": (readconfig("setup", "download_directory"))}  # --> create a variable for the current working
    # directory dowload location, Note --> preferences={"download.default_directory": "C:\user/segun/downloads"}
    # will download the file in any hardcoded path defined.
    ops = webdriver.ChromeOptions()  # ops = webdriver.EdgeOptions()
    # ops.add_argument("headless") # to run driver in headless mode
    ops.add_argument("--ignore-certificate-errors")
    ops.add_argument("--start-maximized")
    ops.add_argument("--disable-notification")
    # ops.add_argument("--incognito")  # to open in incognito mode
    ops.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(options=ops)  # driver = webdriver.Chrome(service=serv_obj, options=ops)
    driver.implicitly_wait(10)
    # browser_name = request.config.getoption("browser_name")
    # if browser_name == "chrome":
    #     preferences = {"download.default_directory": "location"}  # --> create a variable for the current working
    #     # directory dowload location, Note --> preferences={"download.default_directory": "C:\user/segun/downloads"}
    #     # will download the file in any hardcoded path defined.
    #     ops = webdriver.ChromeOptions()  # ops = webdriver.EdgeOptions()
    #     # ops.add_argument("headless") # to run driver in headless mode
    #     ops.add_argument("--ignore-certificate-errors")
    #     # ops.add_argument("--start-maximized")
    #     ops.add_argument("--disable-notification")
    #     ops.add_experimental_option("prefs", preferences)
    #     # driver = webdriver.Chrome(service=serv_obj, options=ops)
    #     driver = webdriver.Chrome(options=ops)
    # elif browser_name == "edge":
    #     preferences = {"download.default_directory": "location"}  # --> create a variable for the current working
    #     # directory dowload location, Note --> preferences={"download.default_directory": "C:\user/segun/downloads"}
    #     # will download the file in any hardcoded path defined.
    #     ops = webdriver.EdgeOptions()  # ops = webdriver.ChromeOptions()
    #     # ops.add_argument("headless") # to run driver in headless mode
    #     ops.add_argument("--ignore-certificate-errors")
    #     ops.add_argument("--start-maximized")
    #     ops.add_argument("--disable-notification")
    #     ops.add_experimental_option("prefs", preferences)
    #     driver = webdriver.Edge(options=ops)  # webdriver.Chrome(options=ops)
    # driver.get("http://176.58.99.160:2025/admn93i")
    driver.get(readconfig("setup", "url"))
    request.cls.driver = driver

    yield driver
    driver.close()
    driver.quit()


@pytest.mark.usefixtures("setup")
class Utils:
    def __init__(self, driver):
        self.driver = driver

    def selectoption_bytext(self, locator, text):
        optns = Select(self.locator)
        optns.select_by_visible_text(text)

    # @staticmethod
    class loggersclass:
        def get_logger(self):
            loggerName = inspect.stack()[1][3]  # this script helps to ensure that the testcase name is printed in the log
            # even when the logger is being called from a base class
            logger = logging.getLogger(loggerName)
            filehandler = logging.FileHandler('logsbase1.log')
            formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
            filehandler.setFormatter(formatter)
            logger.addHandler(filehandler)
            logger.setLevel(logging.ERROR)
            # logger.debug("A debug statement written here will be printer")
            # logger.info("information statenment will be printed")
            # logger.warning("Warning messages")
            # logger.error("A major error has happened")
            # logger.critical("Critical issues")
            logger.error("")
            logger.critical("")
            return logger


def readconfig(section, key):
    # script for reading data from config.ini for test data
    config = ConfigParser()
    config.read("config.ini")
    return config.get(section, key)


def send_mail(sender_address, sender_pass, receiver_address, subject, mail_content, attach_file_name,
              ):
    # sender_pass = 'Selenium@234'

    # setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject

    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    message.attach(payload)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


# @pytest.fixture(scope="session")
def read_data():
    file_path = readconfig("data", "file")
    sheet_name = readconfig("data", "sheet_name")
    print(f"Attempting to open file: '{file_path}'")
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
    except FileNotFoundError:
        pytest.fail(f"Excel file not found: {file_path}")
    except KeyError:
        pytest.fail(f"Sheet '{sheet_name}' not found in the Excel file")

    max_row = sheet.max_row
    max_col = sheet.max_column

    # Get headers from first row
    headers = [sheet.cell(row=1, column=col).value for col in range(1, max_col + 1)]
    print("headers are: ", headers)

    data_rows = []
    for row in range(2, max_row + 1):
        row_data = [sheet.cell(row=row, column=col).value for col in range(1, max_col + 1)]
        data_rows.append(tuple(row_data))
    print(data_rows)
    return data_rows


def get_Excel_data_path_in_script():
        # return [
        #
        #     ["segun", "Ayadi", "Rapture", "segema@gmail", "Testing1", "techsupport@creditswitch.com", "Testing2."],
        #     ["taye", "taiwo", "tailoo", "taiwo@gmail", "Testing4", "ayadisegun02@gmail.com", "Credit2."],
        #
        # ]
        excelfile = "C:\\Users\\Segun\\PycharmProjects\\Android931\\testScripts\\ExcelFile.xlsx"
        sheetName = "details"
        workbook = openpyxl.load_workbook(excelfile)
        sheet = workbook[sheetName]
        totalrows = sheet.max_row
        totalcols = sheet.max_column
        mainList = []

        for i in range(2, totalrows + 1):
            dataList = []
            for j in range(1, totalcols + 1):
                data = sheet.cell(row=i, column=j).value
                dataList.insert(j, data)
            mainList.insert(i, dataList)
        return mainList


def set_data(file_path, sheet_name, rowNum, colNum, data):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]
        sheet.cell(row=rowNum, column=colNum).value = data
        workbook.save(file_path)

# @pytest.fixture(scope="session")
def loggings():
    logger = logging.getLogger(__name__)
    filehandler = logging.FileHandler('e2elogfile.log')
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.setLevel(logging.INFO)
    logger.debug("A debug statement written here will be printer")
    logger.info("information statenment will be printed")
    logger.warning("Warning messages")
    logger.error("A major error has happened")
    logger.critical("Critical issues")


# class loggersclass:
#     def get_logger(self):
#         loggerName = inspect.stack()[1][3] # this script helps to ensure that the testcase name is printed in the log
#         # even when the logger is being called from a base class
#         logger = logging.getLogger(loggerName)
#         filehandler = logging.FileHandler('logsbase1.log')
#         formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
#         filehandler.setFormatter(formatter)
#         logger.addHandler(filehandler)
#         logger.setLevel(logging.ERROR)
#         # logger.debug("A debug statement written here will be printer")
#         # logger.info("information statenment will be printed")
#         # logger.warning("Warning messages")
#         # logger.error("A major error has happened")
#         # logger.critical("Critical issues")
#         logger.error("")
#         logger.critical("")
#         return logger


# @pytest.mark.hookwrapper
# to automatically generate a screenshot when a test fails, we need to write a one-time script as follows
# def pytest_runtest_makereport(item):
#     """
#         Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#         :param item:
#         """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#
#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             _capture_screenshot(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra
#
#
# def _capture_screenshot(self, setup, name):
#     driver = setup
#     screenshot_data = self.driver.get_screenshot_as_png()
#     with open(f"{name}.png", "wb") as file:
#         file.write(screenshot_data)

