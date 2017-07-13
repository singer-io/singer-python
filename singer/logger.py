import logging
import logging.config
import os


def get_logger(name=None):
    """Return a Logger instance appropriate for using in a Tap or a Target."""
    this_dir, _ = os.path.split(__file__)
    path = os.path.join(this_dir, 'logging.conf')
    logging.config.fileConfig(path)
    name = name or 'root'
    return logging.getLogger(name)
