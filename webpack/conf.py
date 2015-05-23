import os
from optional_django import conf
import js_host.conf


class Conf(conf.Conf):
    STATIC_ROOT = None

    STATIC_URL = None

    OUTPUT_DIR = 'webpack'

    BUNDLE_DIR = 'bundles'

    CONFIG_DIR = 'config_files'

    WATCH_CONFIG_FILES = False

    WATCH_SOURCE_FILES = False

    AGGREGATE_TIMEOUT = 200

    POLL = False
    
    TAG_TEMPLATES = {
        'css': '<link rel="stylesheet" href="{url}">',
        'js': '<script src="{url}"></script>',
    }

    JS_HOST_FUNCTION = 'webpack'

    COMPILE_OFFLINE = False

    OFFLINE_BUNDLES = []

    CACHE_FILE = '.webpack_cache.json'

    def get_path_to_output_dir(self):
        return os.path.join(self.STATIC_ROOT, self.OUTPUT_DIR)

    def get_path_to_bundle_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.BUNDLE_DIR)

    def get_path_to_config_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.CONFIG_DIR)

    def get_path_to_cache_file(self):
        if self.CACHE_FILE:
            if os.path.isabs(self.CACHE_FILE):
                return self.CACHE_FILE
            return os.path.join(js_host.conf.settings.SOURCE_ROOT, self.CACHE_FILE)

settings = Conf()
