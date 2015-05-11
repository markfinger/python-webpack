import os
from optional_django import conf
from .exceptions import ImproperlyConfigured


class Conf(conf.Conf):
    BUNDLE_ROOT = None

    BUNDLE_URL = None

    OUTPUT_DIR = 'webpack'

    BUNDLE_DIR = 'bundles'

    CONFIG_DIR = 'config_files'

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

    def get_path_to_output_dir(self):
        return os.path.join(self.BUNDLE_ROOT, self.OUTPUT_DIR)

    def get_path_to_bundle_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.BUNDLE_DIR)

    def get_path_to_config_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.CONFIG_DIR)

settings = Conf()