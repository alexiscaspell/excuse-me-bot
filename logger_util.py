import logging
from logging import INFO,ERROR,WARNING,DEBUG

LOG_LEVELS = [INFO,ERROR,WARNING,DEBUG]

def get_logger(name):

    logger = logging.getLogger(name)

    formatter = logging.Formatter('%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()

    for log_level in LOG_LEVELS:
        logger.setLevel(log_level)
        ch.setLevel(log_level)

    ch.setFormatter(formatter)
    fh = logging.FileHandler("./"+f"{name}.log")

    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger