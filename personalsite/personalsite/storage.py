from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class GarageMediaStorage(S3Boto3Storage):
    # overrides the URL to the nginx proxied location rather than the bucket prefix
    def url(self, name):
        return f'{settings.MEDIA_URL}{name}'

class Ckeditor5UploadsStorage(S3Boto3Storage):
    location = "embeds"

    def url(self, name):
        return f'{settings.MEDIA_URL}{self.location}/{name}'