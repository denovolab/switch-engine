from io import StringIO
from configparser import ConfigParser
import logging

class Helper():
    @classmethod
    def get_configurations(cls, config_path):
        config = ConfigParser()
        config.read(config_path,encoding="utf-8")
        return config


    @classmethod
    def create_logger(cls, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        return logger
