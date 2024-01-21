import logging

import boto3
from botocore.exceptions import NoCredentialsError

class S3LogHandler(logging.Handler):
    def __init__(self, bucket, log_file):
        logging.Handler.__init__(self)
        self.bucket = bucket
        self.log_file = log_file
        self.s3 = boto3.client('s3')

    def emit(self, record):
        log_entry = self.format(record)
        try:
            # Dodajemy każdą linię logu jako nowy obiekt na S3
            self.s3.put_object(Bucket=self.bucket, Key=self.log_file, Body=log_entry)
        except NoCredentialsError:
            print("Brak poświadczeń do AWS S3")



def configure_logger(log_path: str, s3_bucket: str) -> logging.Logger:

    logger = logging.getLogger("configure_logger")

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    if s3_bucket:
        s3_handler = S3LogHandler(s3_bucket, log_path)
        s3_handler.setLevel(logging.DEBUG)
        s3_handler.setFormatter(formatter)
        
        logger.addHandler(s3_handler)

    logger.addHandler(file_handler)

    return logger
