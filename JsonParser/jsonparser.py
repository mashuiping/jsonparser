# coding: utf-8


class JsonParser(object):
    """
    基于Python2.7封装实现一个可重用的Json解析类

    该类能读取JSON格式的数据，并以Python字典的方式读取数据

    给定Python字典，可以更新类中数据，并以JSON格式输出

    遵循JSON格式定义确保相同的同构数据源彼此转换后数据仍然一致

    支持将数据以JSON格式存储到文件并加载回来使用
    """

    def __init__(self):
        """
        添加函数
        """
        self._data = {}

    def loads(self, s):
        pass

    def dumps(self):
        pass

    def load_file(self, f):
        pass

    def dump_file(self, f):
        pass

    def load_dict(self, d):
        pass

    def dump_dict(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def update(self,d):
        pass
