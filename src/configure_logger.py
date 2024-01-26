import logging


def configure_logger(log_path: str) -> logging.Logger:

    """
    Configures and returns a logger with dual handlers: file and console.

    This function sets up a logging system with two handlers. The file handler logs
    error-level messages and above to a specified file, while the console handler
    outputs debug-level messages and above to the console. The logger uses a common
    formatter for both handlers, displaying the time, logger name, log level, and log message.

    Parameters:
    log_path (str): The path to the file where error-level logs will be saved.

    Returns:
    logging.Logger: The configured logger with file and console handlers.
    """

    logger = logging.getLogger("configure_logger")

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
