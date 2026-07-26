import os
import boto3
import logging

def upload_to_storage(config, file_path, logger: logging.Logger):
    s3 = boto3.client(
        "s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=config["storage"]["key_id"],
        aws_secret_access_key=config["storage"]["secret"],
    )
    file_name = os.path.basename(file_path)
    logger.info("▶ Загружаем файл в Object Storage...")
    s3.upload_file(file_path, config["storage"]["bucket"], file_name)
    return f"https://storage.yandexcloud.net/{config['storage']['bucket']}/{file_name}"
