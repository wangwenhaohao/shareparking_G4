from SharedParkingPlace.action.Inventory_query import Inventory,UiUtil
from SharedParkingPlace.tools.fileutil import FileUtil


class TestInventory:
    def __init__(self, driver):
        self.driver = driver

    def test_01_inventory(self, path,section, option):
        result = FileUtil.get_test_info(path,section,option)
        for i in result:
            Inventory(self.driver).do_query_inventory(i)


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    print(TestInventory(driver).test_01_inventory('../conf/test_info.ini','inventory','query_inventory'))