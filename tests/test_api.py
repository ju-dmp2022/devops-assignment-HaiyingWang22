import requests
from calculator_client.client import Client
from calculator_client.api.actions import calculate
from calculator_client.api.actions import register
from calculator_client.api.actions import users_current
from calculator_client.models.calculation import Calculation
from calculator_client.models.opertions import Opertions
from calculator_client.models.user import User
from calculator_client.models.error_response import ErrorResponse
from calculator_client.models import ResultResponse
from calculator_client.models import UserResponse

class BaseTest():
    def setup_method(self):
        #Arrange
        self.BASE_URL = "http://0.0.0.0:5001"

    def teardown_method(self):
        pass


class TestCalculatorAPI(BaseTest):
    def test_culculate_add(self):
        params = {
            "operation": "add",
            "operand1": 3,
            "operand2": 3
        }
        response = requests.post(f"{self.BASE_URL}/calculate", json=params)
        assert response.status_code == 200
        json_data = response.json()
        expected_result = {'result': 6}
        assert json_data == expected_result

    #POST test 
    # test_add
    def test_generated_code_test_add(self):
        response = calculate.sync(client=Client(self.BASE_URL), 
                                  body=Calculation(Opertions.ADD, operand1=3,operand2=3 ))  
        assert isinstance(response, ResultResponse)
        assert response.result == 6  

    # test_divide
    def test_generated_code_test_divide(self):
        response = calculate.sync(client=Client(self.BASE_URL), 
                                  body=Calculation(Opertions.DIVIDE, operand1=3,operand2=0 ))  
        assert isinstance(response, ErrorResponse)
        assert response.detail == "float division by zero"

    # test_register
    def test_generated_code_test_register(self):
        response = register.sync(client=Client(self.BASE_URL), 
                                  body=User(username = "abc", password="123" ))  
        if isinstance(response, ErrorResponse):
            assert response.detail == "User already exists."
        else:
            assert isinstance(response, UserResponse)
            assert response.username == "abc"

    #GET test 
    def test_generated_code_test_current_user(self):
        client = Client(self.BASE_URL)
        response = users_current.sync(client=client) 
        detailed_response = users_current.sync_detailed(client=client)
        assert detailed_response.status_code == 204
        assert detailed_response.parsed is None

        