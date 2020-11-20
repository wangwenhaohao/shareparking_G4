import unittest
from SharedParkingPlace.tools.fileutil import FileUtil
from HTMLTestRunner import HTMLTestRunner


class Start:
    def start(self, path):
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        test_class_info = FileUtil.get_txt(path)
        tests = loader.loadTestsFromName(test_class_info)

        suite.addTests(tests)

        with open('report.html', 'w') as wf:
            runner = HTMLTestRunner(stream=wf, verbosity=2)
            runner.run(suite)


if __name__ == '__main__':
    Start().start('../conf/case_class_path.conf')
