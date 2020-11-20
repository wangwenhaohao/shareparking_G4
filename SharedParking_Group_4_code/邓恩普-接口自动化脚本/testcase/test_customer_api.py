from SharedParkingPlace.tools.fileutil import FileUtil, APIUtil
import unittest


class TestCustomerAPI(unittest.TestCase):
    def test_01_lessors_del(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'user_management', 'lessors_del')
        APIUtil.assert_api(test_info)

    def test_02_lessors_add(self):
        test_info = FileUtil.get_test_info_params(
            '../conf/test_info.ini', 'user_management', 'lessors_add')
        APIUtil.assert_api(test_info)

    def test_03_tenant_update(self):
        test_info = FileUtil.get_test_info_params(
            '../conf/test_info.ini', 'user_management', 'tenant_update')
        APIUtil.assert_api(test_info)

    def test_04_property_query(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'user_management', 'property_query')
        APIUtil.assert_api(test_info)

    def test_05_view_order_query(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'order_management', 'view_order_query')
        APIUtil.assert_api(test_info)

    def test_06_view_order_del(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'order_management', 'view_order_del')
        APIUtil.assert_api(test_info)

    def test_07_evaluation_management_query(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini',
            'order_management',
            'evaluation_management_query')
        APIUtil.assert_api(test_info)

    def test_08_evaluation_management_del(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini',
            'order_management',
            'evaluation_management_del')
        APIUtil.assert_api(test_info)
