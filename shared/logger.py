# logger.py
"""
each service will have its logger in main.py
each logger will be in the depencencyInjectore in the constructor
this is instead of using prints
    in main.py
    - will create its logger
    - level of log from env
    - passes to all components in creation
    each object 
    - will use the logger for (INFO) & (ERRORS)
"""


import logging
import sys
from pathlib import Path


def get_logger(
    name: str = __name__,
    level: int = logging.DEBUG,
    log_file: str | None = None,
) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # console
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # file (optional)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger