from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class WebBase:

    @classmethod
    def setup_class(cls):
        """ Setup to run once
            Initiatiung some common parameters
        """
        cls.app_url = 'http://localhost:8080'

    def setup_method(self):
        """ Setup to run before every test
            Initiate a new driver.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = chrome_options)
        #self.driver = webdriver.Remote(command_executor = "http://localhost:4444", options=chrome_options)
        self.driver.set_window_size(1920,1080)
        self.driver.get(self.app_url)

    def teardown_method(self):
        """ Teardown to run after every test
            Stop the driver
        """
        self.driver.quit()