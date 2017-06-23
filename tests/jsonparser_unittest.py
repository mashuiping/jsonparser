import unittest
from JsonParser import jsonparser


class MyTestCase(unittest.TestCase):
    def setUp(self):

        self.test_function = jsonparser.JsonParser.loads

    def test_parse_space(self):



    def test_invalid_space(self):
        pass

    def test_parse_true(self):

    def test_invalid_true(self):
        pass

    def test_parse_false(self):
        pass

    def test_invalid_false(self):
        pass

    def test_parse_null(self):
        pass


if __name__ == '__main__':
    unittest.main()
