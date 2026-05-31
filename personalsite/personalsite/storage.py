from storages.backends.s3boto3 import S3Boto3Storage

class GarageMediaStorage(S3Boto3Storage):
    """
    Upload via S3 API (authenticated), serve via nginx → Garage web endpoint (public).
    Overrides url() to return nginx-proxied paths instead of direct S3 API URLs.
    """
    def url(self, name):
        return f'/media/{name}'