import os
import random
from selenium.webdriver.support.select import Select
from selenium import webdriver
from SharedParkingPlace.tools.fileutil import LogUtil


class Collection:
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'collection'))
    driver = None

    @classmethod
    def open_browser(cls, browser):
        if hasattr(webdriver, browser):
            cls.driver = getattr(webdriver, browser)()
        else:
            cls.logger.error('浏览器名称不正确')
            cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        return cls.driver

    @classmethod
    def find_element(cls, attr):
        at = attr.split('=')
        element = None
        try:
            if at[0] == 'id':
                element = cls.driver.find_element_by_id(at[1])
            elif at[0] == 'link_text':
                element = cls.driver.find_element_by_link_text(at[1])
            elif at[0] == 'css_selector':
                element = cls.driver.find_element_by_css_selector(at[1])
            elif at[0] == 'xpath':
                element = cls.driver.find_element_by_xpath(at[1])
        except BaseException:
            cls.logger.error(f'没有找到{attr}元素')
        finally:
            return element

    @classmethod
    def get_page(cls, url):
        cls.driver.get(url)

    @classmethod
    def click(cls, attr):
        element = cls.find_element(attr)
        if element is not None:
            element.click()
        return element

    @classmethod
    def input(cls, attr, value):
        element = cls.click(attr)
        element.clear()
        element.send_keys(value)

    @classmethod
    def iframe(cls,attr):
        iframe = cls.find_element(attr)
        cls.driver.switch_to.frame(iframe)
        return cls.driver

    @classmethod
    def select(cls, attr, value):
        element = cls.find_element(attr)
        Select(element).select_by_index(value)

    @classmethod
    def select_ro(cls, attr):
        element = cls.find_element(attr)
        random_index = random.randint(0, len(Select(element).options) - 1)
        Select(element).select_by_index(random_index)

    @classmethod
    def alert(cls):
        cls.driver.switch_to.alert.accept()

    @classmethod
    def get_page_text(cls, attr):
        element = cls.find_element(attr)
        return element.text

    @classmethod
    def input_keyborad(cls,attr,value):   ##   使用ctrl+a 进行全选输入替换
        from selenium.webdriver.common.keys import Keys
        element = cls.find_element(attr)
        element.send_keys(Keys.CONTROL,'a')
        element.send_keys(value)

    @classmethod
    def assert_exist_element(cls, attr):
        element = cls.find_element(attr)
        if element is not None:
            print('页面存在该元素，测试成功')
        else:
            print('页面不存在该元素，测试失败')

    @classmethod
    def sleep(cls, ctime):
        import time
        time.sleep(int(ctime))

    @classmethod
    def close(cls):
        cls.driver.quit()
