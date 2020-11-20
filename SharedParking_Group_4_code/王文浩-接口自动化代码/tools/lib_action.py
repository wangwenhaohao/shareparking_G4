from sharedParkingPlace1111.tools.parse import MakeLog,FileParse,TimeFormat

class ApiAction:

    @classmethod
    def get_session(cls, uname):
        '''
        获取具有权限的session
        :return: 带登录cookie的session
        '''
        import requests
        session = requests.Session()
        # login_url = FileParse.get_ini_value('..\\conf\\base.ini', 'api', 'login_uri')
        # print(login_url)
        # login_data = eval(FileParse.get_ini_value('..\\conf\\base.ini', 'api', 'login_data'))
        session.get("http://172.16.13.151:8080/SharedParkingPlace/image")
        session.get(f"http://172.16.13.151:8080/SharedParkingPlace/login?uname={uname}&upass=123&imgcode=0000")
        return session

    @classmethod
    def request(cls, method, url, data=None):
        '''
        请求
        :param method:具体方法
        :param url:路ing
        :param data:参数
        :return:返回响应
        '''
        session = cls.get_session()
        resp = getattr(session, method)(url ,params=data)
        return resp

    @classmethod
    def assert_api(cls, test_info):
        for info in test_info:
            resp = ApiAction.request(info['method'], info['uri'], info['params'])
            Assert.assert_equal(info['expect'], resp.text)

#==============================================================================================

class Assert: #断言类

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
        print(test_result)


if __name__ == '__main__':
    print(ApiAction.get_session())
