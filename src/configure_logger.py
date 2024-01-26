import logging


def configure_logger(log_path: str) -> logging.Logger:

    logger = logging.getLogger("configure_logger")

    logger.setLevel(logging.DEBUG)
    # logger.propagate = False 

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    return logger
