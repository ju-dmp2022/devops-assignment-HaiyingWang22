import pytest
from assertpy import assert_that
from tests.web.test_base import WebBase
from tests.web.pages.login_page import LoginPage
from tests.web.pages.register_page import RegisterPage
from tests.web.pages.calculator_page import CalculatorPage
import random
from retry import retry

class TestWeb(WebBase):
    def setup_method(self):
        super().setup_method()
        self.userName = f'User{random.randint(1, 9999)}'
        self.password = 'test12345'
        self.adminName ='admin'
        self.adminPassword = 'test1234'
        self.loginPage=LoginPage(self.driver)
        self.registerPage=RegisterPage(self.driver)
        self.calculator_page = CalculatorPage(self.driver)

    def test_login_admin(self):
        LoginPage(self.driver).login(self.adminName,self.adminPassword)
        assert self.calculator_page.elements.username.text == self.adminName
        self.calculator_page.elements.logout.click()   

    # 2.1 Register a new user
    def test_register_newuser(self):
        self.loginPage.elements.register_btn.click()   
        self.registerPage.register(self.userName,self.password) 
        current_url = self.driver.current_url
        print(f"current URL is:{current_url}")
        if current_url=='http://host.docker.internal:8080/index.html':
            # use retry method to deal with delayed loading of elements
            assert_that(self.calculator_page.get_username()).is_equal_to(self.userName)
            self.calculator_page.elements.logout.click()  
        else:
            print(f"user already exist") 
                
        # login the user 
        LoginPage(self.driver).login(self.userName,self.password)
        assert self.calculator_page.elements.username.text == self.userName
        self.calculator_page.elements.logout.click()  

        

    # 2.2 Verify the calculation methods
    @pytest.mark.parametrize("method,P1,P2, expected", [
        ("add",1, 1, 2), 
        ("subtract",2, 1, 1), 
        ("multiply",2, 3, 6), 
        ("divide",4, 1, 4),
        ("divide",4, 0, "undefined")
    ])
    def test_calculation(self,method,P1,P2, expected):
        LoginPage(self.driver).login(self.adminName,self.adminPassword)
        assert self.calculator_page.elements.username.text == self.adminName
        self.calculator_page.calculator(method,P1,P2, expected)  
        assert_that(self.calculator_page.calculator(method,P1,P2,expected)).is_equal_to(expected)
        self.calculator_page.elements.logout.click()  


    # 2.3 Verify the history feature
    @pytest.mark.parametrize("method,P1,P2, expected", [
        ("add",1, 1, 2), 
        # ("subtract",2, 1, 1), 
        # ("multiply",2, 3, 6), 
        # ("divide",4, 1, 4),
        # ("divide",4, 0, "undefined")
    ])
    def test_history(self,method,P1,P2, expected):
        LoginPage(self.driver).login(self.adminName,self.adminPassword)
        assert self.calculator_page.elements.username.text == self.adminName
        self.calculator_page.calculator(method,P1,P2, expected)  
        assert_that(self.calculator_page.calculator(method,P1,P2,expected)).is_equal_to(expected)
        self.calculator_page.elements.history_btn.click()
        expressions = self.calculator_page.element.history.value.split("\n")
        print(f"history text: {expressions}") 
        for expression in expressions:
            if "=" in expression:
                formula, result = expression.split("=")
                if "+" in formula:
                    P1, P2 = formula.split("+")
                    self.calculator_page.calculator('add', P1, P2, result)  
                if "-" in formula:
                    P1, P2 = formula.split("-")
                    self.calculator_page.calculator('subtract', P1, P2, result)     
                if "*" in formula:
                    P1, P2 = formula.split("*")
                    self.calculator_page.calculator('multiply', P1, P2, result)  
                if "/" in formula:
                    P1, P2 = formula.split("/")
                    self.calculator_page.calculator('divide', P1, P2, result)   

        self.calculator_page.elements.logout.click()  

    