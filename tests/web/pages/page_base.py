from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

class PageBase:

    def __init__(self, driver):
        self.app_wait_timeout = 30
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.app_wait_timeout, ignored_exceptions=[StaleElementReferenceException])

    @property
    def element(self):
        return self.elements