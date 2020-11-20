
import time
import os
import configparser


class TimeUtil:

    @classmethod
    def get_filename_time(cls):
        """
           返回用于文件名格式的时间字符串
       :param :

       :return:
           时间字符串格式为%Y%m%d_%H%M%S
       """
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_standard_format_time(cls):
        """
        获取当前系统时间，返回标准格式时间
        :return: 返回的时间格式为%Y-%m-%d %H:%M:%S
        """

        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# *********************************************************************************************

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
            if not os.path.exists('..\\logs'):
                os.mkdir('..\\logs')
            handler = logging.FileHandler(
                '..\\logs\\' + TimeUtil.get_filename_time() + '.log', encoding='utf8')
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            cls.logger.info('*****************************************************\n')

        return cls.logger

# *********************************************************************************************

class FileUtil:

    # 该类包含所有文件读取方法，包括从普通文本、json格式文本、excel文件中读取的相关方法
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'util'))

    @classmethod
    def get_txt(cls, path):
        """
        读取普通文本文件内容，返回字符串
        :param path: 文本文件路径
        :return: 文本文件内容字符串
        """
        content = None
        try:
            with open(path, encoding='utf-8') as file:
                content = file.read()
        except:
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
            with open(path, encoding='utf-8') as file:
                contents = file.readlines()

            for content in contents:
                if not content.startswith('#'):
                    t = content.strip()
                    li.append(t)
        except:
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

        import json5
        content = None
        try:
            with open(path, encoding='utf8') as file:
                content = json5.load(file)
        except BaseException:
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
        import xlrd

        workbook = xlrd.open_workbook(params['test_info_path'])
        sheet_content = workbook.sheet_by_name(params['sheet_name'])
        case_sheet_content = workbook.sheet_by_name(params['case_sheet_name'])
        version = case_sheet_content.cell(1,1).value
        test_data = []

        for i in range(params['start_row'], params['end_row']):
            data = sheet_content.cell(i, params['test_data_col']).value
            expect = sheet_content.cell(i, params['expect_col']).value
            temp = str(data).split('\n')
            di = {}
            for t in temp:
                di[t.split('=')[0]] = t.split('=')[1]
            di['expect'] = expect
            di['caseid'] = sheet_content.cell(i, params['caseid_col']).value
            di['module'] = sheet_content.cell(i, params['module_col']).value
            di['type'] = sheet_content.cell(i, params['type_col']).value
            di['desc'] = sheet_content.cell(i, params['desc_col']).value
            di['version'] = version
            test_data.append(di)

        return test_data

    @classmethod
    def get_test_info_api(cls, path, section, option):
        """
        从test_info.ini读取excel配置信息，将excel内容全部读出
        :param path:测试信息配置文件路径及文件名
        :param section: 页面名称
        :param option: 每条测试信息的键
        :return: 测试信息的json格式
        """
        params = eval(cls.get_ini_value(path, section, option))
        import xlrd

        workbook = xlrd.open_workbook(params['test_info_path'])
        sheet_content = workbook.sheet_by_name(params['sheet_name'])
        case_sheet_content = workbook.sheet_by_name(params['case_sheet_name'])
        version = case_sheet_content.cell(1,1).value
        test_data = []

        for i in range(params['start_row'], params['end_row']):
            data = sheet_content.cell(i, params['test_data_col']).value
            expect = sheet_content.cell(i, params['expect_col']).value
            temp = str(data).split('\n')
            di = {}
            request_params = {}     # 用于保存发送接口传递的参数
            for t in temp:
                request_params[t.split('=')[0]] = t.split('=')[1]
            di['params'] = request_params
            di['expect'] = expect
            di['caseid'] = sheet_content.cell(i, params['caseid_col']).value
            di['module'] = sheet_content.cell(i, params['module_col']).value
            di['type'] = sheet_content.cell(i, params['type_col']).value
            di['desc'] = sheet_content.cell(i, params['desc_col']).value
            di['version'] = version
            di['uri'] = sheet_content.cell(i, params['uri']).value
            di['request_method'] = sheet_content.cell(i, params['request_method']).value
            test_data.append(di)
        # print(test_data)
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
            cp.read(path, encoding='utf-8')
            value = cp.get(section, option)
        except BaseException:
            cls.logger.error('读取配置文件错误')
        return value

    @classmethod
    def get_ini_section(cls, path, section):
        """
        从ini配置文件中读取某个节点下的所有内容，以字典格式返回
        :param path:
        :param section:
        :return:
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

# *******************************************************************************

class DBUtil:

    # 该类包含数据库连接方法，查询单条数据方法，查询多条数据方法和增删改方法
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'util'))

    def __init__(self, option):
        self.db_info = eval(
            FileUtil.get_ini_value(
                '..\\conf\\base.ini',
                'mysql',
                f'{option}'))

    def get_conn(self):
        """
        连接数据库返回数据库连接对象
        :param db_info:数据库配置信息
        :return:数据库连接对象
        """
        import pymysql
        conn = None
        try:
            conn = pymysql.connect(
                host=self.db_info[0],
                user=self.db_info[1],
                password=self.db_info[2],
                database=self.db_info[3],
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

        conn = self.get_conn()
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

        conn = self.get_conn()
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

        conn = self.get_conn()
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

if __name__ == '__main__':
    print(FileUtil.get_test_info('..\\conf\\test_info.ini', 'login', 'login_info'))