import os
from optional_django import conf


class Conf(conf.Conf):
    BUILD_SERVER_URL = 'http://127.0.0.1:9009'

    STATIC_ROOT = None

    STATIC_URL = None

    WATCH = True

    ENV = None

    HMR = False

    CACHE = True

    AGGREGATE_TIMEOUT = 200

    POLL = None

    OUTPUT_DIR = 'webpack'

    INTERNALS_DIR = '.webpack'

    CACHE_DIR = 'cache'

    CONFIG_FILES_DIR = 'config_files'

    def get_path_to_output_dir(self):
        return os.path.join(self.STATIC_ROOT, self.OUTPUT_DIR)

    def get_path_to_internals_dir(self):
        if os.path.isabs(self.INTERNALS_DIR):
            return self.INTERNALS_DIR
        return os.path.join(os.getcwd(), self.INTERNALS_DIR)

    def get_path_to_cache_dir(self):
        return os.path.join(self.get_path_to_internals_dir(), self.CACHE_DIR)

    def get_path_to_config_files_dir(self):
        return os.path.join(self.get_path_to_internals_dir(), self.CONFIG_FILES_DIR)

    def get_public_path(self):
        static_url = self.STATIC_URL
        if static_url and static_url.endswith('/'):
            static_url = static_url[0:-1]
        return '/'.join([static_url, self.OUTPUT_DIR])

settings = Conf()
