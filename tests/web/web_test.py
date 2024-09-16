import pytest
from assertpy import assert_that
from tests.web.test_base import WebBase
from tests.web.pages.login_page import LoginPage
from tests.web.pages.register_page import RegisterPage
from tests.web.pages.calculator_page import CalculatorPage
import time

class TestWeb(WebBase):
    def test_login(self):
        LoginPage(self.driver).login('admin','test1234')
        assert CalculatorPage(self.driver).elements.username.text == 'admin'
        CalculatorPage(self.driver).elements.logout.click()   

    def test_register_newuser(self):
        userName='testUser'
        password='test12345'
        loginPage=LoginPage(self.driver)
        registerPage=RegisterPage(self.driver)
        calculator_page = CalculatorPage(self.driver)
        
        # register new user
        loginPage.elements.register_btn.click()   
        registerPage.register(userName,password) 
        current_url = self.driver.current_url
        print(f"current URL is:{current_url}")
        if current_url=='http://host.docker.internal:8080/index.html':
            time.sleep(10)
            assert calculator_page.elements.username.text == userName
            calculator_page.elements.logout.click()  

        # login the user 
        LoginPage(self.driver).login(userName,password)
        assert calculator_page.elements.username.text == userName

        
    #     loginPage.elements.register_btn.click()   
    #     registerPage.register(userName,password) 
    #     if registerPage.element.message.text == 'User already exists!': 
    #         # self.driver.get("http://localhost:8080/login.html")
    #         self.driver.get("http://host.docker.internal:8080/login.html") 
    #         LoginPage(self.driver).login(userName,password)
    #         assert calculator_page.elements.username.text == userName 
    #     else:
    #         time.sleep(5)
    #         assert calculator_page.elements.username.text == userName

        # Perform calculations
        calculator_page.calculator('add', 1, 2)  
        calculator_page.calculator('subtract', 3, 2)  
        calculator_page.calculator('multiply', 2, 2)  
        # calculator_page.calculator('divide', 4, 0)  
        
        # Check history 
        calculator_page.elements.history_btn.click()
        expressions = calculator_page.element.history.value.split("\n")
        print(f"history text: {expressions}") 
        for expression in expressions:
            if "=" in expression:
                formula, result = expression.split("=")
                if "+" in formula:
                    P1, P2 = formula.split("+")
                    calculator_page.calculator('add', P1, P2)  
                if "-" in formula:
                    P1, P2 = formula.split("-")
                    calculator_page.calculator('subtract', P1, P2)     
                if "*" in formula:
                    P1, P2 = formula.split("*")
                    calculator_page.calculator('multiply', P1, P2)  
                if "/" in formula:
                    P1, P2 = formula.split("/")
                    calculator_page.calculator('divide', P1, P2)   

        calculator_page.elements.logout.click()  
