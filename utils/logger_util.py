import logging
from config.configuration import CurrentConfig
from utils.system_util import make_directory_if_not_exists


def get_logger(name):

    logger = logging.getLogger(name)

    formatter = logging.Formatter('%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()

    for log_level in CurrentConfig.LOG_LEVELS:
        logger.setLevel(log_level)
        ch.setLevel(log_level)

    make_directory_if_not_exists(CurrentConfig.OUTPUT_FILES_FOLDER)

    ch.setFormatter(formatter)
    fh = logging.FileHandler(CurrentConfig.OUTPUT_FILES_FOLDER+f"{name}.log")

    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger