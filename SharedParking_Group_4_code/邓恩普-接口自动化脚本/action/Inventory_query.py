import time

from SharedParkingPlace.tools.fileutil import UiUtil
from SharedParkingPlace.action.login import Login


class Inventory:
    def __init__(self, driver):
        self.driver = driver

    def into_inventory(self):
        inventory_element = self.driver.find_element_by_xpath("//a[text()='库存查询']")
        UiUtil.click(inventory_element)

    def input_goodsserial(self, serial):
        goodsserial_element = self.driver.find_element_by_id('goodsserial')
        UiUtil.input(goodsserial_element, serial)

    def input_goodsname(self, name):
        goodsname_element = self.driver.find_element_by_id('goodsname')
        UiUtil.input(goodsname_element, name)

    def input_barcode(self, barcode):
        barcode_element = self.driver.find_element_by_id('barcode')
        UiUtil.input(barcode_element, barcode)

    def select_goodstype(self, type):
        goodstype_element = self.driver.find_element_by_id('goodstype')
        UiUtil.select_by_text(goodstype_element, type)

    def input_earlystoretime(self, time):
        earlystoretime_element = self.driver.find_element_by_id(
            'earlystoretime')
        self.driver.execute_script(
            'document.getElementById("earlystoretime").readOnly=false;')
        UiUtil.input(earlystoretime_element, time)

    def input_laststoretime(self, time):
        laststoretime_element = self.driver.find_element_by_id('laststoretime')
        self.driver.execute_script(
            'document.getElementById("laststoretime").readOnly=false;')
        UiUtil.input(laststoretime_element, time)

    def click_query_inventory(self):
        query_element = self.driver.find_element_by_xpath(
            "//input[@value='按条件查询库存情况']")
        UiUtil.click(query_element)

    def click_query_zero_stock(self):
        query_element = self.driver.find_element_by_xpath(
            "//input[@value='查询零库存商品']")
        UiUtil.click(query_element)

    def click_query_no_stock(self):
        query_element = self.driver.find_element_by_xpath(
            "//input[@value='查询未入库商品']")
        UiUtil.click(query_element)

    def do_query_inventory(self, params):
        Login(self.driver).do_login({'username': 'admin',
                                'password': 'Milor123', 'verifycode': '0000'})
        time.sleep(2)
        self.into_inventory()
        self.input_goodsserial(params['serial'])
        self.input_goodsname(params['name'])
        self.input_barcode(params['barcode'])
        self.select_goodstype(params['type'])
        self.click_query_inventory()

    def get_query_inventory_result(self):
        result = self.driver.find_element_by_xpath('//*[@id="storedlist"]/tbody')
        print(result.text)

