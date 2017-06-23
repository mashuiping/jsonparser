# coding: utf-8
import logging


class JsonParseLogger(object):
    def __init__(self, message_to_log):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='jsonparser.log',
                            filemode='w')
        logging.debug(message_to_log)
        logging.info(message_to_log)
        logging.warning(message_to_log)
        logging.error(message_to_log)
        logging.critical(message_to_log)
