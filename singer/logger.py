import logging
import logging.config
import os


def get_logger():
    """Return a Logger instance appropriate for using in a Tap or a Target."""
    this_dir, _ = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    return logging.getLogger()


def log_debug(msg, *args, **kwargs):
    get_logger().debug(msg, *args, **kwargs)


def log_info(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)


def log_warning(msg, *args, **kwargs):
    get_logger().warning(msg, *args, **kwargs)


def log_error(msg, *args, **kwargs):
    get_logger().error(msg, *args, **kwargs)


def log_critical(msg, *args, **kwargs):
    get_logger().critical(msg, *args, **kwargs)


def log_fatal(msg, *args, **kwargs):
    get_logger().fatal(msg, *args, **kwargs)


def log_exception(msg, *args, **kwargs):
    get_logger().exception(msg, *args, **kwargs)
