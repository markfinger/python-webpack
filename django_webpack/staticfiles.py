from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from .settings import BUNDLE_ROOT, BUNDLE_URL


class WebpackFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by django-webpack.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = BUNDLE_ROOT
        if base_url is None:
            base_url = BUNDLE_URL
        super(WebpackFileStorage, self).__init__(location, base_url, *args, **kwargs)


class WebpackFinder(BaseStorageFinder):
    """
    A staticfiles finder that looks in BUNDLE_ROOT for generated bundles.

    To be used during development with staticfiles' development file server
    or during deployment.
    """
    storage = WebpackFileStorage

    def list(self, ignore_patterns):
        return []