from SharedParkingPlace.tools.fileutil import UiUtil


class Login:
    def __init__(self, driver):
        self.driver = driver

    def input_username(self, username):
        uname_element = UiUtil.find_element('login','uname')
        UiUtil.input(uname_element, username)

    def input_password(self, password):
        upass_element = UiUtil.find_element('login','upass')
        UiUtil.input(upass_element, password)

    def input_verifycode(self, verifycode):
        vfcode_element = UiUtil.find_element('login','vfcode')
        UiUtil.input(vfcode_element, verifycode)

    def click_login_button(self):
        login_button = UiUtil.find_element('login','login_button')
        UiUtil.click(login_button)

    def error_prompt(self):
        error_prompt = UiUtil.find_element('login','prompt')
        UiUtil.click(error_prompt)

    def click_cancellation_button(self):
        button_element = UiUtil.find_element('login','cancellation')
        UiUtil.click(button_element)

    def do_login(self, login_data):
        self.input_username(login_data['username'])
        self.input_password(login_data['password'])
        self.input_verifycode(login_data['verifycode'])
        self.click_login_button()


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    Login(driver).do_login({'username':'admin', 'password':'Milor123', 'verifycode':'0000'})