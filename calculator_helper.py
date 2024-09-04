import logger

class CalculatorHelper():
    log_properties = {
        'custom_dimensions': {
            'userId': 'haiying_wang'
        }
    }

    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CalculatorHelper, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self._user_list = []
            self._current_user = None
            admin = self.User('admin','test1234')
            self._user_list.append(admin)
            self._is_initialized = True
            self.logger = logger.get_logger(__name__)

    class User():
        def __init__(self, username, password):
            self.username = username
            self.password = password

        def __repr__(self):
            return f"User(username={self.username}, password={self.password})"

    def add(self, a, b):
        result = a + b
        self.logger.debug(f"Adding {a} and {b}", extra=self.log_properties)
        self.logger.info(f"Result of {result}", extra=self.log_properties)
        return result

    def subtract(self, a, b):
        result = a - b
        self.logger.debug(f"subtract {a} and {b}", extra=self.log_properties)
        self.logger.info(f"Result of {result}", extra=self.log_properties)
        return result

    def multiply(self, a, b):
        result = a * b
        self.logger.debug(f"multiply {a} and {b}", extra=self.log_properties)
        self.logger.info(f"Result of {result}", extra=self.log_properties)
        return result

    def divide(self, a, b):
        result = a / b
        self.logger.debug(f"divide {a} and {b}", extra=self.log_properties)
        self.logger.info(f"Result of {result}", extra=self.log_properties)
        return result

    def register_user(self, username, password):
        self.logger.debug(f"Try to registing user: {username}", extra=self.log_properties)
        for user in self._user_list:
            if(user.username == username):
                self.logger.warning(f"User: {username} already exist", extra=self.log_properties)
                return None
        user = self.User(username, password)
        self._user_list.append(user)
        self.logger.info(f"User: {username} are registed success", extra=self.log_properties)
        return username
    

    def login(self, username, password):
        self.logger.debug(f"Try to login user: {username}", extra=self.log_properties)
        for user in self._user_list:
            if(user.username == username and user.password == password):
                self._current_user = user
                self.logger.info(f"User {username} logged in successfully", extra=self.log_properties)
                return username
        self.logger.warning(f"Login failed: Invalid credentials for user {username}", extra=self.log_properties)    
        return None

    def logout(self):
        user = self._current_user
        self._current_user = None
        self.logger.info(f"User {user.username} logged out successfully", extra=self.log_properties)
        return user

    def get_current_user(self):
        user = self._current_user
        self.logger.info(f"Current user is {user.username}", extra=self.log_properties)
        return self._current_user
