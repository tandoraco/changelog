from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'user-uploads'
    file_overwrite = False


class StaticFilesStorage(S3Boto3Storage):
    bucket_name = 'assets'
