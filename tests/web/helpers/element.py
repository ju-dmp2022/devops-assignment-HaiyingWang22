from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Element:

    def __init__(self, locator, page):
        self.page = page
        self.locator = locator

    def find(self):
        self.page.wait.until(EC.presence_of_element_located((By.XPATH, self.locator)))
        return self

    def click(self):
        self.page.wait.until(EC.element_to_be_clickable((By.XPATH, self.locator))).click()
        return self

    def set(self, value):
        element = self.page.wait.until(EC.element_to_be_clickable((By.XPATH, self.locator)))
        element.clear()
        element.send_keys(value)
        return self

    @property
    def text(self):
        return self.page.wait.until(EC.presence_of_element_located((By.XPATH, self.locator))).text

    @property
    def value(self):
        return self.page.wait.until(EC.presence_of_element_located((By.XPATH, self.locator))).get_attribute('value')