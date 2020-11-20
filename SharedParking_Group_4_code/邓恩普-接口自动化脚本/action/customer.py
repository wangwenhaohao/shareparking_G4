from SharedParkingPlace.tools.fileutil import UiUtil


class Customer:
    def __init__(self, driver):
        self.driver = driver

    def into_customer(self):
        into_members = UiUtil.find_element('customer', 'customer_button')
        UiUtil.click(into_members)

    def input_cphone(self, cphone):
        customerphone = UiUtil.find_element('customer', 'phone')
        UiUtil.input(customerphone, cphone)

    def input_nick_name(self, name):
        customername = UiUtil.find_element('customer', 'name')
        UiUtil.input(customername, name)

    def select_childsex(self, sex):
        gender = UiUtil.find_element('customer', 'sex')
        UiUtil.select_by_text(gender, sex)

    def input_childdate(self, childdate):
        date = self.driver.find_element_by_id('childdate')
        self.driver.execute_script(
            'document.getElementById("childdate").readOnly=false;')
        UiUtil.input(date, childdate)

    def input_creditkids(self, credit):
        creditkids = self.driver.find_element_by_id('creditkids')
        UiUtil.input(creditkids, credit)

    def input_creditcloth(self, credit):
        creditcloth = self.driver.find_element_by_id('creditcloth')
        UiUtil.input(creditcloth, credit)

    def click_add(self):
        add = self.driver.find_element_by_xpath(
            "//button[contains(text(),'新增')]")
        UiUtil.click(add)

    def click_edit(self):
        edit = self.driver.find_element_by_xpath(
            "//button[contains(text(),'修改')]")
        UiUtil.click(edit)

    def click_query(self):
        query = self.driver.find_element_by_xpath(
            "//button[contains(text(),'查询')]")
        UiUtil.click(query)

    def click_gotoEdit(self):
        edit = self.driver.find_element_by_xpath("//a[contains(text(),'修改')]")
        UiUtil.click(edit)

    def do_add_customer(self, customer):
        self.into_customer()
        self.input_cphone(customer['customerphone'])
        self.input_nick_name(customer['customername'])
        self.select_childsex(customer['childsex'])
        self.input_childdate(customer['childdate'])
        self.input_creditkids(customer['creditkids'])
        self.input_creditcloth(customer['creditcloth'])
        self.click_add()

    def do_query_customer(self, customer):
        self.into_customer()
        self.input_cphone(customer['cphone'])
        self.click_query()

    def do_edit_customer(self, customer):
        self.do_query_customer(customer)
        self.click_gotoEdit()
