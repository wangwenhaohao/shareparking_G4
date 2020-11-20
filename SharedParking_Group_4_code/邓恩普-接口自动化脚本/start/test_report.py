import time
from SharedParkingPlace.tools.fileutil import DBUtil, TimeUtil, LogUtil


class TestReport:
    def __init__(self, app_name):
        self.app_name = app_name
        self.logger = LogUtil.get_logger('test_report')

    def write_result_db(self, result_info):
        now = TimeUtil.get_standard_format_time()
        sql = 'insert into %s (version,module,case_type,case_id,case_desc,' \
              'test_result,execute_time,error_msg,error_screenshot)' \
              ' values("%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
              % (self.app_name, result_info['version'], result_info['module'],
                 result_info['case_type'], result_info['case_id'], result_info['case_desc'],
                 result_info['test_result'], now, result_info['error_msg'],
                 result_info['error_screenshot'])
        DBUtil('db_report').update_db(sql)

    def generate_html_report(self, version):
        # 根据不同的版本读取该版本的测试结果数据
        sql_all = f'select * from test_result where version = "{version}";'
        all_result = DBUtil('db_report').query_all(sql_all)
        if len(all_result) == 0:
            self.logger.info('当前版本没有测试结果。')
            return
        # 替换模板上特定位置的字符串
        with open('../conf/template.html', encoding='utf8') as rf:
            content = rf.read()
        content = content.replace('$test-version', version)

        # 计算测试执行成功的数量
        base_sql = 'select count(*) from test_result where version = "%s" and ' % version
        query_pass = base_sql + 'test_result = "测试通过"'
        pass_count = str(DBUtil('db_report').query_one(query_pass)[0])
        content = content.replace('$pass-count', pass_count)
        # 计算测试执行失败的数据
        query_fail = base_sql + 'test_result = "测试失败"'
        fail_count = str(DBUtil('db_report').query_one(query_fail)[0])
        content = content.replace('$fail-count', fail_count)
        # 计算测试执行错误的数据
        query_error = base_sql + 'test_result = "测试错误"'
        error_count = str(DBUtil('db_report').query_one(query_error)[0])
        content = content.replace('$error-count', error_count)
        # 获取最后一条用例执行的时间
        query_last_time = f'select execute_time from test_result where version' \
                          f' = "{version}" order by execute_time desc limit 1;'
        last_time = str(DBUtil('db_report').query_one(query_last_time)[0])
        content = content.replace('$last-time', last_time)
        # 获取日期
        content = content.replace('$test-date', last_time.split(' ')[0])

        test_result = ''
        for record in all_result:
            if record[6] == '成功':
                color = 'lightgreen'
            elif record[6] == '失败':
                color = 'red'
            else:
                color = 'yellow'
            if record[9] == '无':
                screenshot = '无'
            else:
                screenshot = f'<a href="{record[9]}">查看截图</a>'
            test_result += f'<tr height="40">' \
                           f'<td width="7%">{record[0]}</td>' \
                           f'<td width="9%">{record[2]}</td>' \
                           f'<td width="10%">{record[3]}</td>' \
                           f'<td width="7%">{record[4]}</td>' \
                           f'<td width="20%">{record[5]}</td>' \
                           f'<td width="7%" bgcolor="{color}">{record[6]}</td>' \
                           f'<td width="15%">{record[7]}</td>' \
                           f'<td width="15%">{record[8]}</td>' \
                           f'<td width="10%">{screenshot}</td>' \
                           f'</tr>\r\n'
        content = content.replace('$test-result', test_result)

        now = int(time.time())
        report_path = f'../report/{version}/{self.app_name}_{version}_{now}版本测试报告.html'
        with open(report_path, 'w', encoding='utf8') as wf:
            wf.write(content)


if __name__ == '__main__':
    test = TestReport('test_result')
    result_info = {
        "version": "v2.0",
        "module": "登录",
        "case_type": "GUI",
        "case_id": "login_01",
        "case_desc": "登录成功",
        "test_result": "测试通过",
        "error_msg": "无",
        "error_screenshot": "无"}
    test.write_result_db(result_info)
    test.generate_html_report('v2.0')
