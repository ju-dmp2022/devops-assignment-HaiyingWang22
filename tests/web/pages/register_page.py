from tests.web.pages.page_base import PageBase
from tests.web.helpers.element import Element
from munch import munchify


class RegisterPage(PageBase):
    def __init__(self, driver):
        PageBase.__init__(self, driver = driver)

        page_elements = {
            'username': Element('//input[@id="username"]', self),
            'password1': Element('//input[@id="password1"]', self),
            'password2': Element('//input[@id="password2"]', self),
            'register_btn': Element('//button[@id="register"]', self),
            'message':Element('//div[@id="errormsg"]', self),

        }
        self.elements = munchify(page_elements)

    def register(self,username,password):
        self.element.username.set(username)
        self.element.password1.set(password)
        self.element.password2.set(password)
        self.element.register_btn.click()

        

