import logging
import logging.config
import os
from typing import Optional


class Logger:

    def __init__(self, config_file_path: Optional[str] = None, logger_name: Optional[str] = None):
        """
        Creates a Logger instance appropriate for using in a Tap or a Target.
        :param config_file_path: path to a custom logging file
        :param logger_name: custom name for logger
        """

        # fallback to singer's logging.conf if no file is given
        if not config_file_path:
            this_dir, _ = os.path.split(__file__)
            config_file_path = os.path.join(this_dir, 'logging.conf')

        # See
        # https://docs.python.org/3.5/library/logging.config.html#logging.config.fileConfig
        # for a discussion of why or why not to set disable_existing_loggers
        # to False. The long and short of it is that if you don't set it to
        # False it ruins external module's abilities to use the logging
        # facility.
        logging.config.fileConfig(config_file_path, disable_existing_loggers=False)

        # use current file name as logger name
        logger_name = __name__ if not logger_name else logger_name

        self.__logger = logging.getLogger(logger_name)

    def log_debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def log_info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def log_warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def log_error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def log_critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)

    def log_fatal(self, msg, *args, **kwargs):
        self.__logger.fatal(msg, *args, **kwargs)

    def log_exception(self, msg, *args, **kwargs):
        self.__logger.exception(msg, *args, **kwargs)

    def get_level(self):
        return self.__logger.level
