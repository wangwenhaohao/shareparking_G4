from sharingspace.tools.lib_util import APIUtil, Assert
from sharingspace.tools.util import FileUtil
import unittest
# //td[@id="tangram-suggestion--TANGRAM__1o-item0"]

class TestSalesApi():

    def test_search_address(self):
        test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'space_grap', 'search_address_api')
        APIUtil.assert_api(test_info)

    # def test_query_customer(self):
    #     test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'sales', 'query_customer_api')
    #     APIUtil.assert_api(test_info)


if __name__ == '__main__':
    TestSalesApi().test_search_address()