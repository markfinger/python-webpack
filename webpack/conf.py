from optional_django import conf
from .exceptions import ImproperlyConfigured


class Conf(conf.Conf):
    django_namespace = 'WEBPACK'

    BUNDLE_ROOT = None

    BUNDLE_URL = None

    BUNDLE_DIR = 'webpack'

    WATCH_CONFIG_FILES = False

    WATCH_SOURCE_FILES = False

    WATCH_DELAY = 200
    
    OUTPUT_FULL_STATS = False

    TAG_TEMPLATES = {
        'css': '<link rel="stylesheet" href="{url}">',
        'js': '<script src="{url}"></script>',
    }

    JS_HOST_FUNCTION = 'webpack'

    def configure(self, **kwargs):
        if kwargs.get('BUNDLE_URL', None) and not kwargs['BUNDLE_URL'].endswith('/'):
            raise ImproperlyConfigured('`BUNDLE_URL` must have a trailing slash')

        super(Conf, self).configure(**kwargs)

settings = Conf()