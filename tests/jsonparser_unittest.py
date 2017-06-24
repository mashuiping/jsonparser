# coding: utf-8
import unittest
# json库用于测试对比生成数据的正确性
import json
from JsonParser import jsonparser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.test_func_loads = jsonparser.JsonParser().loads
        self.test_func_dumps = jsonparser.JsonParser().dumps
        self.json_ok = [
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
           # ('{"\\"":"\\""}', 1),
        ]
        self.json_ok2 = [
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
        self.json_ex = [
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
#    def test_parse_true(self):
#        # 测试引发异常
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\r\rtRue\r\r")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\n\ntRUe\n\n")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r truE\n\t\r ")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r tRUE\n\t\r ")
#        # 没有错误没有异常抛出，通过日志查看
#        self.test_func_loads(u"\t\ntrue")
#        self.test_func_loads(u"\ttrue\n")
#
#    def test_parse_false(self):
#        # 测试引发异常
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\r\rfAlse\r\r")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\n\nfaLSe\n\n")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r fAlse\n\t\r ")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r fALSE\n\t\r ")
#        # 没有错误没有异常抛出，通过日志查看
#        self.test_func_loads(u"\t\nfalse")
#        self.test_func_loads(u"\tfalse\n")
#
#    def test_parse_null(self):
#        # 测试引发异常
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\r\rnuLl\r\r")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\n\nnUll\n\n")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r nUll\n\t\r ")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(u"\t\n\r nulL\n\t\r ")
#        # 没有错误没有异常抛出，通过日志查看
#        self.test_func_loads(u"\t\nnull")
#        self.test_func_loads(u"\tnull\n")
#
#    def test_parse_number(self):
#        # 能通过测试的样例
#        self.test_func_loads("0.0")
#        self.test_func_loads("0.0")
#        self.test_func_loads("-0.0")
#        self.test_func_loads("1")
#        self.test_func_loads("1.5")
#        self.test_func_loads("-1.5")
#        self.test_func_loads("3.1415")
#        self.test_func_loads("1E10")
#        self.test_func_loads("1e10")
#        self.test_func_loads("1E+10")
#        self.test_func_loads("1E-10")
#        self.test_func_loads("-1E10")
#        self.test_func_loads("-1E-10")
#        self.test_func_loads("1.234E+10")
#        self.test_func_loads("1e-10000")
#
#        # 测试不能通过样例
#        with self.assertRaises(ValueError):
#            self.test_func_loads("+0")
#        with self.assertRaises(ValueError):
#            self.test_func_loads("+1")
#        with self.assertRaises(ValueError):
#            self.test_func_loads(".123")
#        with self.assertRaises(ValueError):
#            self.test_func_loads("1.")
#        with self.assertRaises(ValueError):
#            self.test_func_loads("INF")
#        with self.assertRaises(ValueError):
#            self.test_func_loads("inf")
#        with self.assertRaises(ValueError):
#            self.test_func_loads("NAN")
#
#    def test_parse_string(self):
#        # 能通过测试的样例
#        self.test_func_loads('""')
#        self.test_func_loads('"a"')
#        self.test_func_loads('"a:"')
#        self.test_func_loads('"\\t\\n"')
#        # 会引发异常的测试
#        with self.assertRaises(ValueError):
#            self.test_func_loads('"\uxx"')
#
#    def test_parse_array(self):
#        # 能通过测试的样例
#        self.test_func_loads("[]")
#        self.test_func_loads("[1,2,3]")
#        self.test_func_loads("[   3,   4  ,  3]")
#       # 会引发异常的样例
#        with self.assertRaises(ValueError):
#            self.test_func_loads("[1, 5, 3")
#
#    def test_object(self):
#        # 能通过测试的样例
#        self.test_func_loads('{"":""}')
#        self.test_func_loads('{"a":true}')
#        self.test_func_loads('{"a" :[]}')
#        self.test_func_loads('{"a": false}')
#        self.test_func_loads('{"a" : 123}')
#        self.test_func_loads('{"a": "{ab" }')
#        self.test_func_loads('{"a":"cc"}')
#        self.test_func_loads('{"a":[1,2,[3]]}')
#        self.test_func_loads('{"a": {"a": {"a": [1,2,[3]]}}}')
#        self.test_func_loads('{"a":1e-1}')
#        # 会引发异常的样例
#        with self.assertRaises(ValueError):
#            self.test_func_loads('{"a":"\\"}')
#            self.test_func_loads('{"a", [}')
#            self.test_func_loads('{"a", True')
#            self.test_func_loads("{'a':1}")
#
#    def test_loads(self):

#        # 测试json_ok
        test_counter = 0
#        for elem in self.json_ok:
#            for index in range(0, elem[1]):
#                test_counter += 1
#                self.test_func_loads(elem[0])
#        # 测试json_ok2
#        for elem in self.json_ok2:
#            for index in range(0, elem[1]):
#                test_counter += 1
#                self.test_func_loads(elem[0])
#        # 测试json_ex
#        for elem in self.json_ex:
#            for index in range(0, elem[1]):
#                test_counter += 1
#                with self.assertRaises(ValueError):
#                    self.test_func_loads(elem[0])

    def test_dumps(self):
        # 能通过测试的样例
        my_jsonparser = jsonparser.JsonParser()
        for elem in self.json_ok:
            for index in range(0, elem[1]):
                my_jsonparser.loads(elem[0])
                self.assertEqual(my_jsonparser.dumps(), json.dumps(json.loads(elem[0])))
        for elem in self.json_ok2:
            for index in range(0, elem[1]):
                my_jsonparser.loads(elem[0])
                self.assertEqual(my_jsonparser.dumps(), json.dumps(json.loads(elem[0])))
        # 会引发异常的样例

if __name__ == '__main__':
    unittest.main()
