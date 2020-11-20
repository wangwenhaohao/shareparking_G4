import os
import configparser

class TimeFormat:
    @classmethod
    def get_filename_time(cls):  # 获取当前系统时间
        import time
        return time.strftime('%Y%m%d_%H%M%S', time.localtime())

    @classmethod
    def get_standar_time(cls):  # 数据库里面用的时间
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

#===================================================================================

class MakeLog:  #生成日志
    logger = None

    @classmethod
    def get_logger(cls,name): #生成日志
        """
        生成日志文件
        信息级别：debug,info,warn,error
        :return:
        """
        import logging
        if cls.logger is None:
            cls.logger = logging.getLogger(name)  #再那个模块生成日志
            cls.logger.setLevel(level=logging.INFO)  #日志信息级别
            if not os.path.exists('..\\logs'): #如果日志文件不存在生成日志文件夹
                os.mkdir('..\\logs')
            #创建logger文件句柄，与文件的关联
            handler = logging.FileHandler('..\\logs\\' + TimeFormat.get_filename_time() + '.log',encoding='utf8')
            #定义信息的格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls.logger.addHandler(handler)
            cls.logger.info('*****************************************************\n')
        return cls.logger

#==============================================================================================

class FileParse:
    '''
    得到logger,os.path.join把一个路径和一个字符串合并为一个路径，
    os.getcwd()获取当前页面的绝对路径
    '''
    logger = MakeLog.get_logger(os.path.join(os.getcwd(),'parse'))

    @classmethod
    def get_txt(cls,path):
        '''
        读取普通文本文件的方法
        :param path: 文件路径
        :return: 以字符串形式返回文件内容
        '''
        result = None
        try:
            with open(path, encoding='utf-8') as rf:
                result = rf.read()
        except:
            cls.logger.error(f"读取{path}文件失败")
        finally:
            return result

    @classmethod
    def get_txt_line(cls, path):
        '''
        按行读取文本，去掉注释,[str,str]
        :param path:文件路径
        :return:返回[str,str]格式文件
        '''
        li = []
        try:
            with open(path, encoding='utf-8') as file:
                contents = file.readlines()
            for content in contents:
                if not content.startswith('#'):
                    temp = content.strip()
                    li.append(temp)
        except:
            cls.logger.error(f"读取{path}文件失败")
        finally:
            return li

    @classmethod
    def get_json(cls,path):
        '''
        获取json字符串，转换为json对象，python可识别的
        :param path: 打开文件的路径
        :return: 返回转换后的文件，{[]}json格式
        '''
        import json5
        content = None
        try:
            with open(path,encoding='utf8') as rf:
                content = json5.load(rf)
        except:
            cls.logger.error(f'文件{path}读取错误')
        finally:
            return content

    @classmethod
    def get_ini_value(cls,path,section,option):
        '''
        读取ini文件中的某个section中的某个键值对的值
        :param path: 文件路径
        :param section: 节点名称
        :param option:  键名
        :return: 返回节点对应的键的值
        '''
        cp = configparser.ConfigParser()  #实例化一个对象
        value = None
        try:
            cp.read(path,encoding='utf-8-sig')
            value = cp.get(section,option)
        except:
            cls.logger.error(f"读取{path}文件错误")
        finally:
            return value

    @classmethod
    def get_ini_section(cls,path,section):
        '''
        读取ini文件中的某个section全部内容
        :param path: 文件路径
        :param section: 节点名称
        :return: 返回节点下面的所有键的值，[{},{}]
        '''
        cp = configparser.ConfigParser()
        list_finl = []
        try:
            cp.read(path,encoding='utf-8')
            temp = cp.items(section)
            for t in temp:
                di = {}
                di[t[0]] = t[1]
                list_finl.append(di)
        except:
            cls.logger.error(f"获取{path}文件的{section}错误")
        finally:
            return list_finl

    @classmethod
    def get_test_info(cls, path, section, option):
        """
        读取excel文件内容
        :param section: 配置信息的:login,addcustomer,querycustomer
        :return:读取excel文件[{},{}]
        """
        import xlrd
        test_data_list = []
        try:
            params = eval(cls.get_ini_value(path, section, option))
            # print(params)
            workbook = xlrd.open_workbook(params['path'])
            # print(workbook)
            sheet_content = workbook.sheet_by_name(params['sheet_name'])
            case_sheet_content = workbook.sheet_by_name(params['case_sheet_name'])
            # print(case_sheet_content)
            version = case_sheet_content.cell(1, 1).value
            # print(version)
            # print(type(params['start_row']))
            for i in range(params['start_row'], params['end_row']):
                test_data = sheet_content.cell(i, params['data_col']).value
                # print(type(test_data))
                expect = sheet_content.cell(i, params['expect_col']).value
                # print(expect)
                di = {}
                data_list = {}
                if test_data:  #判断是否是空的
                    temp = str(test_data).split('\n')
                    # print(temp)
                    for t in temp:
                        data_list[t.split('=')[0]] = t.split('=')[1]
                # print(data_list)
                di['params'] = data_list
                di['expect'] = expect
                di['case_id'] = sheet_content.cell(i, params['case_id_col']).value
                di['module'] = sheet_content.cell(i, params['module_col']).value
                di['type'] = sheet_content.cell(i, params['type_col']).value
                di['case_desc'] = sheet_content.cell(i, params['desc_col']).value
                di['version'] = version
                di['uri'] = sheet_content.cell(i, params['uri_col']).value
                di['method'] = sheet_content.cell(i, params['method_col']).value
                test_data_list.append(di)
        except:
            cls.logger.error(f'读取{path}的{section}的{option}文件失败')
        finally:
            return test_data_list

    #解析yaml文件
    @classmethod
    def get_ymal(cls,path):
        import yaml
        try:
            with open(path,encoding='utf-8') as y:
                result = yaml.load(y.read(),Loader=yaml.SafeLoader)
        except:
            cls.logger.error("yaml文件读取失败")
        finally:
            return result

#=============================================================================================

class DataBase:
    """
    数据操作：
    建立链接，
    查询，1条，多条
    更新，增，删，改
    """
    def __init__(self, section, option):
    #日志生成器
        self.logger = MakeLog.get_logger(os.path.join(os.getcwd(),'parse'))
        self.db_info = eval(FileParse.get_ini_value('..\\conf\\base.ini', section, option))

    #与mysql数据库建立链接
    def get_conn(self):
        import pymysql
        #解析ini数据
        db_info = self.db_info
        conn = None
        try:
            conn = pymysql.connect(host=db_info[0],database=db_info[3],
                user=db_info[1],password=db_info[2],charset=db_info[4])
        except:
            self.logger.error("数据库链接异常")
        finally:
            return conn

    #获取一条信息，记得要关闭游标和链接
    def get_one(self,sql):
        conn = self.get_conn()
        cur = conn.cursor()
        result = None
        try:
            cur.execute(sql)
            result = cur.fetchone()
        except:
            self.logger.error("数据库查询异常")
        finally:
            cur.close()
            conn.close()
            return result

    #查询多条数据库信息
    def get_all(self,sql):
        result = None
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
        except:
            self.logger.error('查询多条数据库信息错误')
        finally:
            cur.close()
            conn.close()
            return result

    #数据库更新操作
    def update_db(self, sql):
        flag = True  #标识符，判断是否执行正确
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()  #执行完增删改后要提交，不然数据库中没有实际信息
        except:
            flag = False
            self.logger.error("sql更新操作执行失败")
        finally:
            cur.close()
            conn.close()
            return flag
