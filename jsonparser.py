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
        # 字典格式保存json数据
        self._data = {}
        # 对输入字符串的深拷贝
        self.json_string = ""
        # 转换成功
        self.PARSE_OK = 0
        # 转换失败
        self.PARSE_INVALID_VALUE = 1
        # JsonParserLogger类实例
        self.logger = JsonParseLogger()
        # 合法的数字开头标志
        self.valid_number_symbol_front = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')
        # 合法的数字尾部标志,不一定是最后一个字符
        self.valid_number_symbol_behind = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', 'E', 'e', '.')
        # 浮点数标志
        self.float_symbol = ('e', 'E', '.')
        # 出错时的具体信息
        self.error_message = ""
        # 设置栈，找出括号匹配不合法字符串
        self.stack = []

    def __json_parse_true(self, json_string):
        """
        :param json_string: 当前json类型字符串
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取字面值true
        """
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
        """
        :param json_string: 当前json类型字符串
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取字面值false
        """
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
        """
        :param json_string: 当前json类型字符串
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取字面值null
        """
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
        """
        :param json_string: 当前字符串的值
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取数字值
        """
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

        json_string = json_string[index:]
        return self.PARSE_OK, json_string, value

    def __json_parse_string(self, json_string):
        """
        :param json_string: 当前字符串的值
        :return: 返回转换状态，当前json类型字符串，提取到的值
        """
        string_len = len(json_string)
        index = 1
        value = u''

        while index < string_len:

            if json_string[index] == '"':
                break

            elif json_string[index] == '\\':
                if json_string[index+1] == u't':
                    value += '\t'
                elif json_string[index+1] == '\"':
                    value += '\"'
                elif json_string[index+1] == '\\':
                    value += '\\'
                elif json_string[index+1] == '\/':
                    value += '\/'
                elif json_string[index+1] == '\b':
                    value += '\b'
                elif json_string[index+1] == '\f':
                    value += '\f'
                elif json_string[index+1] == u'n':
                    value += '\n'
                elif json_string[index+1] == '\r':
                    value += '\r'
                elif json_string[index+1] == 'u':
                    if string_len - index < 6:
                        self.error_message = "字符串不符合\uxxxx格式"
                        self.logger.error(self.json_string, self.error_message)
                        raise ValueError(self.error_message)
                    else:
                        try:
                            value += json_string[index:index+6].decode('unicode-escape')
                        except UnicodeDecodeError:
                            raise UnicodeDecodeError("字符串解码错误")
                        index += 6
                        continue
                else:
                    raise ValueError(self.error_message)

                index += 2
                continue
            else:
                value += json_string[index]

            index += 1

        return self.PARSE_OK, json_string[index+1:], value

    def __json_parse_array(self, json_string):
        """
        :param json_string: 当前字符串的值
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取json数组值.
        解析思路：
            数组中存储的值可能是所有类型，用逗号分隔，
            运用状态机的思想，当解析到某一种类型的时候，把字符串交给解析
            那种类型的方法解析，然后返回结果。
        """
        if json_string == '':
            self.error_message = "找不到下一个]"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)

        array_to_parse = []
        json_string = json_string[1:].strip()
        if json_string[0] == ']':
            if len(self.stack) is 0 or self.stack.pop() != '[':
                self.error_message = "[]括号不匹配"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
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
                if len(self.stack)is 0 or self.stack.pop() != '[':
                    self.error_message = "[]括号不匹配"
                    self.logger.error(self.json_string, self.error_message)
                    raise ValueError(self.error_message)
                json_string = json_string[1:]
                return self.PARSE_OK, json_string, array_to_parse
            else:
                self.error_message = "解析数组时出现错误"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)

    def __json_parse_object(self, json_string):
        """
        :param json_string: 当前字符串的值
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取json对象值.
        解析思路：
            由于对象是key:value形式, 可以建立一个key列表，一个value列表
            分别存储后合成一个对象。
            此时，key必然是字符串类型，但是value的类型可以是全部的6种类型
            运用状态机的思想，当解析到某一种类型的时候，把字符串交给解析
            那种类型的方法解析，然后返回结果。
        """

        dict_key = []
        dict_value = []
        side_flag = True
        json_string = json_string[1:].strip()
        if json_string[0] == '}':
            if len(self.stack) is 0 or self.stack.pop() != '{':
                self.error_message = "{}括号不匹配"
                self.logger.error(self.json_string, self.error_message)
                raise ValueError(self.error_message)
            dict_to_parse = dict(zip(dict_key, dict_value))
            return self.PARSE_OK, json_string[1:], dict_to_parse
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
                if len(self.stack) is 0 or self.stack.pop() != '{':
                    self.error_message = "{}括号不匹配"
                    self.logger.error(self.json_string, self.error_message)
                    raise ValueError(self.error_message)
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
        """
        :param json_string: 当前字符串的值
        :return: 返回转换状态，当前json类型字符串，提取到的值
        解析并提取json所有可能对象的值.
        解析思路：
            根据字符串的第一个非空符号可以唯一确定是哪一种数据类型
            不能确定视为非法字符
        """
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
            self.stack.append('[')
            return self.__json_parse_array(json_string)
        elif json_string[0] == '{':
            self.stack.append('{')
            return self.__json_parse_object(json_string)
        else:
            self.error_message = "不认识的开头"
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)

    def __json_dump_array(self, json_string, array):
        """
        :param json_string: 当前字符串值
        :param array: 要转化成字符串的数组
        :return: 加入数组后json字符串的值
        """
        json_string += "["
        for elem in array:
            if isinstance(elem, dict):
                json_string = self.__json_dump_object(json_string, elem)
            elif isinstance(elem, list):
                json_string = self.__json_dump_array(json_string, elem)
            elif isinstance(elem, unicode):
                json_string = self.__json_dump_string(json_string, elem)
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

    def __json_dump_object(self, json_string, json_object):
        """
        :param json_string: 当前字符串的值
        :param json_object: 要转换的对象值
        :return: 加入转换后对象后json字符串的值
        """
        json_string += '{'
        counter = len(json_object)
        if counter is 0:
            json_string += '}'
            return json_string
        for elem in json_object:
            counter = counter - 1
            json_string += "{}{}{}{}".format("\"", elem, "\"", ": ")
            if isinstance(json_object[elem], list):
                json_string = self.__json_dump_array(json_string, json_object[elem])
            elif isinstance(json_object[elem], dict):
                json_string = self.__json_dump_object(json_string, json_object[elem])
            elif isinstance(json_object[elem], unicode):
                json_string = self.__json_dump_string(json_string, elem)
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
        # 初始化loads函数
        self._data = {}
        self.stack = []
        if not isinstance(json_string, (str, unicode)):
            error_message = "输入类型应该为字符串或Unicode类型"
            self.logger.error(json_string, error_message)
            raise ValueError(self.error_message)
        elif isinstance(json_string, str):
            json_string = json_string.decode()
        json_string_copy = ""
        for element in json_string:
            json_string_copy += element
        json_string_copy = json_string_copy.strip()
        parse_status, json_string_copy, value = self.__json_parse_value(json_string_copy)
        if len(self.stack) is not 0:
            self.error_message = "括号{}不匹配".format(self.stack.pop())
            self.logger.error(self.json_string, self.error_message)
            raise ValueError(self.error_message)
        self.logger.debug(json_string, value)
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
            json_string = self.__json_dump_string(json_string, elem[0]) + u": "
            if isinstance(elem[1], list):
                self.stack.append('[')
                json_string = self.__json_dump_array(json_string, elem[1])
            elif isinstance(elem[1], dict):
                self.stack.append('{')
                json_string = self.__json_dump_object(json_string, elem[1])
            elif isinstance(elem[1], (unicode, str)):
                json_string = self.__json_dump_string(json_string, elem[1])
            elif isinstance(elem[1], bool):
                if elem[1] is True:
                    json_string += 'true'
                else:
                    json_string += 'false'
            elif elem[1] is None:
                json_string += 'null'
            elif isinstance(elem[1], float) or isinstance(elem[1], int):
                if elem[1] == float('inf'):
                    json_string += 'Infinity'
                else:
                    json_string += str(elem[1])
            if counter == 0:
                json_string += '}'
            else:
                json_string += ', '
        return json_string

    def __json_dump_string(self, json_string, string):
        json_string_copy = u"{}{}".format(json_string, u"\"")
        for index, elem in enumerate(string):
            elem = elem.encode('unicode-escape')
            if elem == '\t':
                json_string_copy += '\\t'
            elif elem == '\n':
                json_string_copy += '\\n'
            elif elem == '\\':
                json_string_copy += '\\\\'
            elif elem == '\"':
                json_string_copy += '\\\"'
            elif elem == '\b':
                json_string_copy += '\\\b'
            elif elem == '\f':
                json_string_copy += '\\\f'
            elif elem == '\r':
                json_string_copy += '\\\r'
            else:
                json_string_copy += elem

        json_string_copy = u"{}{}".format(json_string_copy, u"\"")
        return json_string_copy


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
        return self.deepcopy_value(self._data)

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
        self._data[key] = self.deepcopy_value(value)

    def update(self, d):
        """
        :param d: 新加入字典数据
        :return: 无返回值
        用字典d更新实例中的数据，类似于字典的update
        """
        for key in d:
            if key not in self._data:
                self._data[key] = self.deepcopy_value(d[key])

    # 以下实现深拷贝
    def deepcopy_array(self, array):
        return [self.deepcopy_value(elem) for elem in array]

    def deepcopy_object(self, object):
        ret = {}
        for elem in object:
            ret[elem] = self.deepcopy_value(object[elem])
        return ret

    def deepcopy_value(self, value):
        if isinstance(value, dict):
            return self.deepcopy_object(value)
        elif isinstance(value, list):
            return self.deepcopy_array(value)
        else:
            return value
