import os

class LogUtil:

    logger = None

    @classmethod
    def get_ctime(cls):
        """
           返回规定格式的时间字符串
       :param :

       :return:
           时间字符串格式为%Y%m%d_%H%M%S
       """
        import time
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

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
            # 获取日志生成器对象
            cls.logger = logging.getLogger(name)
            # 定义获取信息的级别
            cls.logger.setLevel(level=logging.INFO)
            # 如果日志目录不存在则创建
            if not os.path.exists('../logs'):
                os.mkdir('../logs')
            # 创建logger的文件句柄与规定的文件关联
            handler = logging.FileHandler('..\\logs\\'+cls.get_ctime()+'.log', encoding='utf8')
            # 定义信息的格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            cls.logger.info('*****************************************************\n')

        return cls.logger


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
        with open(path, encoding='utf-8') as file:
            content = file.read()
        return content

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
            cls.logger.info('读取正确')
        except:
            cls.logger.error('文件读取错误')
        finally:
            return content

    @classmethod
    def get_excel(cls, path, index):
        """
        从excel文件中读取测试信息
        :param path:测试信息配置文件路径及文件名
        :param index: 测试信息索引下标
        :return: 测试信息的json格式
        """
        params = cls.get_json(path)[index]
        import xlrd

        # 读取excel文件
        workbook = xlrd.open_workbook(params['path'])
        # 读取sheet页的内容
        sheet_content = workbook.sheet_by_name(params['sheet_name'])
        login_data = []

        for i in range(params['start_row'],params['end_row']):
            test_data = sheet_content.cell(i, params['data_col']).value
            expect = sheet_content.cell(i, params['expect_col']).value
            temp = str(test_data).split('\n')
            di ={}
            for t in temp:
                di[t.split('=')[0]] = t.split('=')[1]
            di['expect'] = expect
            login_data.append(di)

        return login_data

    @classmethod
    def get_ini_value(cls, path, section, option):
        """
        从ini配置文件中读取某个指定的键对应的值并返回
        :param path:配置文件路径
        :param section:节点名称
        :param option:键的名称
        :return:对应的单值
        """
        import configparser
        cp = configparser.ConfigParser()
        value = None
        try:
            cp.read(path, encoding='utf-8')
            value = cp.get(section, option)
        except:
            cls.logger.error('读取配置文件错误')
        return value

    @classmethod
    def get_ini_section(cls, path, section):
        import configparser
        cp = configparser.ConfigParser()
        li = []
        try:
            cp.read(path, encoding='utf-8-sig')
            temp = cp.items(section)
            for t in temp:
                di = {}
                di[t[0]] = t[1]
                li.append(di)
        except:
            cls.logger.error('读取配置文件错误')
        finally:
            return li

class DBUtil:

    # 该类包含数据库连接方法，查询单条数据方法，查询多条数据方法和增删改方法
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'util'))

    @classmethod
    def get_conn(cls, db_info):
        """
        连接数据库返回数据库连接对象
        :param db_info:数据库配置信息
        :return:数据库连接对象
        """
        import pymysql
        conn = None
        try:

            conn = pymysql.connect(host=db_info[0], database=db_info[1], user=db_info[2], password=db_info[3], charset=db_info[4])
        except:
            cls.logger.error('数据库连接失败')
        finally:
            return conn

    @classmethod
    def query_one(cls, sql):
        """
        查询一条结果
        :param sql: 查询语句
        :return: 单条结果集，以元组方式返回
        """
        db_info = eval(FileUtil.get_ini_value('../conf/base.ini', 'mysql', 'db_info'))
        conn = cls.get_conn(db_info)
        cur = conn.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchone()
        except:
            cls.logger.error('查询失败')
        finally:
            cur.close()
            conn.close()
            return result

    @classmethod
    def query_all(cls, sql):
        """
        查询多条结果
        :param sql: 查询语句
        :return: 多条结果集，以二维元组方式返回
        """
        db_info = eval(FileUtil.get_ini_value('../conf/base.ini', 'mysql', 'db_info'))
        conn = cls.get_conn(db_info)
        cur = conn.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except:
            cls.logger.error('查询失败')
        finally:
            cur.close()
            conn.close()
            return result

    @classmethod
    def update_db(cls, sql):
        """
        增删改操作
        :param sql: DML语句
        :return:执行成功或失败的标记
        """
        flag = True
        db_info = eval(FileUtil.get_ini_value('../conf/base.ini', 'mysql', 'db_info'))
        conn = cls.get_conn(db_info)
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
        except:
            flag = False
            cls.logger.error('sql执行失败')
        finally:
            cur.close()
            conn.close()
            return flag

if __name__ == '__main__':

    # print(DBUtil.query_one('select * from user where userid=2'))
    print(FileUtil.get_ini_section('../conf/base.ini', 'host'))
