
from sharingspace.tools.util import FileUtil


class APIUtil:

    # session = None
    @classmethod
    def get_session(cls):
        '''
        获取具有权限的session
        :return: 带登录cookie的session
        '''
        import requests
        session = requests.session()
        session.get(url='http://192.168.77.146:8080/SharedParkingPlace/image')
        login_url = FileUtil.get_ini_value('..\\conf\\base.ini', 'api', 'login_url')
        login_data = eval(FileUtil.get_ini_value('..\\conf\\base.ini', 'api', 'login_data'))
        # print(login_data)
        # login_resp = session.get(url='http://192.168.77.146:8080/SharedParkingPlace/login?uname=抢租客0&upass=123&imgcode=0000')
        # login_resp = session.get(url=login_url, params=login_data)
        session.get(url=login_url, params=login_data)
        # print(login_resp.text)
        return session

    @classmethod
    def request(cls, method, url, data=None):

        session = cls.get_session()
        resp = getattr(session, method)(url, params=data)
        return resp
        # if method == 'get':     # 查询
        #     return session.get(url, params=data)
        # elif method == 'post':
        #     return session.post(url, data)
        # elif method == 'put':   # 修改
        #     return session.put(url, data)
        # elif method == 'delete':
        #     return session.delete(url, parama=data)

    @classmethod
    def assert_api(cls, test_info):
        for info in test_info:
            resp = APIUtil.request(info['request_method'], info['uri'], info['params'])
            print(Assert.assert_equal(resp.text, info['expect']))


class Assert:

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        # print(test_result)
        return test_result

from selenium.webdriver.common.by import By

from woniutest.tools.fileutil import FileUtil
import os


class UiUtil:

    driver = None
    logger = FileUtil.get_logger(os.path.join(os.getcwd(), 'ui_util'))

    @classmethod
    def get_driver(cls):
        print('**************')
        from selenium import webdriver
        try:
            browser = FileUtil.get_ini_value('..\\conf\\base', 'ui', 'browser')
            url = FileUtil.get_ini_value('..\\conf\\base', 'ui', 'url')
            if cls.driver is None:
                cls.driver = getattr(webdriver, browser)()
                cls.driver.implicitly_wait(5)
                cls.driver.maximize_window()
                cls.driver.get(url)
        except:
            cls.logger.error('浏览器对象生成错误，请检查配置文件')
        return cls.driver

    @classmethod
    def find_element(cls, section, option):
        try:
            element_attr = FileUtil.get_ini_section('..\\conf\\inspector.ini', section)
            for element in element_attr:
                if option in element.keys():
                    attr = eval(element[option])
            return cls.driver.find_element(getattr(By, attr[0]), attr[1])
        except:
            return None

    @classmethod
    def input(cls, element, value):
        '''

        :param element:
        :param value:
        :return:
        '''
        element.click()
        element.clear()
        element.send_keys(value)

    @classmethod
    def click(cls, element):
        element.click()

    @classmethod
    def select_ro(cls, element):
        '''

        :param element:
        :return:
        '''
        from selenium.webdriver.support.select import Select
        import random
        random_index = random.randint(0, len(Select(element).options)-1)
        Select(element).select_by_index(random_index)

    # 判断页面上某个元素是否存在
    @classmethod
    def is_element_present(cls, driver, how, what):
        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True



if __name__ == '__main__':
    a = APIUtil()
    # test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'sales', 'scan_barcode_api')
    # a.assert_api(test_info)
    a.get_session()


