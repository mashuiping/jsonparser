# coding: utf-8
import logging


class JsonParseLogger(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='jsonparser.log',
                            filemode='a')

    @staticmethod
    def debug(json_string, debug_message):
        logging.debug('{}解析成功,解析成：{}'.format(json_string,debug_message))

    @staticmethod
    def error(json_string, debug_message, line_number):
        logging.error('{}解析失败，原因：{},失败所在行号'.format(json_string,debug_message,line_number))

