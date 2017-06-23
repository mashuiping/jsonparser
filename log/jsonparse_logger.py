# coding: utf-8
import logging


class JsonParseLogger(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='jsonparser.log',
                            filemode='a')

    @staticmethod
    def debug( message_to_log):
        logging.debug(message_to_log)

    @staticmethod
    def info(message_to_log):
        logging.debug(message_to_log)

    @staticmethod
    def warning(message_to_log):
        logging.warning(message_to_log)

    @staticmethod
    def error(message_to_log):
        logging.error(message_to_log)

    @staticmethod
    def critical(message_to_log):
        logging.critical(message_to_log)
