from tests.web.pages.page_base import PageBase
from tests.web.helpers.element import Element
from munch import munchify


class LoginPage(PageBase):
    def __init__(self, driver):
        PageBase.__init__(self, driver = driver)

        page_elements = {
            'username': Element('//input[@id="username"]', self),
            'password': Element('//input[@id="password"]', self),
            'login_btn': Element('//button[@id="login"]', self),
            'register_btn': Element('//button[@id="register"]', self)

        }
        self.elements = munchify(page_elements)

    def login(self,username,password):
        self.element.username.set(username)
        self.element.password.set(password)
        self.element.login_btn.click()
