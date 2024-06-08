import logging
from datetime import datetime, timedelta
import os


def configure_logger() -> logging.Logger:
    """
    Configures and returns a logger with dual handlers: file and console.

    This function sets up a logging system tailored to log error-level messages
    and above in a file, and debug-level messages and above in the console.
    The file for error-level logging is named based on the current date and time,
    formatted as 'YYYY-MM-DD HH:00-HH+1:00.log', and stored in the 'logs' directory.
    Both handlers use a common formatter displaying the time, logger name, log level,
    and the log message.

    Returns:
    logging.Logger: The configured logger with file and console handlers.
    """

    current_datetime = datetime.now()

    date_str = current_datetime.strftime("%Y-%m-%d")

    hour = current_datetime + timedelta(hours=1)
    hour_str = hour.strftime("%H:00")

    next_hour = current_datetime + timedelta(hours=2)
    next_hour_str = next_hour.strftime("%H:00")

    timestamp = f"{date_str} {hour_str}-{next_hour_str}"

    log_path = f"src/logs/{timestamp}.log"

    os.makedirs("src/logs", exist_ok=True)

    logger = logging.getLogger("configure_logger")

    logger.setLevel(logging.DEBUG)

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
        logger.addHandler(console_handler)

    return logger
