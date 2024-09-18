from tests.web.pages.page_base import PageBase
from tests.web.helpers.element import Element
from munch import munchify
from retry import retry
from assertpy import assert_that



class CalculatorPage(PageBase):
    def __init__(self, driver):
        PageBase.__init__(self, driver = driver)

        page_elements = {
            '1': Element('//button[@id="key-1"]', self),
            '2': Element('//button[@id="key-2"]', self),
            '3': Element('//button[@id="key-3"]', self),
            '4': Element('//button[@id="key-4"]', self),
            '5': Element('//button[@id="key-5"]', self),
            '6': Element('//button[@id="key-6"]', self),
            '7': Element('//button[@id="key-7"]', self),
            '8': Element('//button[@id="key-8"]', self),
            '9': Element('//button[@id="key-9"]', self),
            '0': Element('//button[@id="key-0"]', self),
            ',': Element('//button[@id="key-decimal"]', self),
            'clear_btn': Element('//button[@id="key-clear"]', self),
            'equals': Element('//button[@id="key-equals"]', self),
            'add': Element('//button[@id="key-add"]', self),
            'subtract': Element('//button[@id="key-subtract"]', self),
            'multiply': Element('//button[@id="key-multiply"]', self),
            'divide': Element('//button[@id="key-divide"]', self),
            'remote': Element('//button[@id="remote-toggle"]', self),
            'history_btn': Element('//button[@id="toggle-button"]', self),
            'logout': Element('//button[@id="logout-button"]', self),
            'screen':Element('//input[@id="calculator-screen"]' ,self),
            'username': Element('//label[@id="user-name"]', self),
            'history': Element('//textarea[@id="history"]', self)
        }
        self.elements = munchify(page_elements)

    def calculator(self,method,P1,P2,expected):  
        self.element.clear_btn.click() 
        getattr(self.element,str(P1)).click()
        getattr(self.element,method).click()
        getattr(self.element,str(P2)).click()
        self.element.equals.click() 
        P1 = int(P1)
        P2 = int(P2)
        if method == 'add':
            result = P1 + P2
        elif method == 'subtract':
            result = P1 - P2
        elif method == 'multiply':
            result = P1 * P2
        elif method == 'divide':
            if P2==0:
                result = 'undefined'
            else:
                result = P1 / P2

        print(f"Screen text: {self.element.screen.value}, Expected: {expected}")  
        return result  
        # assert self.element.screen.value == str(expected) 

    @retry(tries=15, delay=1)
    def get_username(self):
        username = self.elements.username.text  
        assert_that(username).is_not_empty()
        return username  