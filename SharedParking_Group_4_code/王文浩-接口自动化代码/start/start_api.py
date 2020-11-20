from HTMLTestRunner_cn import HTMLTestRunner
from sharedParkingPlace1111.tools.parse import FileParse
import unittest
from sharedParkingPlace1111.testcase.owner_parking_api import TestParkingAPI

class AllStart:

    def start(self, path):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        test_case_info = FileParse.get_txt(path)
        print(test_case_info)
        tests = loader.loadTestsFromTestCase(test_case_info)
        suite.addTests(tests)

        with open('report.html', 'w') as file:
            runner = HTMLTestRunner(stream=file, verbosity=2)
            runner.run(suite)

if __name__ == '__main__':
    AllStart().start("..\\conf\\case_class_path.conf")