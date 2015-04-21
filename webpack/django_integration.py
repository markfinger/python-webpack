from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from django.core.exceptions import ImproperlyConfigured
from .conf import settings


def validate_settings():
    from django.conf import settings

    finder_path = 'webpack.django_integration.WebpackFinder'

    if (
        ('staticfiles' in settings.INSTALLED_APPS or 'django.contrib.staticfiles' in settings.INSTALLED_APPS) and
        finder_path not in settings.STATICFILES_FINDERS
    ):
        raise ImproperlyConfigured(
            (
                'When using webpack together with staticfiles, please add \'{}\' to the '
                'STATICFILES_FINDERS setting.'
            ).format(finder_path)
        )


class WebpackFileStorage(FileSystemStorage):
    """
    Standard file system storage for files handled by django-webpack.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.BUNDLE_ROOT
        if base_url is None:
            base_url = settings.BUNDLE_URL
        super(WebpackFileStorage, self).__init__(location, base_url, *args, **kwargs)


class WebpackFinder(BaseStorageFinder):
    """
    A staticfiles finder that looks in BUNDLE_ROOT for generated bundles.

    To be used during development with staticfiles' development file server
    or during deployment.
    """
    storage = WebpackFileStorage

    def list(self, *args, **kwargs):
        return []