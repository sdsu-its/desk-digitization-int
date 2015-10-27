import logging
from logging.config import dictConfig

import os
import yaml

__author__ = 'tpaulus'


class Logging:
    logger_initialized = False

    def __init__(self):
        pass

    @staticmethod
    def setup_logging(
            default_path='logging_config.yaml',
            default_level=logging.WARN,
            env_key='LOG_CFG'):
        """
        Setup logging configuration

        """
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    @staticmethod
    def get_logger(name):
        """
        Get the Logger

        :return: Instance of Logger
        :rtype: logging
        """
        if not Logging.logger_initialized:
            Logging.setup_logging()
            Logging.logger_initialized = True
            logging.getLogger(__name__).debug('Logger Initialized')

        return logging.getLogger(name)
