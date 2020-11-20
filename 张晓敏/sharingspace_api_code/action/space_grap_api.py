from sharingspace.tools.util import FileUtil
from sharingspace.tools.lib_util import APIUtil


class Space_Grap:

    def search_address(self):

            search_address_test_info = FileUtil.get_test_info_api('..\\conf\\test_info.ini', 'space_grap', 'search_address_api')
            for test_info in search_address_test_info:
                search_address_resp = APIUtil.request(test_info['request_method'], test_info['uri'], test_info['params'])
                print(search_address_resp.json())
            return search_address_resp.text


if __name__ == '__main__':
    a = Space_Grap()
    a.search_address()