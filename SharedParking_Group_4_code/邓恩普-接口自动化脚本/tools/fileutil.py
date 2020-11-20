import requests
import xlrd
import os
import time
import configparser
import random
import cv2
from pykeyboard.windows import PyKeyboard
from pymouse import PyMouse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from PIL import ImageGrab


class TimeUtil:
    @classmethod
    def get_filename_time(cls):
        """
        获取用于文件名格式的时间字符串
        :return: 返回的时间字符串格式为%Y%m%d_%H%M%S
        """
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_standard_format_time(cls):
        """
        获取当前系统时间，返回标准格式时间
        :return: 返回的时间格式为%Y-%m-%d %H:%M:%S
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class LogUtil:
    logger = None

    @classmethod
    def get_logger(cls, name):
        """
            返回规定格式的日志生成器对象
        :param name:
            调用logger的模块名
        :return:
            日志生成器对象
        """
        import logging
        if cls.logger is None:
            cls.logger = logging.getLogger(name)
            cls.logger.setLevel(level=logging.INFO)
            if not os.path.exists("../logs"):
                os.mkdir("../logs")
            handler = logging.FileHandler(
                '../logs/' +
                TimeUtil.get_filename_time() +
                '.log',
                encoding='utf8')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
        return cls.logger


class FileUtil:
    # 该类包含所有文件读取方法，包括从普通文本、json格式文本、excel文件中读取的相关方法

    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'fileutil'))

    @classmethod
    def get_txt(cls, path):
        '''
        读取普通文本文件内容，返回字符串
        :param path: 文本文件路径
        :return: 文本文件内容字符串
        '''
        content = None
        try:
            with open(path, encoding='utf8') as rf:
                content = rf.read()
        except BaseException:
            cls.logger.error(f'没有读取{path}文件')
        finally:
            return content

    @classmethod
    def get_txt_line(cls, path):
        """
        按行读取文本内容，返回列表+字符串格式
        :param path: 文本路径
        :return: 列表+字符串（不包含换行，去掉#开始的行内容）
        """
        li = []
        try:
            with open(path, encoding='utf8') as rf:
                contents = rf.readlines()
            for content in contents:
                if not content.startswith('#'):
                    temp = content.strip()
                    li.append(temp)
        except BaseException:
            cls.logger.error(f'没有读取{path}文件')
        finally:
            return li

    @classmethod
    def get_json(cls, path):
        """
            从json格式文件中读取原始格式内容并返回
        :param path:
            要读取的json文件路径
        :return:
            原始数据类型的数据
        """
        import json
        content = None
        try:
            with open(path, encoding='utf8') as rf:
                content = json.load(rf)
        except:
            cls.logger.error(f'{path}文件读取错误')
        finally:
            return content

    @classmethod
    def get_test_info(cls, path, section, option):
        """
        从test_info.ini读取excel配置信息，将excel内容全部读出
        :param path:测试信息配置文件路径及文件名
        :param section: 页面名称
        :param option: 每条测试信息的键
        :return: 测试信息的json格式
        """
        params = eval(cls.get_ini_value(path, section, option))
        wb = xlrd.open_workbook(params['test_info_path'])
        sheet_content = wb.sheet_by_name(params['sheet_name'])
        case_sheet_content = wb.sheet_by_name(params['case_sheet_name'])
        version = case_sheet_content.cell(1, 1).value
        test_data = []
        for i in range(params['start_row'], params['end_row']):
            expect = sheet_content.cell(i, params['expect_col']).value
            data_dict = {}
            request_params = {}
            data_dict['params'] = request_params
            data_dict['expect'] = expect
            data_dict['caseid'] = sheet_content.cell(
                i, params['caseid_col']).value
            data_dict['module'] = sheet_content.cell(
                i, params['module_col']).value
            data_dict['type'] = sheet_content.cell(i, params['type_col']).value
            data_dict['desc'] = sheet_content.cell(i, params['desc_col']).value
            data_dict['version'] = version
            data_dict['uri'] = sheet_content.cell(i, params['uri_col']).value
            data_dict['request_method'] = sheet_content.cell(
                i, params['request_method_col']).value
            test_data.append(data_dict)
        return test_data

    @classmethod
    def get_test_info_params(cls, path, section, option):
        """
        从test_info.ini读取excel配置信息，将excel内容全部读出
        :param path:测试信息配置文件路径及文件名
        :param section: 页面名称
        :param option: 每条测试信息的键
        :return: 测试信息的json格式
        """
        params = eval(cls.get_ini_value(path, section, option))
        wb = xlrd.open_workbook(params['test_info_path'])
        sheet_content = wb.sheet_by_name(params['sheet_name'])
        case_sheet_content = wb.sheet_by_name(params['case_sheet_name'])
        version = case_sheet_content.cell(1, 1).value
        test_data = []
        for i in range(params['start_row'], params['end_row']):
            data = sheet_content.cell(i, params['test_data_col']).value
            expect = sheet_content.cell(i, params['expect_col']).value
            temp = str(data).split('\n')
            data_dict = {}
            request_params = {}
            for t in temp:
                request_params[t.split('=')[0]] = t.split('=')[1]
            data_dict['params'] = request_params
            data_dict['expect'] = expect
            data_dict['caseid'] = sheet_content.cell(
                i, params['caseid_col']).value
            data_dict['module'] = sheet_content.cell(
                i, params['module_col']).value
            data_dict['type'] = sheet_content.cell(i, params['type_col']).value
            data_dict['desc'] = sheet_content.cell(i, params['desc_col']).value
            data_dict['version'] = version
            data_dict['uri'] = sheet_content.cell(i, params['uri_col']).value
            data_dict['request_method'] = sheet_content.cell(
                i, params['request_method_col']).value
            test_data.append(data_dict)
        return test_data


    @classmethod
    def get_ini_value(cls, path, section, option):
        """
        从ini配置文件中读取某个指定的键对应的值并返回
        :param path:配置文件路径
        :param section:节点名称
        :param option:键的名称
        :return:对应的单值
        """
        cp = configparser.ConfigParser()
        value = None
        try:
            cp.read(path, encoding='utf8')
            value = cp.get(section, option)
        except BaseException:
            cls.logger.error('读取配置文件错误')
        return value

    @classmethod
    def get_ini_section(cls, path, section):
        """
        从ini配置文件中读取某个节点下的所有内容，以字典格式返回
        :param path:配置文件路径
        :param section:节点名称
        :return:对应的单值的列表
        """
        cp = configparser.ConfigParser()
        li = []
        try:
            cp.read(path, encoding='utf-8-sig')
            temp = cp.items(section)
            for t in temp:
                di = {}
                di[t[0]] = t[1]
                li.append(di)
        except BaseException:
            cls.logger.error('读取配置文件错误')
        finally:
            return li


class DBUtil:
    # 该类包含数据库连接方法，查询单条数据方法，查询多条数据方法和增删改方法
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'fileutil'))

    def __init__(self, option):
        self.db_info = eval(
            FileUtil.get_ini_value(
                '../conf/base.ini',
                'mysql',
                option))

    def conn_db(self):
        """
        连接数据库返回数据库连接对象
        :return:数据库连接对象
        """
        import pymysql
        conn = None
        try:
            conn = pymysql.connect(
                host=self.db_info[0],
                database=self.db_info[1],
                user=self.db_info[2],
                password=self.db_info[3],
                charset=self.db_info[4])
        except BaseException:
            self.logger.error('数据库连接失败')
        finally:
            return conn

    def query_one(self, sql):
        """
        查询一条结果
        :param sql: 查询语句
        :return: 单条结果集，以元组方式返回
        """
        conn = self.conn_db()
        cur = conn.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchone()
        except BaseException:
            self.logger.error('查询失败')
        finally:
            cur.close()
            conn.close()
            return result

    def query_all(self, sql):
        """
        查询多条结果
        :param sql: 查询语句
        :return: 多条结果集，以二维元组方式返回
        """
        conn = self.conn_db()
        cur = conn.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except BaseException:
            self.logger.error('查询失败')
        finally:
            cur.close()
            conn.close()
            return result

    def update_db(self, sql):
        """
        增删改操作
        :param sql: DML语句
        :return:执行成功或失败的标记
        """
        flag = True
        conn = self.conn_db()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except BaseException:
            flag = False
            self.logger.error('sql执行失败')
        finally:
            cur.close()
            conn.close()
            return flag


class UiUtil:
    driver = None
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'ui_util'))

    @classmethod
    def get_driver(cls):
        from selenium import webdriver
        try:
            browser = FileUtil.get_ini_value(
                '../conf/base.ini', 'ui', 'browser')
            base_url = FileUtil.get_ini_value(
                '../conf/base.ini', 'ui', 'homepage_url')
            if cls.driver is None:
                cls.driver = getattr(webdriver, browser)()
                cls.driver.implicitly_wait(10)
                cls.driver.maximize_window()
                cls.driver.get(base_url)
        except BaseException:
            cls.logger.error('浏览器对象生成错误，请检查配置文件')
        return cls.driver

    @classmethod
    def find_element(cls, section, option):
        try:
            element_attr = FileUtil.get_ini_section(
                '../conf/inspector.ini', section)
            for element in element_attr:
                if option in element.keys():
                    attr = eval(element[option])
            return cls.driver.find_element(getattr(By, attr[0]), attr[1])
        except BaseException:
            return None

    @classmethod
    def input(cls, element, value):
        """
        对文本输入框执行点击、清理和输入值的动作
        :param element:文本元素对象
        :param value:向文本框输入的值
        :return:无
        """
        element.click()
        element.clear()
        element.send_keys(value)

    @classmethod
    def click(cls, element):
        """
        点击某个元素
        :param element:任何一个元素对象
        :return:无
        """
        element.click()

    @classmethod
    def select_ro(cls, element):
        """
        随机选择下拉框中的某一项
        :param element: 下拉框元素对象
        :return: 无
        """
        random_index = random.randint(0, len(Select(element).options) - 1)
        Select(element).select_by_index(random_index)

    @classmethod
    def select_by_text(cls, element, value):
        """
        根据下拉文本选择该项
        :param element: 下拉框元素对象
        :param text: 可见的文本
        :return:无
        """
        Select(element).select_by_visible_text(value)


class ImageMatchByCV:
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'ui_util'))
    mouse = PyMouse()
    keyboard = PyKeyboard()

    @classmethod
    def find_image(cls, target):
        image_path = '../image'
        screen_path = os.path.join(image_path, 'screen.png')
        ImageGrab.grab().save(screen_path)

        # 读取大图对象
        screen = cv2.imread(screen_path)
        # 读取小图对象
        template = cv2.imread(os.path.join(image_path, target))
        # 进行模板匹配，参数包括大图对象、小图对象和匹配算法
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        # 获取匹配结果
        min, max, min_loc, max_loc = cv2.minMaxLoc(result)
        similirity = FileUtil.get_ini_value(
            '../conf/base.ini', 'imagematch', 'similirity')

        if max < float(similirity):
            return -1, -1

        x = max_loc[0] + int(template.shape[1] / 2)
        y = max_loc[1] + int(template.shape[0] / 2)
        return x, y

    @classmethod
    def click_image(cls, target):
        """
        单击一张图片
        :param target:
        :return:
        """
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y)

    @classmethod
    def double_click_image(cls, target):
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y, n=2)

    @classmethod
    def input_image(cls, target, msg):
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.keyboard.type_string(msg)

    @classmethod
    def select_image(cls, target, count):
        # 点击这个下拉框
        cls.click_image(target)
        # count次执行向下键
        for i in range(count):
            cls.keyboard.press_key(cls.keyboard.down_key)
        # 回车
        cls.keyboard.press_key(cls.keyboard.enter_key)

    @classmethod
    def screen_shot(cls, driver, path):
        driver.get_screenshot_as_file(path)


class APIUtil:
    @classmethod
    def get_session(cls):
        """
        获取具有权限的session
        :return: 带登录cookie的session
        """
        session = requests.session()
        login_url = FileUtil.get_ini_value(
            '../conf/base.ini', 'api', 'login_url')
        # login_data = eval(FileUtil.get_ini_value(
        #     '../conf/base.ini', 'api', 'login_data'))
        session.get(login_url)
        return session

    @classmethod
    def login(cls):
        session = cls.get_session()
        login_url = FileUtil.get_ini_value(
            '../conf/base.ini', 'api', 'login_url1')
        session.get(login_url)
        return session

    @classmethod
    def request(cls, method, url, data=None):
        """
        发送请求获得响应
        :param method: 请求方式
        :param url: 请求url
        :param data: 请求数据
        :return: 响应结果
        """
        session = cls.login()
        resp = getattr(session, method)(url, params=data)
        return resp

    @classmethod
    def assert_api(cls, test_info):
        for info in test_info:
            resp = APIUtil.request(
                info['request_method'],
                info['uri'],
                info['params'])
            Assert.assert_equal(resp.text, info['expect'])


class Assert:
    @classmethod
    def assert_equal(cls, expect, actual):
        if expect in actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        print(test_result)



