from sharingspace.tools.util import FileUtil
from sharingspace.tools.lib_util import APIUtil
import requests


class LoginApi:

    # def __init__(self, session):
        # self.session = session

    def login(self):

        # from woniutestV05.tools.util import

        login_test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'login', 'login_info_api')
        for test_info in login_test_info:
            login_resp = APIUtil.request(test_info['request_method'], test_info['uri'], test_info['params'])
            print(login_resp.text)
        return login_resp.text


    # def query_customer(self):
    #     query_customer_test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'sales', 'query_customer_api')
    #     for test_info in query_customer_test_info:
    #         query_customer_resp = APIUtil.request(test_info['request_method'], test_info['uri'], test_info['params'])
    #         print(query_customer_resp.text)
    #     return query_customer_resp.text
    #
    # def sale(self):
    #     pass



if __name__ == '__main__':
    a = LoginApi()
    a.login()