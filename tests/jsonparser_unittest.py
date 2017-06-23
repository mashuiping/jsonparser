import unittest
from JsonParser import jsonparser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_function = jsonparser.JsonParser.loads

    def test_parse_true(self):
        # 测试引发异常
        self.assertRaises(ValueError, self.test_function(u"\r\rTrue\r\r"))
        self.assertRaises(ValueError, self.test_function(u"\n\ntRue\n\n"))
        self.assertRaises(ValueError, self.test_function(u"\t\n\r truE\n\t\r "))
        self.assertRaises(ValueError, self.test_function(u"\t\n\r tRUE\n\t\r "))
        # 通过日志查看
        self.test_function(u"\t\ntrue")
        self.test_function(u"\ttrue\n")

    def test_parse_false(self):
        pass

    def test_parse_null(self):
        pass


if __name__ == '__main__':
    unittest.main()
