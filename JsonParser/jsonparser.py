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
        self.valid_number_symbol_front = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')
        self.valid_number_symbol_behind = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', 'E', 'e', '.')
        self.float_symbol = ('e', 'E', '.')

    def __json_parse_true(self, json_string):
        if json_string[:4] != u'true':
            raise ValueError("首字母t是却不是true")
        else:
            if len(json_string) < 4:
                raise ValueError("字面值不足true的长度")
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, 'true'

    def __json_parse_false(self, json_string):
        if json_string[:5] != u'false':
            raise ValueError("首字母f是却不是false")
        else:
            if len(json_string) < 5:
                raise ValueError("字面值不足false的长度")
            json_string = json_string[5:]
            return self.PARSE_OK, json_string, 'false'

    def __json_parse_null(self, json_string):
        if json_string[:4] != u'null':
            raise ValueError("首字母n是却不是null")
        else:
            if len(json_string) < 4:
                raise ValueError("字面值不足null的长度")
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, 'null'

    def __json_parse_number(self, json_string):
        isfloat_flag = False

        index = 0
        for index, elem in enumerate(json_string):
            if elem in self.float_symbol:
                isfloat_flag = True
            if elem not in self.valid_number_symbol_behind:
                break
        # 最后跳出来可能是循环结束，也可能是break跳出
        # break跳出说明最后一位不是合法数字字符 循环自动结束说明
        # 最后一位是合法字符，这样跳出需要+1才能包含合法的最后一位
        # 并且最后一个字符不能是.
        if json_string[index] == '.':
            raise ValueError("json不支持'num.类型'")
        elif json_string[index] in self.valid_number_symbol_behind:
            index += 1
        if isfloat_flag:
            try:
                value = float(json_string[:index])
            except ValueError:
                raise ValueError("float转换错误")
        else:
            try:
                value = int(json_string[:index])
            except ValueError:
                raise ValueError("int转换错误")
        json_string = json_string[index:]
        return self.PARSE_OK, json_string, value

    def __json_parse_string(self, json_string):
        is_valid_string = False
        index = 0
        string_len = len(json_string)
        # 寻找第二个引号(能进到这个函数说明第一个引号就在第一个位置)，即找到字符串的结尾位置
        for index in range(1, string_len):
            if json_string[index] == '"':
                is_valid_string = True
                break
            elif json_string[index] == '\\':
                if json_string[index+1] == 'u':
                    if string_len - index < 6:
                        raise ValueError("字符串不符合\uxxxx格式")
                    else:
                        json_string_copy = json_string[:index]
                        json_string_copy += json_string[index:index+6].decode()
                        json_string = json_string_copy + json_string[index+6:]
                        # json_string[index+4:] = json_string[index+6:]
                    index += 5
                else:
                    index += 1
        if is_valid_string is True:
            value = json_string[:index+1]
            json_string = json_string[index+1:]
            return self.PARSE_OK, json_string, value
        else:
            raise ValueError("PARSE_INVALID_VALUE")

    def __json_parse_array(self, json_string):
        if json_string == '':
            raise ValueError("找不到下一个]")

        array_to_parse = []
        json_string = json_string[1:].strip()
        if json_string[0] == ']':
            json_string = json_string[1:]
            return self.PARSE_OK, json_string, array_to_parse
        while True:
            json_return_status, json_string, value = self.__json_parse_value(json_string)
            if json_string == '':
                raise ValueError("找不到下一个]")
            array_to_parse.append(value)
            json_string = json_string.strip()
            if json_string[0] == ',':
                json_string = json_string[1:].strip()
            elif json_string[0] == ']':
                json_string = json_string[1:]
                return self.PARSE_OK, json_string, array_to_parse
            else:
                raise ValueError("解析数组时出现错误")
            
    def __json_parse_object(self, json_string):
        dict_to_parse = {}
        dict_key = []
        dict_value = []
        side_flag = True
        json_string = json_string[1:].strip()
        if json_string[0] == '}':
            dict_to_parse = dict(zip(dict_key, dict_value))
            return self.PARSE_OK, json_string, dict_to_parse
        while True:
            json_return_status, json_string, value = self.__json_parse_value(json_string)
            if json_string == '':
                raise ValueError("找不到下一个}")
            if side_flag is True:
                dict_key.append(value)
            else:
                dict_value.append(value)
            json_string = json_string.strip()
            if json_string[0] == ':':
                side_flag = False
                json_string = json_string[1:].strip()
            elif json_string[0] == '}':
                json_string = json_string[1:]
                dict_to_parse = dict(zip(dict_key, dict_value))
                return self.PARSE_OK, json_string, dict_to_parse
            elif json_string[0] == ',':
                json_string = json_string[1:].strip()
                side_flag = True
            else:
                raise ValueError("解析对象时出现错误")



    def __json_parse_value(self, json_string):
        # 可能是null
        if json_string[0] == 'n':
            return self.__json_parse_null(json_string)
        # 可能是true
        elif json_string[0] == 't':
            return self.__json_parse_true(json_string)
        # 可能是false
        elif json_string[0] == 'f':
            return self.__json_parse_false(json_string)
        # 可能是数字
        elif json_string[0] in self.valid_number_symbol_front:
            return self.__json_parse_number(json_string)
        # 可能是字符串
        elif json_string[0] == '\"':
            return self.__json_parse_string(json_string)
        elif json_string[0] == '[':
            return self.__json_parse_array(json_string)
        elif json_string[0] == '{':
            return self.__json_parse_object(json_string)
        else:
            raise ValueError("不认识的开头")

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
        print json_string
        self.logger.debug("{}:{}".format(u"成功解析了字符串".encode('utf-8'), json_string.encode('utf-8')))
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
