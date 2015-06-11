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

    POLL = False

    OUTPUT_DIR = 'webpack'

    BUNDLE_DIR = 'bundles'

    CONFIG_DIR = 'config_files'

    def get_path_to_output_dir(self):
        return os.path.join(self.STATIC_ROOT, self.OUTPUT_DIR)

    def get_path_to_bundle_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.BUNDLE_DIR)

    def get_path_to_config_dir(self):
        return os.path.join(self.get_path_to_output_dir(), self.CONFIG_DIR)

settings = Conf()
