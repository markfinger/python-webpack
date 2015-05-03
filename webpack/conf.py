from optional_django import conf
from .exceptions import ImproperlyConfigured


class Conf(conf.Conf):
    django_namespace = 'WEBPACK'

    BUNDLE_ROOT = None
    BUNDLE_URL = None
    BUNDLE_DIR = 'webpack'
    WATCH_CONFIG_FILES = False
    WATCH_SOURCE_FILES = False
    OUTPUT_FULL_STATS = False
    TAG_TEMPLATES = {
        'css': '<link rel="stylesheet" href="{url}">',
        'js': '<script src="{url}"></script>',
    }
    FUNCTION_NAME = 'webpack'

    def configure(self, **kwargs):
        super(Conf, self).configure(**kwargs)
        if self.BUNDLE_URL and not self.BUNDLE_URL.endswith('/'):
            raise ImproperlyConfigured('`BUNDLE_URL` must have a trailing slash')

settings = Conf()