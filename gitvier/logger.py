import logging
import sys

LOGGER_NAME = 'gitvier'


class InfoFilter(logging.Filter):
    """
    Filter for logging which only allows DEBUG and INFO to go through. We use this
    to allow us to best split the logging where WARN and above are on sys.stderr and
    INFO and below are on sys.stdout.
    """
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


def configure_logging(verbosity: int = 0) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    debug_format = "%(asctime)s [%(levelname)-7.7s] [%(module)s %(levelno)s]  %(message)s"
    info_format = "%(asctime)s [%(levelname)-7.7s] %(message)s"
    warn_format = "%(levelname)s: %(message)s"
    error_format = "%(message)s"

    stdout = logging.StreamHandler(sys.stdout)
    stdout.addFilter(InfoFilter())
    stdout.setLevel(logging.INFO)

    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.WARNING)

    log_format = logging.Formatter(fmt=error_format, datefmt="%Y-%m-%d %H:%M:%S")
    if verbosity == -1:
        stderr.setLevel(logging.ERROR)
    elif verbosity == 0:
        log_format = logging.Formatter(fmt=warn_format, datefmt="%Y-%m-%d %H:%M:%S")
    elif verbosity == 1:
        log_format = logging.Formatter(fmt=info_format, datefmt="%Y-%m-%d %H:%M:%S")
    elif verbosity >= 2:
        stdout.setLevel(logging.DEBUG)
        log_format = logging.Formatter(fmt=debug_format, datefmt="%Y-%m-%d %H:%M:%S")

    stdout.setFormatter(log_format)
    stderr.setFormatter(log_format)
    logger.addHandler(stderr)
    if verbosity > 0:
        logger.addHandler(stdout)

    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)
