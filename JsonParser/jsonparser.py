# coding: utf-8
from log.jsonparse_logger import JsonParseLogger


class JsonParser(object):
    """
    基于Python2.7封装实现一个可重用的Json解析类

    该类能读取JSON格式的数据，并以Python字典的方式读取数据

    给定Python字典，可以更新类中数据，并以JSON格式输出

    遵循JSON格式定义确保相同的同构数据源彼此转换后数据仍然一致

    支持将数据以JSON格式存储到文件并加载回来使用

    """

    def __init__(self):
        self._data = {}
        self.PARSE_OK = 0
        self.PARSE_INVALID_VALUE = 1
        self.logger = JsonParseLogger()

    def __json_parse_true(self, json_string):
        if json_string != 'true':
            raise ValueError("首字母t是却不是true")
        else:
            if len(json_string) < 4:
                raise ValueError("字面值不足true的长度")
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, 'true'

    def __json_parse_false(self, json_string):
        if json_string != 'false':
            raise ValueError("首字母f是却不是false")
        else:
            if len(json_string) < 5:
                raise ValueError("字面值不足false的长度")
            json_string = json_string[5:]
            return self.PARSE_OK, json_string, 'false'

    def __json_parse_null(self, json_string):
        if json_string != 'null':
            raise ValueError("首字母n是却不是null")
        else:
            if len(json_string) < 4:
                raise ValueError("字面值不足null的长度")
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, 'null'

    def __json_parse_value(self, json_string):
        if json_string[0] == 'n':
            return self.__json_parse_null(json_string)
        elif json_string[0] == 't':
            return self.__json_parse_true(json_string)
        elif json_string[0] == 'f':
            return self.__json_parse_false(json_string)
        else:
            return self.PARSE_INVALID_VALUE, json_string, ""

    def loads(self, json_string):
        """
        :param json_string: JSON格式数据，S为一个JSON字符串
        :return: 无返回值
        若遇到JSON格式错误的应该抛异常，JSON中数据如果超过
        Python里的浮点数上限的，也抛出异常。JSON的最外层假定为Object
        """
        # 确保输入为str或unicode类型，然后转换为unicode类型
        if not isinstance(json_string, basestring):
            self.logger.error("输入类型应该为字符串或Unicode类型")
        elif isinstance(json_string, str):
            json_string = json_string.decode()
        json_string_copy = ""
        for element in json_string:
            json_string_copy += element
        json_string_copy = json_string_copy.strip()
        parse_status, json_string_copy, value = self.__json_parse_value(json_string_copy)
        self.logger.debug(parse_status)
        self._data = value


    def dumps(self):
        """
        :return: JSON格式内容
        将实例中的内容转成JSON格式返回
        """
        pass

    def load_file(self, f):
        """
        :param f: 待读取的文本路径
        :return: 无返回值
        从文件中读取JSON格式数据
        文件操作失败抛出异常，异常处理和loads函数相同
        """
        pass

    def dump_file(self, f):
        """
        :param f:待保存的文件路径
        :return: 无返回值
        将实例中的内容以JSON格式存入文件，
        文件若存在则覆盖，
        文件操作失败抛出异常
        """
        pass

    def load_dict(self, d):
        """
        :param d: Python字典数据
        :return: 无返回值
        将dict中读取数据存入实例中，若遇到不是字符串的key则忽略
        """

        pass

    def dump_dict(self):
        """
        :return: 字典，包含实例中的内容
        返回一个字典，包含实例中的内容
        """
        pass

    def __getitem__(self, item):
        """
        :param item: 键值item
        :return: 键值为item的value值
        获取self._data[iter]
        """

        pass

    def __setitem__(self, key, value):
        """
        :param key: 键值key
        :param value: 键值key对应的value值
        :return: 无返回值
        给字典添加键值为key的值value
        """
        pass

    def update(self,d):
        """
        :param d: 新加入字典数据
        :return: 无返回值
        用字典d更新实例中的数据，类似于字典的update
        """
        pass
