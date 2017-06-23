# coding: utf-8
import unittest
from JsonParser import jsonparser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_function = jsonparser.JsonParser().loads

    def test_parse_true(self):
        # 测试引发异常
        with self.assertRaises(ValueError):
            self.test_function(u"\r\rtRue\r\r")
        with self.assertRaises(ValueError):
            self.test_function(u"\n\ntRUe\n\n")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r truE\n\t\r ")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r tRUE\n\t\r ")
        # 没有错误没有异常抛出，通过日志查看
        self.test_function(u"\t\ntrue")
        self.test_function(u"\ttrue\n")

    def test_parse_false(self):
        # 测试引发异常
        with self.assertRaises(ValueError):
            self.test_function(u"\r\rfAlse\r\r")
        with self.assertRaises(ValueError):
            self.test_function(u"\n\nfaLSe\n\n")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r fAlse\n\t\r ")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r fALSE\n\t\r ")
        # 没有错误没有异常抛出，通过日志查看
        self.test_function(u"\t\nfalse")
        self.test_function(u"\tfalse\n")

    def test_parse_null(self):
        # 测试引发异常
        with self.assertRaises(ValueError):
            self.test_function(u"\r\rnuLl\r\r")
        with self.assertRaises(ValueError):
            self.test_function(u"\n\nnUll\n\n")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r nUll\n\t\r ")
        with self.assertRaises(ValueError):
            self.test_function(u"\t\n\r nulL\n\t\r ")
        # 没有错误没有异常抛出，通过日志查看
        self.test_function(u"\t\nnull")
        self.test_function(u"\tnull\n")

    def test_parse_number(self):
        # 能通过测试的样例
        self.test_function("0.0")
        self.test_function("0.0")
        self.test_function("-0.0")
        self.test_function("1")
        self.test_function("1.5")
        self.test_function("-1.5")
        self.test_function("3.1415")
        self.test_function("1E10")
        self.test_function("1e10")
        self.test_function("1E+10")
        self.test_function("1E-10")
        self.test_function("-1E10")
        self.test_function("-1E-10")
        self.test_function("1.234E+10")
        self.test_function("1e-10000")

        # 测试不能通过样例
        with self.assertRaises(ValueError):
            self.test_function("+0")
        with self.assertRaises(ValueError):
            self.test_function("+1")
        with self.assertRaises(ValueError):
            self.test_function(".123")
        with self.assertRaises(ValueError):
            self.test_function("1.")
        with self.assertRaises(ValueError):
            self.test_function("INF")
        with self.assertRaises(ValueError):
            self.test_function("inf")
        with self.assertRaises(ValueError):
            self.test_function("NAN")

    def test_parse_string(self):
        # 能通过测试的样例
        self.test_function('""')
        self.test_function('"a"')
        self.test_function('"a:"')
        self.test_function('"\\t\\n"')
        # 会引发异常的测试
        with self.assertRaises(ValueError):
            self.test_function('"\uxx"')

    def test_parse_array(self):
        # 能通过测试的样例
        self.test_function("[]")
        self.test_function("[1,2,3]")
        self.test_function("[   3,   4  ,  3]")
       # 会引发异常的样例
        with self.assertRaises(ValueError):
            self.test_function("[1, 5, 3")

    def test_object(self):
        # 能通过测试的样例
        self.test_function('{"":""}')
        self.test_function('{"a":true}')
        self.test_function('{"a" :[]}')
        self.test_function('{"a": false}')
        self.test_function('{"a" : 123}')
        self.test_function('{"a": "{ab" }')
        self.test_function('{"a":"cc"}')
        self.test_function('{"a":[1,2,[3]]}')
        self.test_function('{"a": {"a": {"a": [1,2,[3]]}}}')
        self.test_function('{"a":1e-1}')
        # 会引发异常的样例
        with self.assertRaises(ValueError):
            self.test_function('{"a":"\\"}')
            self.test_function('{"a", [}')
            self.test_function('{"a", True')
            self.test_function("{'a':1}")

    def test_loads(self):
        json_ok = [
            ('{}', 1),
            ('{"":""}', 1),
            ('{"a":123}', 1),
            ('{"a":-123}', 1),
            ('{"a":1.23}', 1),
            ('{"a":1e1}', 1),
            ('{"a":true,"b":false}', 1),
            ('{"a":null}', 1),
            ('{"a":[]}', 1),
            ('{"a":{}}', 1),
            (' {"a:": 123}', 1),
            ('{ "a  " : 123}', 1),
            ('{ "a" : 123    	}', 1),
            ('{"true": "null"}', 1),
            ('{"":"\\t\\n"}', 1),
            ('{"\\"":"\\""}', 1),
        ]
        json_ok2 = [
            ('{"a":' + '1' * 310 + '.0' + '}', 2),
            ('{"a":"abcde,:-+{}[]"}', 2),
            ('{"a": [1,2,"abc"]}', 2),
            ('{"d{": "}dd", "a":123}', 2),
            ('{"a": {"a": {"a": 123}}}', 2),
            ('{"a": {"a": {"a": [1,2,[3]]}}}', 2),
            ('{"a": "\\u7f51\\u6613CC\\"\'"}', 3),

            ('{"a":1e-1, "cc": -123.4}', 2),
            # ('{ "{ab" : "}123", "\\\\a[": "]\\\\"}', 3),
        ]
        json_ex = [
            # exceptions
            ('{"a":[}', 2),
            ('{"a":"}', 2),

            ('{"a":True}', 1),
            ('{"a":Null}', 1),
            ('{"a":foobar}', 2),
            ("{'a':1}", 3),
            ('{1:1}', 2),
            ('{true:1}', 2),
            # ('{"a":{}', 2),
            ('{"a":-}', 1),
            ('{"a":[,]}', 2),
            ('{"a":.1}', 1),
            ('{"a":+123}', 1),
            ('{"a":1..1}', 1),
            ('{"a":--1}', 1),
            ('{"a":"""}', 1),
            ('{"a":"\\"}', 1),
        ]
        # 测试json_ok
        test_counter = 0
        for elem in json_ok:
            for index in range(0, elem[1]):
                test_counter += 1
                self.test_function(elem[0])
        # 测试json_ok2
        for elem in json_ok2:
            for index in range(0, elem[1]):
                test_counter += 1
                self.test_function(elem[0])
        # 测试json_ex
        for elem in json_ex:
            for index in range(0, elem[1]):
                test_counter += 1
                with self.assertRaises(ValueError):
                    self.test_function(elem[0])

if __name__ == '__main__':
    unittest.main()
