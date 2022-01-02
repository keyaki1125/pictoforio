from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    AWS S3にて、
    mediaファイルとstaticファイルを別フォルダで管理するためのバックエンド
    """

    location = 'media'
    file_overwrite = False