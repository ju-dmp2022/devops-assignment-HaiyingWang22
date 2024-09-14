from BE.calculator_helper import CalculatorHelper
from assertpy import assert_that
import pytest

class BaseTest():
    def setup_method(self):
        #Arrange
        self.calculator = CalculatorHelper()

    def teardown_method(self):
        pass

    def execute_test(self, method_name, a, b, expected):
        # Dynamic get methods form CalculatorHelper
        method = getattr(self.calculator, method_name)
        
        # Action
        value = method(a, b)
        # Assert
        assert_that(value).is_equal_to(expected)

class TestCalculator(BaseTest):
    # test add
    @pytest.mark.parametrize("a, b, expected", [
            (3, 3, 6),       # 3 + 3 = 6
            (3, -3, 0),      # 3 + (-3) = 0
            (-1, -1, -2),    # -1 + (-1) = -2
            (0, 0, 0),       # 0 + 0 = 0
        ])
    def test_add(self,a, b, expected):
        self.execute_test("add", a, b, expected)


    # test subtract
    @pytest.mark.parametrize("a, b, expected", [
            (3, 2, 1),       # 3 - 2 = 1
            (3, -3, 6),      # 3 - (-3) = 6
            (-1, -1, 0),    # -1 - (-1) = 0
            (0, 0, 0),       # 0 - 0 = 0
        ])
    def test_subtract(self,a, b, expected):   
        self.execute_test("subtract", a, b, expected) 
        

    # test multiply
    @pytest.mark.parametrize("a, b, expected", [
            (3, 2, 6),       # 3 * 2 = 6
            (3, -3, -9),      # 3 * (-3) = -9
            (-1, -1, 1),    # -1 * (-1) = 1
            (0, 0, 0),       # 0 * 0 = 0
        ])
    def test_multiply(self,a, b, expected): 
        self.execute_test("multiply", a, b, expected) 
        

    # test divide
    @pytest.mark.parametrize("a, b, expected", [
            (4, 2, 2),       # 4 / 2 = 6
            (3, -3, -1),      # 3 / (-3) = -1
            (-1, -1, 1),    # -1 / (-1) = 1
        ])
    def test_divide(self,a, b, expected): 
        self.execute_test("divide", a, b, expected)

        # test devide by 0
        with pytest.raises(ZeroDivisionError, match="division by zero"):
            value = self.calculator.divide(10, 0)

    # test_register_user
    def test_register_user(self):

        # test exist user
        self.calculator._user_list = [self.calculator.User("existing_user", "password")]

        result = self.calculator.register_user("existing_user", "password")

        assert result == None

        # test new user
        self.calculator._user_list = []
        
        result = self.calculator.register_user("new_username", "secure_password")
        username = self.calculator._user_list[0].username
        password = self.calculator._user_list[0].password
        length = len(self.calculator._user_list)

        assert result == "new_username"
        assert username == "new_username"
        assert password == "secure_password"
        assert length == 1
        

    # test_login
    @pytest.mark.parametrize("username, password, expected", [
            ("existing_user", "password","existing_user"), 
            ("uncharted_user", "password",None)  
        ])
    def test_login(self,username, password, expected):

        calculator = CalculatorHelper()
        self.calculator._user_list = [self.calculator.User("existing_user", "password")]
        result = self.calculator.login(username, password)

        assert result == expected

    # test_get_current_user
    @pytest.mark.parametrize("username, password, expected", [
            ("existing_user", "password","existing_user"), 
            (None, None, None)  
        ])
    def test_get_current_user(self,username, password, expected):

        self.calculator._current_user = self.calculator.User(username, password) 
        result = self.calculator.get_current_user()

        assert result.username == expected

    #test_logout 
    def test_logout(self):

        self.calculator._current_user = self.calculator.User("test_user","password123") 
        result = self.calculator.logout()

        assert result.username == "test_user"
        assert self.calculator._current_user is None    
    



        

        
    



