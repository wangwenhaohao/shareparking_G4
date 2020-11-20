from SharedParkingPlace.tools.fileutil import FileUtil, APIUtil


class TestSalesAPI:
    def test_scan_barcode(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'seles', 'scan_barcode_api')
        print(test_info[0]['expect'])
        APIUtil.assert_api(test_info)

    def test_query_customer(self):
        test_info = FileUtil.get_test_info(
            '../conf/test_info.ini', 'seles', 'query_customer_api')
        APIUtil.assert_api(test_info)


if __name__ == '__main__':
    TestSalesAPI().test_scan_barcode()
