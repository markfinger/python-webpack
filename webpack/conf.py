from optional_django import conf
from service_host.conf import settings as service_host_settings
from .exceptions import ImproperlyConfigured


class Conf(conf.Conf):
    django_namespace = 'WEBPACK'

    BUNDLE_ROOT = None
    BUNDLE_URL = None
    BUNDLE_DIR = 'webpack'
    WATCH_CONFIG_FILES = not service_host_settings.PRODUCTION
    WATCH_SOURCE_FILES = not service_host_settings.PRODUCTION
    OUTPUT_FULL_STATS = False
    SERVICE_NAME = 'webpack'

    def configure(self, **kwargs):
        super(Conf, self).configure(**kwargs)
        if self.BUNDLE_URL and not self.BUNDLE_URL.endswith('/'):
            raise ImproperlyConfigured('`BUNDLE_URL` must have a trailing slash')

settings = Conf()