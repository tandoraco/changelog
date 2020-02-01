from storages.backends.s3boto3 import S3Boto3Storage
from datetime import datetime


class MediaStorage(S3Boto3Storage):
    location = f'user-uploads/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}'
    file_overwrite = False
