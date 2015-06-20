from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from .conf import settings


class WebpackFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by webpack.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.STATIC_ROOT
        if base_url is None:
            base_url = settings.STATIC_URL
        super(WebpackFileStorage, self).__init__(location, base_url, *args, **kwargs)


class WebpackFinder(BaseStorageFinder):
    """
    A staticfiles finder that looks in webpack.conf.settings.STATIC_ROOT for generated bundles.

    To be used during development with staticfiles' development file server or during deployment.
    """
    storage = WebpackFileStorage

    def list(self, *args, **kwargs):
        return []
