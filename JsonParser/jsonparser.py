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
        self.json_string = ""
        self.PARSE_OK = 0
        self.PARSE_INVALID_VALUE = 1
        self.logger = JsonParseLogger()
        self.valid_number_symbol_front = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')
        self.valid_number_symbol_behind = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', 'E', 'e', '.')
        self.float_symbol = ('e', 'E', '.')
        self.error_message = ""

    def __json_parse_true(self, json_string):
        if json_string[:4] != u'true':
            self.error_message = "首字母t的字面量是却不是true"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        else:
            if len(json_string) < 4:
                self.error_message = "字面值不足true的长度"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, True

    def __json_parse_false(self, json_string):
        if json_string[:5] != u'false':
            self.error_message = "首字母f是却不是false"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        else:
            if len(json_string) < 5:
                self.error_message = "字面值不足false的长度"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            json_string = json_string[5:]
            return self.PARSE_OK, json_string, False

    def __json_parse_null(self, json_string):
        if json_string[:4] != u'null':
            self.error_message = "首字母n是却不是null"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        else:
            if len(json_string) < 4:
                self.error_message = "字面值不足null的长度"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            json_string = json_string[4:]
            return self.PARSE_OK, json_string, None

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
            self.error_message = "json不支持'num.类型'"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        elif json_string[index] in self.valid_number_symbol_behind:
            index += 1
        if isfloat_flag:
            try:
                # 超过浮点数上限直接用inf表示，不抛出异常
                value = float(json_string[:index])
            except ValueError:
                self.error_message = "float转换错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
        else:
            try:
                value = int(json_string[:index])
            except ValueError:
                self.error_message = "int转换错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
        if value == (float('inf') or float('-inf')):
            value = u'Infinity'
        json_string = json_string[index:]
        return self.PARSE_OK, json_string, value

    def __json_parse_string(self, json_string):
        is_valid_string = False
        valid_escape_symbol = ('"', '\\', '/', 'b', 'f', 'n', 'r', 't')
        index = 0
        string_len = len(json_string)
        # 寻找第二个引号(能进到这个函数说明第一个引号就在第一个位置)，即找到字符串的结尾位置
        for index in range(1, string_len):
            if json_string[index] == '"' and json_string[index-1] != '\\':
                is_valid_string = True
                break
            elif json_string[index] == '\\':
                if json_string[index+1] == 'u':
                    if string_len - index < 6:
                        self.error_message = "字符串不符合\uxxxx格式"
                        self.logger.error(self.json_string, self.error_message)
                        raise ValueError(self.error_message)
                    else:
                        json_string_copy = json_string[:index]
                        json_string_copy += json_string[index:index+6].decode()
                        json_string = json_string_copy + json_string[index+6:]
                        # json_string[index+4:] = json_string[index+6:]
                    index += 5
                elif json_string[index+1] in valid_escape_symbol:
                    index += 1
                else:
                    continue

        if is_valid_string is True:
            value = json_string[:index+1]
            json_string = json_string[index+1:]
            return self.PARSE_OK, json_string, value
        else:
            self.error_message = "传递非法值"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)

    def __json_parse_array(self, json_string):
        if json_string == '':
            self.error_message = "找不到下一个]"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)

        array_to_parse = []
        json_string = json_string[1:].strip()
        if json_string[0] == ']':
            json_string = json_string[1:]
            return self.PARSE_OK, json_string, array_to_parse
        while True:
            json_return_status, json_string, value = self.__json_parse_value(json_string)
            if json_string == '':
                self.error_message = "找不到下一个]"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            array_to_parse.append(value)
            json_string = json_string.strip()
            if json_string[0] == ',':
                json_string = json_string[1:].strip()
            elif json_string[0] == ']':
                json_string = json_string[1:]
                return self.PARSE_OK, json_string, array_to_parse
            else:
                self.error_message = "解析数组时出现错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)

    def __json_parse_object(self, json_string):
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
                self.error_message = "找不到下一个}"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            if side_flag is True:
                if not isinstance(value, unicode):
                    self.error_message = "key值不是字符串"
                    self.logger.error(self.json_string, self.error_message)
                    raise ValueError(self.error_message)
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
                self.error_message = "解析对象时出现错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)

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
            self.error_message = "不认识的开头"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)

    def __json_dump_array(self, json_string, array):
        json_string += "["
        for elem in array:
            if isinstance(elem, dict):
                json_string = self.__json_dump_object(json_string, elem)
            elif isinstance(elem, list):
                json_string = self.__json_dump_array(json_string, elem)
            elif isinstance(elem, unicode):
                json_string += elem
            elif isinstance(elem, bool):
                if elem is True:
                    json_string += 'true'
                else:
                    json_string += 'false'
            elif elem is None:
                json_string += 'null'
            elif isinstance(elem, float) or isinstance(elem, int):
                json_string += str(elem)
            else:
                self.error_message = "__json_dump_array发生错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            if elem != array[-1]:
                json_string += ', '
        json_string += ']'
        return json_string

    # 对象转字符串
    def __json_dump_object(self, json_string, json_object):
        json_string += '{'
        counter = len(json_object)
        if counter is 0:
            json_string += '}'
            return json_string
        for elem in json_object:
            counter = counter - 1
            json_string += "{}{}".format(elem, ": ")
            if isinstance(json_object[elem], list):
                json_string = self.__json_dump_array(json_string, json_object[elem])
            elif isinstance(json_object[elem], dict):
                json_string = self.__json_dump_object(json_string, json_object[elem])
            elif isinstance(json_object[elem], unicode):
                json_string += json_object[elem]
            elif isinstance(json_object[elem], bool):
                    if json_object[elem] is True:
                        json_string += 'true'
                    else:
                        json_string += 'false'
            elif json_object[elem] is None:
                json_string += 'null'
            # 不能放在True False前面，可能会吧True判断为int类型
            elif isinstance(json_object[elem], float) or isinstance(json_object[elem], int):
                json_string += str(json_object[elem])
            else:
                self.error_message = "__json_dump_object发生错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            if counter == 0:
                json_string += "}"
            else:
                json_string += ", "
        return json_string

    def loads(self, json_string):
        """
        :param json_string: JSON格式数据，S为一个JSON字符串
        :return: 无返回值
        若遇到JSON格式错误的应该抛异常，JSON中数据如果超过
        Python里的浮点数上限的，也抛出异常。JSON的最外层假定为Object
        """
        # 确保输入为str或unicode类型，然后转换为unicode类型
        if not isinstance(json_string, (str, unicode)):
            self.error_message = "输入类型应该为字符串或Unicode类型"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        elif isinstance(json_string, str):
            json_string = json_string.decode()
        json_string_copy = ""
        self.json_string = ""
        for element in json_string:
            self.json_string += element
            json_string_copy += element
        json_string_copy = json_string_copy.strip()
        parse_status, json_string_copy, value = self.__json_parse_value(json_string_copy)
        self.logger.debug(self.json_string, value)
        self._data = value

    def dumps(self):
        """
        :return: JSON格式内容
        将实例中的内容转成JSON格式返回
        """
        json_string = '{'
        counter = len(self._data)
        if counter == 0:
            json_string += '}'
            return json_string
        for elem in self._data.items():
            counter -= 1
            json_string += '{}{}'.format(elem[0].decode(), ': ')
            if isinstance(elem[1], list):
                json_string = self.__json_dump_array(json_string, elem[1])
            elif isinstance(elem[1], dict):
                json_string = self.__json_dump_object(json_string, elem[1])
            elif isinstance(elem[1], unicode):
                json_string += elem[1]
            elif isinstance(elem[1], bool):
                if elem[1] is True:
                    json_string += 'true'
                else:
                    json_string += 'false'
            elif elem[1] is None:
                json_string += 'null'
            elif isinstance(elem[1], float) or isinstance(elem[1], int):
                json_string += str(elem[1])
            if counter == 0:
                json_string += '}'
            else:
                json_string += ', '
        return json_string

    def load_file(self, f):
        """
        :param f: 待读取的文本路径
        :return: 无返回值
        从文件中读取JSON格式数据
        文件操作失败抛出异常，异常处理和loads函数相同
        """
        with open(f, 'r') as json_file:
            json_text = json_file.read()
        self.loads(json_text)

    def dump_file(self, f):
        """
        :param f:待保存的文件路径
        :return: 无返回值
        将实例中的内容以JSON格式存入文件，
        文件若存在则覆盖，
        文件操作失败抛出异常
        """
        with open(f, 'w') as json_file:
            json_file.write(self.dumps())

    def load_dict(self, d):
        """
        :param d: Python字典数据
        :return: 无返回值
        将dict中读取数据存入实例中，若遇到不是字符串的key则忽略
        """
        for elem in d:
            if isinstance(elem, (str, unicode)):
                self._data[elem] = d[elem]

    def dump_dict(self):
        """
        :return: 字典，包含实例中的内容
        返回一个字典，包含实例中的内容
        """
        new_data = dict.copy(self._data)
        return new_data

    def __getitem__(self, item):
        """
        :param item: 键值item
        :return: 键值为item的value值
        获取self._data[iter]
        """
        return self._data[item]

    def __setitem__(self, key, value):
        """
        :param key: 键值key
        :param value: 键值key对应的value值
        :return: 无返回值
        给字典添加键值为key的值value
        """
        self._data[key] = value

    def update(self, d):
        """
        :param d: 新加入字典数据
        :return: 无返回值
        用字典d更新实例中的数据，类似于字典的update
        """
        for key in d:
            if key not in self._data:
                self._data[key] = d[key]
