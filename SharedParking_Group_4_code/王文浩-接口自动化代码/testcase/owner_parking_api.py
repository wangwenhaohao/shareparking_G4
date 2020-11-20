from sharedParkingPlace1111.tools.lib_action import ApiAction,Assert
from sharedParkingPlace1111.tools.parse import FileParse

class TestParkingAPI:

    def test_modify_parking(self):
        test_info = FileParse.get_test_info("..\\conf\\test_info.ini", "parking_api", "modify_parking")
        ApiAction.assert_api(test_info)

    def test_del_parking(self):
        test_info = FileParse.get_test_info("..\\conf\\test_info.ini", "parking_api", "del_parking")
        print(test_info)
        ApiAction.assert_api(test_info)

    def test_add_parking(self):
        test_info = FileParse.get_test_info("..\\conf\\test_info.ini", "parking_api", "add_parking")
        ApiAction.assert_api(test_info)


if __name__ == '__main__':
    # TestParkingAPI().test_modify_parking()
    # TestParkingAPI().test_del_parking()
    TestParkingAPI().test_add_parking()