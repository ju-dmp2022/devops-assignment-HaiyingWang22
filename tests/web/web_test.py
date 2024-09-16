import pytest
from assertpy import assert_that
from tests.web.test_base import WebBase
from tests.web.pages.login_page import LoginPage
from tests.web.pages.register_page import RegisterPage
from tests.web.pages.calculator_page import CalculatorPage
import time

class TestWeb(WebBase):
    def setup_method(self, method):
        self.userName = 'testUser'
        self.password = 'test12345'
        self.loginPage = LoginPage(self.driver)
        self.registerPage = RegisterPage(self.driver)
        self.calculator_page = CalculatorPage(self.driver)

    def test_login(self):
        LoginPage(self.driver).login('admin','test1234')
        assert self.calculator_page.elements.username.text == 'admin'
        self.calculator_page.elements.logout.click()   

    def test_register_newuser(self):
        
        # register new user
        self.loginPage.elements.register_btn.click()   
        self.registerPage.register(self.userName,self.password) 
        current_url = self.driver.current_url
        print(f"current URL is:{current_url}")
        if current_url=='http://host.docker.internal:8080/index.html':
            time.sleep(10)
            assert self.calculator_page.elements.username.text == self.userName
            self.calculator_page.elements.logout.click()  

        # login the user 
        self.loginPage.login(self.userName,self.password)
        assert self.calculator_page.elements.username.text == self.userName

        # Perform calculations
        self.calculator_page.calculator('add', 1, 2)  
        self.calculator_page.calculator('subtract', 3, 2)  
        self.calculator_page.calculator('multiply', 2, 2)  
        self.calculator_page.calculator('divide', 4, 0)  
        
        # Check history 
        self.calculator_page.elements.history_btn.click()
        expressions = self.calculator_page.element.history.value.split("\n")
        print(f"history text: {expressions}") 
        for expression in expressions:
            if "=" in expression:
                formula, result = expression.split("=")
                if "+" in formula:
                    P1, P2 = formula.split("+")
                    self.calculator_page.calculator('add', P1, P2)  
                if "-" in formula:
                    P1, P2 = formula.split("-")
                    self.calculator_page.calculator('subtract', P1, P2)     
                if "*" in formula:
                    P1, P2 = formula.split("*")
                    self.calculator_page.calculator('multiply', P1, P2)  
                if "/" in formula:
                    P1, P2 = formula.split("/")
                    self.calculator_page.calculator('divide', P1, P2)   

        self.calculator_page.elements.logout.click()  
