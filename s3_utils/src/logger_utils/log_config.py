"""Logger config to be used for logging across the system modules."""
import logging
import os
import sys

from immutabledict import immutabledict

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Refer to this page: https://docs.python.org/3/library/logging.html to understand various logging levels in python
LOG_LEVEL_MAP: immutabledict[str, int] = immutabledict({
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
})


def config_root_logger() -> logging.Logger:
    """
    Configure root logger_utils to be used across the system modules. Adds a handler to write logs to stdout also and also
    a formatter for better readability of logs.
    :return: Logger object set with environment variable provided log level and with a stdout handler added.
    """
    log_level = LOG_LEVEL_MAP[LOG_LEVEL]
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    # With the following formatter, an example log would appear as below:
    # [2020-11-02 20:42:17,483] root p61594 {<module_name>:<line_number>} INFO - <log_message_content>
    formatter = logging.Formatter(
        "[%(asctime)s] %(name)s %(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    return root_logger


logger = config_root_logger()
